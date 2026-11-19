import pytest
from django.contrib.auth import get_user_model

SENHA = "senha-de-teste-123"


@pytest.mark.django_db
def test_senha_nao_e_guardada_em_texto_simples():
    User = get_user_model()
    utilizador = User.objects.create_user(username="aluno", password=SENHA)

    assert utilizador.password != SENHA
    assert utilizador.check_password(SENHA)


@pytest.mark.django_db
def test_senha_errada_e_rejeitada():
    User = get_user_model()
    utilizador = User.objects.create_user(username="aluno", password=SENHA)

    assert not utilizador.check_password("outra-senha")
