from datetime import UTC, datetime

from django.conf import settings
from django.utils import timezone


def test_idioma_do_site_e_portugues():
    assert settings.LANGUAGE_CODE == "pt"


def test_hora_local_e_a_de_luanda():
    meio_dia_utc = datetime(2026, 1, 15, 12, 0, tzinfo=UTC)

    assert timezone.localtime(meio_dia_utc).hour == 13
