from django.contrib.auth.models import AbstractUser
from django.db import models
from users.enum_types import RoleTypes


class User(AbstractUser):
    role = models.CharField(max_length=7, choices=RoleTypes.items(), default=RoleTypes.STUDENT.value)
