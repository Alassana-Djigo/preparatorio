import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_o_admin_mostra_os_nomes_das_seccoes_em_portugues(admin_client):
    pagina = admin_client.get(reverse("admin:index")).content.decode()

    assert "Estrutura académica" in pagina
    assert "Contas" in pagina
    assert "Academics" not in pagina
    assert "Accounts" not in pagina
