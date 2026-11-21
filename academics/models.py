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

    kind = models.CharField(max_length=20, choices=Kind)
    title = models.CharField(max_length=200)
    url = models.URLField(blank=True)
    published_on = models.DateField(null=True, blank=True)
    retrieved_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class Provenance(models.Model):
    """Origem e verificação de um dado que descreve a realidade.

    Tudo nasce como demonstração por verificar. Um dado só pode ficar verificado se for
    oficial e tiver fonte, e a base de dados faz cumprir essa regra.
    """

    origin = models.CharField(max_length=10, choices=Origin, default=Origin.DEMO)
    source = models.ForeignKey(Source, null=True, blank=True, on_delete=models.PROTECT)
    verification_status = models.CharField(
        max_length=12, choices=VerificationStatus, default=VerificationStatus.UNVERIFIED
    )
    verified_on = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                condition=(
                    ~models.Q(verification_status=VerificationStatus.VERIFIED)
                    | (models.Q(origin=Origin.OFFICIAL) & models.Q(source__isnull=False))
                ),
                name="%(app_label)s_%(class)s_verified_needs_official_source",
            ),
        ]


class Institution(Provenance):
    name = models.CharField(max_length=200)
    acronym = models.CharField(max_length=20, blank=True)

    class Meta(Provenance.Meta):
        ordering = ["name"]

    def __str__(self):
        return self.name


class Faculty(Provenance):
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, related_name="faculties")
    name = models.CharField(max_length=200)

    class Meta(Provenance.Meta):
        ordering = ["name"]
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
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, related_name="courses")
    name = models.CharField(max_length=200)

    class Meta(Provenance.Meta):
        ordering = ["name"]
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

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
