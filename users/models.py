from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email=None, password=None, username=None, **extra_fields):
        if not email and username:
            # Compatibilidad con los usuarios de las pruebas anteriores.
            email = f'{username}@example.invalid'
        if not email:
            raise ValueError('El correo electrónico es obligatorio.')
        email = self.normalize_email(email)
        if not username:
            username = email
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if not extra_fields['is_staff'] or not extra_fields['is_superuser']:
            raise ValueError('El superusuario requiere is_staff e is_superuser.')
        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField('teléfono', max_length=20, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
