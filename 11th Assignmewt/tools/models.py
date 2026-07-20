from django.db import models
from core.models import AuditMixin


class Tool(AuditMixin):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name
