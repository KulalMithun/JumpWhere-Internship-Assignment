from django.db import models
from core.models import AuditMixin
from coding.models import Coding
from tools.models import Tool


class Project(AuditMixin):
    STATUS_CHOICES = (('ongoing', 'Ongoing'), ('completed', 'Completed'))

    name = models.CharField(max_length=240)
    description = models.TextField(blank=True)
    technologies = models.ManyToManyField(Coding, blank=True, related_name='projects')
    tools = models.ManyToManyField(Tool, blank=True, related_name='projects')
    role_responsibilities = models.JSONField(default=list, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='ongoing')
    employees = models.ManyToManyField('employees.Employee', blank=True, related_name='projects')

    def __str__(self) -> str:
        return self.name
