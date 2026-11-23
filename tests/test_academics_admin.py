from datetime import date

import pytest
from django.contrib import admin
from django.urls import reverse
from django.utils import timezone

from academics.models import (
    AdmissionCycle,
    Course,
    CourseRequirement,
    Faculty,
    Institution,
    Origin,
    Source,
    Subject,
    VerificationStatus,
)


@pytest.fixture
def fonte():
    return Source.objects.create(kind=Source.Kind.NOTICE, title="Edital de exemplo")


def mensagens(resposta):
    return [str(m) for m in resposta.context["messages"]]


@pytest.mark.parametrize(
    "modelo",
    [Source, Institution, Faculty, Course, Subject, AdmissionCycle, CourseRequirement],
)
def test_todos_os_modelos_do_dominio_podem_ser_geridos_no_admin(modelo):
    assert admin.site.is_registered(modelo)


@pytest.mark.django_db
def test_a_acao_verifica_so_dados_oficiais_com_fonte(admin_client, fonte):
    oficial = Institution.objects.create(name="Oficial", origin=Origin.OFFICIAL, source=fonte)
    demo = Institution.objects.create(name="Demo", source=fonte)
    sem_fonte = Institution.objects.create(name="Sem fonte", origin=Origin.OFFICIAL)

    resposta = admin_client.post(
        reverse("admin:academics_institution_changelist"),
        {"action": "mark_verified", "_selected_action": [oficial.pk, demo.pk, sem_fonte.pk]},
        follow=True,
    )

    for instituicao in (oficial, demo, sem_fonte):
        instituicao.refresh_from_db()
    assert oficial.verification_status == VerificationStatus.VERIFIED
    assert oficial.verified_on == timezone.localdate()
    assert demo.verification_status == VerificationStatus.UNVERIFIED
    assert sem_fonte.verification_status == VerificationStatus.UNVERIFIED
    assert any("2 registo(s) ignorado(s)" in texto for texto in mensagens(resposta))


@pytest.mark.django_db
def test_a_acao_remove_a_verificacao_e_limpa_a_data(admin_client, fonte):
    instituicao = Institution.objects.create(
        name="Oficial",
        origin=Origin.OFFICIAL,
        source=fonte,
        verification_status=VerificationStatus.VERIFIED,
        verified_on=date(2026, 1, 1),
    )

    admin_client.post(
        reverse("admin:academics_institution_changelist"),
        {"action": "mark_unverified", "_selected_action": [instituicao.pk]},
    )

    instituicao.refresh_from_db()
    assert instituicao.verification_status == VerificationStatus.UNVERIFIED
    assert instituicao.verified_on is None


@pytest.mark.django_db
def test_ao_gravar_como_verificado_regista_a_data_de_hoje(admin_client, fonte):
    admin_client.post(
        reverse("admin:academics_institution_add"),
        {
            "name": "Instituição de Exemplo",
            "acronym": "IEX",
            "origin": Origin.OFFICIAL,
            "source": fonte.pk,
            "verification_status": VerificationStatus.VERIFIED,
        },
    )

    instituicao = Institution.objects.get(name="Instituição de Exemplo")
    assert instituicao.verified_on == timezone.localdate()


@pytest.mark.django_db
def test_o_formulario_recusa_um_dado_verificado_sem_fonte(admin_client):
    resposta = admin_client.post(
        reverse("admin:academics_institution_add"),
        {
            "name": "Instituição de Exemplo",
            "acronym": "IEX",
            "origin": Origin.OFFICIAL,
            "verification_status": VerificationStatus.VERIFIED,
        },
    )

    assert resposta.status_code == 200
    assert not Institution.objects.exists()


def dados_de_uma_exigencia(concurso, curso, disciplina):
    return {
        "admission_cycle": concurso.pk,
        "course": curso.pk,
        "subject": disciplina.pk,
        "origin": Origin.DEMO,
        "verification_status": VerificationStatus.UNVERIFIED,
    }


@pytest.mark.django_db
def test_o_admin_cria_uma_exigencia_valida(admin_client):
    instituicao = Institution.objects.create(name="Instituição de Exemplo")
    concurso = AdmissionCycle.objects.create(institution=instituicao, academic_year="2026/2027")
    faculdade = Faculty.objects.create(institution=instituicao, name="Faculdade de Exemplo")
    curso = Course.objects.create(faculty=faculdade, name="Curso de Exemplo")
    disciplina = Subject.objects.create(name="Matemática")

    admin_client.post(
        reverse("admin:academics_courserequirement_add"),
        dados_de_uma_exigencia(concurso, curso, disciplina),
    )

    assert CourseRequirement.objects.filter(admission_cycle=concurso, course=curso).count() == 1


@pytest.mark.django_db
def test_o_admin_recusa_uma_exigencia_com_curso_de_outra_instituicao(admin_client):
    instituicao = Institution.objects.create(name="Instituição de Exemplo")
    outra = Institution.objects.create(name="Outra Instituição de Exemplo")
    concurso = AdmissionCycle.objects.create(institution=instituicao, academic_year="2026/2027")
    faculdade_de_outra = Faculty.objects.create(institution=outra, name="Faculdade de Exemplo")
    curso_de_outra = Course.objects.create(faculty=faculdade_de_outra, name="Curso de Exemplo")
    disciplina = Subject.objects.create(name="Matemática")

    resposta = admin_client.post(
        reverse("admin:academics_courserequirement_add"),
        dados_de_uma_exigencia(concurso, curso_de_outra, disciplina),
    )

    assert resposta.status_code == 200
    assert "O curso tem de pertencer à instituição do concurso." in resposta.content.decode()
    assert not CourseRequirement.objects.exists()
