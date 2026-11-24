from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


class Origin(models.TextChoices):
    OFFICIAL = "official", "Oficial"
    DEMO = "demo", "Demonstração"


class VerificationStatus(models.TextChoices):
    UNVERIFIED = "unverified", "Por verificar"
    VERIFIED = "verified", "Verificado"


class Source(models.Model):
    """Documento de onde vem uma informação: edital, programa oficial, site..."""

    class Kind(models.TextChoices):
        NOTICE = "notice", "Edital"
        OFFICIAL_PROGRAM = "official_program", "Programa oficial"
        WEBSITE = "website", "Site da instituição"
        OTHER = "other", "Outro"

    kind = models.CharField("tipo", max_length=20, choices=Kind)
    title = models.CharField("título", max_length=200)
    url = models.URLField("endereço (URL)", blank=True)
    published_on = models.DateField("publicado em", null=True, blank=True)
    retrieved_on = models.DateField("consultado em", null=True, blank=True)

    class Meta:
        verbose_name = "fonte"
        verbose_name_plural = "fontes"

    def __str__(self):
        return self.title


class Provenance(models.Model):
    """Origem e verificação de um dado que descreve a realidade.

    Tudo nasce como demonstração por verificar. Um dado só pode ficar verificado se for
    oficial e tiver fonte, e a base de dados faz cumprir essa regra.
    """

    origin = models.CharField("origem", max_length=10, choices=Origin, default=Origin.DEMO)
    source = models.ForeignKey(
        Source, verbose_name="fonte", null=True, blank=True, on_delete=models.PROTECT
    )
    verification_status = models.CharField(
        "estado de verificação",
        max_length=12,
        choices=VerificationStatus,
        default=VerificationStatus.UNVERIFIED,
    )
    verified_on = models.DateField("verificado em", null=True, blank=True)

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                condition=(
                    ~models.Q(verification_status=VerificationStatus.VERIFIED)
                    | (models.Q(origin=Origin.OFFICIAL) & models.Q(source__isnull=False))
                ),
                name="%(app_label)s_%(class)s_verified_needs_official_source",
                violation_error_message="Um dado verificado tem de ser oficial e ter fonte.",
            ),
        ]


class Institution(Provenance):
    name = models.CharField("nome", max_length=200)
    acronym = models.CharField("sigla", max_length=20, blank=True)

    class Meta(Provenance.Meta):
        ordering = ["name"]
        verbose_name = "instituição"
        verbose_name_plural = "instituições"

    def __str__(self):
        return self.name


class Faculty(Provenance):
    institution = models.ForeignKey(
        Institution,
        verbose_name="instituição",
        on_delete=models.PROTECT,
        related_name="faculties",
    )
    name = models.CharField("nome", max_length=200)

    class Meta(Provenance.Meta):
        ordering = ["name"]
        verbose_name = "faculdade"
        verbose_name_plural = "faculdades"
        constraints = [
            *Provenance.Meta.constraints,
            models.UniqueConstraint(
                fields=["institution", "name"],
                name="academics_faculty_unique_name_per_institution",
            ),
        ]

    def __str__(self):
        return self.name


class Course(Provenance):
    faculty = models.ForeignKey(
        Faculty, verbose_name="faculdade", on_delete=models.PROTECT, related_name="courses"
    )
    name = models.CharField("nome", max_length=200)

    class Meta(Provenance.Meta):
        ordering = ["name"]
        verbose_name = "curso"
        verbose_name_plural = "cursos"
        constraints = [
            *Provenance.Meta.constraints,
            models.UniqueConstraint(
                fields=["faculty", "name"],
                name="academics_course_unique_name_per_faculty",
            ),
        ]

    def __str__(self):
        return self.name


class Subject(models.Model):
    """Catálogo único e partilhado de disciplinas (Matemática, Física...)."""

    name = models.CharField("nome", max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "disciplina"
        verbose_name_plural = "disciplinas"

    def __str__(self):
        return self.name


class AdmissionCycle(Provenance):
    """Concurso de acesso: uma instituição num ano letivo."""

    institution = models.ForeignKey(
        Institution,
        verbose_name="instituição",
        on_delete=models.PROTECT,
        related_name="admission_cycles",
    )
    academic_year = models.CharField(
        "ano letivo",
        max_length=9,
        validators=[RegexValidator(r"^\d{4}(/\d{4})?$", "Use o formato 2026 ou 2026/2027.")],
    )

    class Meta(Provenance.Meta):
        ordering = ["-academic_year"]
        verbose_name = "concurso de acesso"
        verbose_name_plural = "concursos de acesso"
        constraints = [
            *Provenance.Meta.constraints,
            models.UniqueConstraint(
                fields=["institution", "academic_year"],
                name="academics_cycle_unique_year_per_institution",
            ),
        ]

    def __str__(self):
        return f"{self.institution} {self.academic_year}"


class CourseRequirement(Provenance):
    """Num concurso, um curso exige uma disciplina, com um peso opcional.

    A regra de que o curso pertence à instituição do concurso atravessa três tabelas e não
    se consegue exprimir numa restrição da base de dados. É validada ao gravar. Operações em
    massa (bulk_create, update) saltam esta validação, por isso não se usam aqui sem a repetir.
    """

    admission_cycle = models.ForeignKey(
        AdmissionCycle,
        verbose_name="concurso de acesso",
        on_delete=models.PROTECT,
        related_name="requirements",
    )
    course = models.ForeignKey(
        Course, verbose_name="curso", on_delete=models.PROTECT, related_name="requirements"
    )
    subject = models.ForeignKey(
        Subject, verbose_name="disciplina", on_delete=models.PROTECT, related_name="requirements"
    )
    weight = models.DecimalField("peso", max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta(Provenance.Meta):
        verbose_name = "exigência"
        verbose_name_plural = "exigências"
        constraints = [
            *Provenance.Meta.constraints,
            models.UniqueConstraint(
                fields=["admission_cycle", "course", "subject"],
                name="academics_requirement_unique_per_cycle_course_subject",
            ),
            models.CheckConstraint(
                condition=models.Q(weight__isnull=True) | models.Q(weight__gt=0),
                name="academics_requirement_weight_positive",
                violation_error_message="O peso tem de ser positivo.",
            ),
        ]

    def __str__(self):
        return f"{self.admission_cycle}: {self.course} - {self.subject}"

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if not (self.course_id and self.admission_cycle_id):
            return
        if self.course.faculty.institution_id != self.admission_cycle.institution_id:
            raise ValidationError("O curso tem de pertencer à instituição do concurso.")
