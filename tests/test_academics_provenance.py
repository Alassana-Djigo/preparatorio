import pytest
from django.db import IntegrityError, transaction

from academics.models import Institution, Origin, Source, VerificationStatus


@pytest.fixture
def fonte():
    return Source.objects.create(kind=Source.Kind.NOTICE, title="Edital de exemplo")


@pytest.mark.django_db
def test_um_dado_novo_e_demonstracao_por_verificar():
    instituicao = Institution.objects.create(name="Instituição de Exemplo", acronym="IEX")

    assert instituicao.origin == Origin.DEMO
    assert instituicao.verification_status == VerificationStatus.UNVERIFIED


@pytest.mark.django_db
def test_um_dado_oficial_com_fonte_pode_ser_verificado(fonte):
    instituicao = Institution.objects.create(
        name="Instituição de Exemplo",
        acronym="IEX",
        origin=Origin.OFFICIAL,
        source=fonte,
        verification_status=VerificationStatus.VERIFIED,
    )

    assert instituicao.verification_status == VerificationStatus.VERIFIED


@pytest.mark.django_db
def test_um_dado_verificado_sem_fonte_e_recusado():
    with pytest.raises(IntegrityError), transaction.atomic():
        Institution.objects.create(
            name="Instituição de Exemplo",
            acronym="IEX",
            origin=Origin.OFFICIAL,
            verification_status=VerificationStatus.VERIFIED,
        )


@pytest.mark.django_db
def test_um_dado_de_demonstracao_nunca_fica_verificado(fonte):
    with pytest.raises(IntegrityError), transaction.atomic():
        Institution.objects.create(
            name="Instituição de Exemplo",
            acronym="IEX",
            origin=Origin.DEMO,
            source=fonte,
            verification_status=VerificationStatus.VERIFIED,
        )
