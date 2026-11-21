import pytest
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError

from academics.models import (
    Course,
    Faculty,
    Institution,
    Origin,
    Source,
    Subject,
    VerificationStatus,
)


@pytest.fixture
def instituicao():
    return Institution.objects.create(name="Instituição de Exemplo", acronym="IEX")


@pytest.fixture
def faculdade(instituicao):
    return Faculty.objects.create(institution=instituicao, name="Faculdade de Exemplo")


def criar(modelo, instituicao, faculdade, **extra):
    """Cria uma instância válida de qualquer modelo com proveniência."""
    if modelo is Institution:
        return Institution.objects.create(name="Outra Instituição", **extra)
    if modelo is Faculty:
        return Faculty.objects.create(institution=instituicao, name="Outra Faculdade", **extra)
    return Course.objects.create(faculty=faculdade, name="Outro Curso", **extra)


@pytest.mark.django_db
def test_faculdades_e_cursos_ficam_ligados_a_quem_os_contem(instituicao, faculdade):
    curso = Course.objects.create(faculty=faculdade, name="Curso de Exemplo")

    assert list(instituicao.faculties.all()) == [faculdade]
    assert list(faculdade.courses.all()) == [curso]


@pytest.mark.django_db
def test_nao_ha_duas_faculdades_com_o_mesmo_nome_na_mesma_instituicao(instituicao, faculdade):
    with pytest.raises(IntegrityError), transaction.atomic():
        Faculty.objects.create(institution=instituicao, name=faculdade.name)


@pytest.mark.django_db
def test_o_mesmo_nome_de_faculdade_pode_existir_noutra_instituicao(faculdade):
    outra = Institution.objects.create(name="Outra Instituição de Exemplo", acronym="OIE")

    repetida = Faculty.objects.create(institution=outra, name=faculdade.name)

    assert repetida.pk != faculdade.pk


@pytest.mark.django_db
def test_nao_ha_dois_cursos_com_o_mesmo_nome_na_mesma_faculdade(faculdade):
    Course.objects.create(faculty=faculdade, name="Curso de Exemplo")

    with pytest.raises(IntegrityError), transaction.atomic():
        Course.objects.create(faculty=faculdade, name="Curso de Exemplo")


@pytest.mark.django_db
def test_o_mesmo_nome_de_curso_pode_existir_noutra_faculdade(instituicao, faculdade):
    outra = Faculty.objects.create(institution=instituicao, name="Outra Faculdade de Exemplo")
    Course.objects.create(faculty=faculdade, name="Curso de Exemplo")

    repetido = Course.objects.create(faculty=outra, name="Curso de Exemplo")

    assert repetido.faculty == outra


@pytest.mark.django_db
def test_nao_ha_duas_disciplinas_com_o_mesmo_nome():
    Subject.objects.create(name="Matemática")

    with pytest.raises(IntegrityError), transaction.atomic():
        Subject.objects.create(name="Matemática")


@pytest.mark.django_db
def test_nao_se_apaga_uma_instituicao_que_tem_faculdades(instituicao, faculdade):
    with pytest.raises(ProtectedError):
        instituicao.delete()


@pytest.mark.django_db
@pytest.mark.parametrize("modelo", [Institution, Faculty, Course])
def test_um_dado_novo_e_demonstracao_por_verificar(modelo, instituicao, faculdade):
    dado = criar(modelo, instituicao, faculdade)

    assert dado.origin == Origin.DEMO
    assert dado.verification_status == VerificationStatus.UNVERIFIED


@pytest.mark.django_db
@pytest.mark.parametrize("modelo", [Institution, Faculty, Course])
def test_a_regra_de_verificacao_vale_em_todos_os_modelos(modelo, instituicao, faculdade):
    with pytest.raises(IntegrityError), transaction.atomic():
        criar(
            modelo,
            instituicao,
            faculdade,
            origin=Origin.OFFICIAL,
            verification_status=VerificationStatus.VERIFIED,
        )


@pytest.mark.django_db
@pytest.mark.parametrize("modelo", [Institution, Faculty, Course])
def test_oficial_com_fonte_fica_verificado_em_todos_os_modelos(modelo, instituicao, faculdade):
    fonte = Source.objects.create(kind=Source.Kind.NOTICE, title="Edital de exemplo")

    dado = criar(
        modelo,
        instituicao,
        faculdade,
        origin=Origin.OFFICIAL,
        source=fonte,
        verification_status=VerificationStatus.VERIFIED,
    )

    assert dado.verification_status == VerificationStatus.VERIFIED
