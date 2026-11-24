from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse

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

MENSAGEM_DE_VERIFICACAO = "Um dado verificado tem de ser oficial e ter fonte."


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("modelo", "rotulo"),
    [
        ("source", "Título"),
        ("institution", "Sigla"),
        ("faculty", "Instituição"),
        ("course", "Faculdade"),
        ("subject", "Nome"),
        ("admissioncycle", "Ano letivo"),
        ("courserequirement", "Concurso de acesso"),
    ],
)
def test_o_admin_mostra_os_rotulos_em_portugues(admin_client, modelo, rotulo):
    resposta = admin_client.get(reverse(f"admin:academics_{modelo}_add"))

    assert rotulo in resposta.content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize("modelo", ["institution", "faculty", "course"])
def test_os_dados_com_proveniencia_mostram_o_estado_de_verificacao(admin_client, modelo):
    resposta = admin_client.get(reverse(f"admin:academics_{modelo}_add"))

    assert "Estado de verificação" in resposta.content.decode()


@pytest.mark.django_db
def test_verificar_sem_fonte_mostra_uma_mensagem_clara_no_modelo():
    instituicao = Institution(
        name="Instituição de Exemplo",
        origin=Origin.OFFICIAL,
        verification_status=VerificationStatus.VERIFIED,
    )

    with pytest.raises(ValidationError) as erro:
        instituicao.full_clean()

    assert MENSAGEM_DE_VERIFICACAO in str(erro.value)


@pytest.mark.django_db
def test_verificar_sem_fonte_mostra_uma_mensagem_clara_no_admin(admin_client):
    resposta = admin_client.post(
        reverse("admin:academics_institution_add"),
        {
            "name": "Instituição de Exemplo",
            "origin": Origin.OFFICIAL,
            "verification_status": VerificationStatus.VERIFIED,
        },
    )

    assert MENSAGEM_DE_VERIFICACAO in resposta.content.decode()
    assert not Institution.objects.exists()


@pytest.mark.django_db
def test_um_peso_negativo_mostra_uma_mensagem_clara():
    instituicao = Institution.objects.create(name="Instituição de Exemplo")
    faculdade = Faculty.objects.create(institution=instituicao, name="Faculdade de Exemplo")
    curso = Course.objects.create(faculty=faculdade, name="Curso de Exemplo")
    concurso = AdmissionCycle.objects.create(institution=instituicao, academic_year="2026/2027")
    disciplina = Subject.objects.create(name="Matemática")
    exigencia = CourseRequirement(
        admission_cycle=concurso, course=curso, subject=disciplina, weight=Decimal("-1")
    )

    with pytest.raises(ValidationError) as erro:
        exigencia.full_clean()

    assert "O peso tem de ser positivo." in str(erro.value)
