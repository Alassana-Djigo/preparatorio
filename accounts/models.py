from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Utilizador da plataforma. Ver docs/adr/0005-modelo-de-utilizador-personalizado.md."""
