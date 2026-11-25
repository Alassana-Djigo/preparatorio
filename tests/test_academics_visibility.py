import os
import subprocess
import sys
from pathlib import Path

import pytest

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

RAIZ = Path(__file__).resolve().parent.parent

POR_VERIFICAR = {"origin": Origin.OFFICIAL}
DEMONSTRACAO = {}


@pytest.fixture
def fonte():
    return Source.objects.create(kind=Source.Kind.NOTICE, title="Edital de exemplo")


def verificado(fonte):
    return {
        "origin": Origin.OFFICIAL,
        "source": fonte,
        "verification_status": VerificationStatus.VERIFIED,
    }


def criar_cadeia(fonte):
    """Uma exigência com toda a cadeia de que depende, tudo oficial e verificado."""
    instituicao = Institution.objects.create(name="Instituição", **verificado(fonte))
    faculdade = Faculty.objects.create(
        institution=instituicao, name="Faculdade", **verificado(fonte)
    )
    curso = Course.objects.create(faculty=faculdade, name="Curso", **verificado(fonte))
    concurso = AdmissionCycle.objects.create(
        institution=instituicao, academic_year="2026/2027", **verificado(fonte)
    )
    disciplina = Subject.objects.create(name="Matemática")
    exigencia = CourseRequirement.objects.create(
        admission_cycle=concurso, course=curso, subject=disciplina, **verificado(fonte)
    )
    return {
        "instituicao": instituicao,
        "faculdade": faculdade,
        "curso": curso,
        "concurso": concurso,
        "exigencia": exigencia,
    }


def valor_da_opcao(modulo, extra=None):
    """Lê SHOW_DEMO_DATA num processo à parte, para ver o valor por defeito de cada módulo."""
    env = {k: v for k, v in os.environ.items() if k != "DJANGO_SHOW_DEMO_DATA"}
    env.update(extra or {})
    codigo = f"from config.settings import {modulo}; print({modulo}.SHOW_DEMO_DATA)"
    resultado = subprocess.run(
        [sys.executable, "-c", codigo], capture_output=True, text=True, cwd=RAIZ, env=env
    )
    assert resultado.returncode == 0, resultado.stderr
    return resultado.stdout.strip()


def test_a_demonstracao_vem_desligada_por_defeito():
    assert valor_da_opcao("base") == "False"


def test_a_demonstracao_liga_se_o_ambiente_pedir():
    assert valor_da_opcao("base", {"DJANGO_SHOW_DEMO_DATA": "true"}) == "True"


def test_no_desenvolvimento_a_demonstracao_vem_ligada():
    assert valor_da_opcao("dev") == "True"


@pytest.mark.django_db
def test_em_producao_so_o_oficial_verificado_e_publico(settings, fonte):
    settings.SHOW_DEMO_DATA = False
    Institution.objects.create(name="Oficial", **verificado(fonte))
    Institution.objects.create(name="Por verificar", **POR_VERIFICAR)
    Institution.objects.create(name="Demonstração", **DEMONSTRACAO)

    assert {i.name for i in Institution.objects.public()} == {"Oficial"}
    assert Institution.objects.count() == 3


@pytest.mark.django_db
def test_com_a_demonstracao_ligada_nunca_aparece_o_por_verificar(settings, fonte):
    settings.SHOW_DEMO_DATA = True
    Institution.objects.create(name="Oficial", **verificado(fonte))
    Institution.objects.create(name="Por verificar", **POR_VERIFICAR)
    Institution.objects.create(name="Demonstração", **DEMONSTRACAO)

    assert {i.name for i in Institution.objects.public()} == {"Oficial", "Demonstração"}


@pytest.mark.django_db
def test_public_pode_ser_combinado_com_outros_filtros(settings, fonte):
    settings.SHOW_DEMO_DATA = False
    Institution.objects.create(name="Alfa", acronym="A", **verificado(fonte))
    Institution.objects.create(name="Beta", acronym="B", **verificado(fonte))

    assert [i.name for i in Institution.objects.filter(acronym="B").public()] == ["Beta"]
    assert [i.name for i in Institution.objects.public().filter(acronym="A")] == ["Alfa"]


@pytest.mark.django_db
def test_uma_cadeia_toda_verificada_e_publica(settings, fonte):
    settings.SHOW_DEMO_DATA = False
    criar_cadeia(fonte)

    for modelo in (Institution, Faculty, Course, AdmissionCycle, CourseRequirement):
        assert modelo.objects.public().count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize("demonstracao_ligada", [False, True])
@pytest.mark.parametrize(
    ("modelo", "elo"),
    [
        (Faculty, "instituicao"),
        (Faculty, "faculdade"),
        (Course, "instituicao"),
        (Course, "faculdade"),
        (Course, "curso"),
        (AdmissionCycle, "instituicao"),
        (AdmissionCycle, "concurso"),
        (CourseRequirement, "instituicao"),
        (CourseRequirement, "faculdade"),
        (CourseRequirement, "curso"),
        (CourseRequirement, "concurso"),
        (CourseRequirement, "exigencia"),
    ],
)
def test_um_elo_por_verificar_esconde_tudo_o_que_depende_dele(
    settings, fonte, modelo, elo, demonstracao_ligada
):
    settings.SHOW_DEMO_DATA = demonstracao_ligada
    cadeia = criar_cadeia(fonte)
    elo_estragado = cadeia[elo]
    type(elo_estragado).objects.filter(pk=elo_estragado.pk).update(
        verification_status=VerificationStatus.UNVERIFIED
    )

    assert modelo.objects.public().count() == 0


@pytest.mark.django_db
def test_dados_de_demonstracao_formam_cadeias_visiveis_so_com_a_opcao_ligada(settings):
    instituicao = Institution.objects.create(name="Instituição")
    faculdade = Faculty.objects.create(institution=instituicao, name="Faculdade")

    settings.SHOW_DEMO_DATA = True
    assert list(Faculty.objects.public()) == [faculdade]

    settings.SHOW_DEMO_DATA = False
    assert list(Faculty.objects.public()) == []


@pytest.mark.django_db
def test_a_etiqueta_diz_a_verdade_sobre_a_proveniencia(fonte):
    oficial = Institution.objects.create(name="A", **verificado(fonte))
    por_verificar = Institution.objects.create(name="B", **POR_VERIFICAR)
    demonstracao = Institution.objects.create(name="C", **DEMONSTRACAO)

    assert oficial.provenance_label == "Oficial verificado"
    assert por_verificar.provenance_label == "Oficial, por verificar"
    assert demonstracao.provenance_label == "Dados de demonstração"
