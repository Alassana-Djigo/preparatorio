from django.conf import settings
from django.contrib.auth import get_user_model


def test_django_usa_o_user_do_modulo_accounts():
    assert settings.AUTH_USER_MODEL == "accounts.User"


def test_get_user_model_devolve_o_user_do_accounts():
    User = get_user_model()

    assert User._meta.app_label == "accounts"
    assert User.__name__ == "User"
