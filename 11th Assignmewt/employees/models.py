from django.db import models
from core.models import AuditMixin
from coding.models import Coding
from tools.models import Tool


class Employee(AuditMixin):
    STATUS_CHOICES = (('current', 'Current'), ('ex', 'Ex Employee'))

    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200, blank=True)
    professional_summary = models.JSONField(default=list, blank=True)
    coding = models.ManyToManyField(Coding, blank=True, related_name='employees')
    tools = models.ManyToManyField(Tool, blank=True, related_name='employees')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='current')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    years_of_experience = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name
