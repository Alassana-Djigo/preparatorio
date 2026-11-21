from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError

from academics.models import (
    AdmissionCycle,
    Course,
    CourseRequirement,
    Faculty,
    Institution,
    Origin,
    Subject,
    VerificationStatus,
)


@pytest.fixture
def instituicao():
    return Institution.objects.create(name="Instituição de Exemplo", acronym="IEX")


@pytest.fixture
def curso(instituicao):
    faculdade = Faculty.objects.create(institution=instituicao, name="Faculdade de Exemplo")
    return Course.objects.create(faculty=faculdade, name="Curso de Exemplo")


@pytest.fixture
def concurso(instituicao):
    return AdmissionCycle.objects.create(institution=instituicao, academic_year="2026/2027")


@pytest.fixture
def matematica():
    return Subject.objects.create(name="Matemática")


@pytest.fixture
def fisica():
    return Subject.objects.create(name="Física")


def exigir(concurso, curso, disciplina, **extra):
    return CourseRequirement.objects.create(
        admission_cycle=concurso, course=curso, subject=disciplina, **extra
    )


@pytest.mark.django_db
def test_uma_exigencia_liga_concurso_curso_e_disciplina(concurso, curso, matematica):
    exigencia = exigir(concurso, curso, matematica)

    assert list(concurso.requirements.all()) == [exigencia]
    assert list(curso.requirements.all()) == [exigencia]
    assert list(matematica.requirements.all()) == [exigencia]


@pytest.mark.django_db
def test_o_curso_tem_de_ser_da_instituicao_do_concurso(concurso, matematica):
    outra = Institution.objects.create(name="Outra Instituição de Exemplo", acronym="OIE")
    faculdade_de_outra = Faculty.objects.create(institution=outra, name="Faculdade de Exemplo")
    curso_de_outra = Course.objects.create(faculty=faculdade_de_outra, name="Curso de Exemplo")

    with pytest.raises(ValidationError):
        exigir(concurso, curso_de_outra, matematica)


@pytest.mark.django_db
def test_nao_ha_duas_exigencias_iguais(concurso, curso, matematica):
    exigir(concurso, curso, matematica)

    with pytest.raises(IntegrityError), transaction.atomic():
        exigir(concurso, curso, matematica)


@pytest.mark.django_db
def test_a_mesma_exigencia_pode_repetir_se_noutro_concurso(
    instituicao, concurso, curso, matematica
):
    outro_ano = AdmissionCycle.objects.create(institution=instituicao, academic_year="2027/2028")
    exigir(concurso, curso, matematica)

    repetida = exigir(outro_ano, curso, matematica)

    assert repetida.admission_cycle == outro_ano


@pytest.mark.django_db
@pytest.mark.parametrize("peso", [Decimal("0"), Decimal("-1")])
def test_o_peso_tem_de_ser_positivo(peso, concurso, curso, matematica):
    with pytest.raises(IntegrityError), transaction.atomic():
        exigir(concurso, curso, matematica, weight=peso)


@pytest.mark.django_db
def test_o_peso_e_opcional_e_aceita_valores_positivos(concurso, curso, matematica, fisica):
    sem_peso = exigir(concurso, curso, matematica)
    com_peso = exigir(concurso, curso, fisica, weight=Decimal("2.5"))

    assert sem_peso.weight is None
    assert com_peso.weight == Decimal("2.5")


@pytest.mark.django_db
def test_so_ha_um_concurso_por_instituicao_e_ano(instituicao, concurso):
    with pytest.raises(IntegrityError), transaction.atomic():
        AdmissionCycle.objects.create(institution=instituicao, academic_year=concurso.academic_year)


@pytest.mark.django_db
def test_o_mesmo_ano_pode_existir_noutra_instituicao(concurso):
    outra = Institution.objects.create(name="Outra Instituição de Exemplo", acronym="OIE")

    repetido = AdmissionCycle.objects.create(
        institution=outra, academic_year=concurso.academic_year
    )

    assert repetido.pk != concurso.pk


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("ano", "valido"),
    [("2026", True), ("2026/2027", True), ("26-27", False), ("2026/27", False), ("", False)],
)
def test_formato_do_ano_letivo(ano, valido, instituicao):
    concurso = AdmissionCycle(institution=instituicao, academic_year=ano)

    if valido:
        concurso.full_clean()
    else:
        with pytest.raises(ValidationError):
            concurso.full_clean()


@pytest.mark.django_db
def test_a_regra_de_verificacao_vale_nos_concursos(instituicao):
    with pytest.raises(IntegrityError), transaction.atomic():
        AdmissionCycle.objects.create(
            institution=instituicao,
            academic_year="2030/2031",
            origin=Origin.OFFICIAL,
            verification_status=VerificationStatus.VERIFIED,
        )


@pytest.mark.django_db
def test_a_regra_de_verificacao_vale_nas_exigencias(concurso, curso, matematica):
    with pytest.raises(IntegrityError), transaction.atomic():
        exigir(
            concurso,
            curso,
            matematica,
            origin=Origin.OFFICIAL,
            verification_status=VerificationStatus.VERIFIED,
        )


@pytest.mark.django_db
def test_nao_se_apaga_um_concurso_com_exigencias(concurso, curso, matematica):
    exigir(concurso, curso, matematica)

    with pytest.raises(ProtectedError):
        concurso.delete()


@pytest.mark.django_db
def test_nao_se_apaga_uma_disciplina_usada_numa_exigencia(concurso, curso, matematica):
    exigir(concurso, curso, matematica)

    with pytest.raises(ProtectedError):
        matematica.delete()


@pytest.mark.django_db
def test_responde_que_cursos_exigem_uma_disciplina_num_concurso(
    concurso, curso, matematica, fisica
):
    outro_curso = Course.objects.create(faculty=curso.faculty, name="Outro Curso de Exemplo")
    exigir(concurso, curso, fisica)
    exigir(concurso, outro_curso, matematica)

    cursos = Course.objects.filter(
        requirements__admission_cycle=concurso, requirements__subject=fisica
    )

    assert list(cursos) == [curso]
