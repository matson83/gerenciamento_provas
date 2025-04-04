from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        PARTICIPANTE = 'PARTICIPANTE', 'Participante'
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PARTICIPANTE
    )
    
    def is_admin(self):
        return self.role == self.Role.ADMIN
 