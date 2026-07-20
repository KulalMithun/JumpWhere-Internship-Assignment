from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    name = models.CharField(max_length=150, blank=True)

    def __str__(self) -> str:
        return self.get_full_name() or self.username
