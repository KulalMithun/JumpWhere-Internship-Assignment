from typing import List
from django.shortcuts import get_object_or_404
from employees.models import Employee
from projects.models import Project


class ResumeService:
    @staticmethod
    def get_employee_resume(employee_id: int) -> dict:
        emp = get_object_or_404(Employee, pk=employee_id, is_deleted=False)
        projects = emp.projects.filter(is_deleted=False).order_by('-start_date')
        data = {
            'name': emp.name,
            'designation': emp.designation,
            'professional_summary': emp.professional_summary,
            'coding': list(emp.coding.filter(is_deleted=False).values_list('name', flat=True)),
            'tools': list(emp.tools.filter(is_deleted=False).values_list('name', flat=True)),
            'projects': [],
        }
        for p in projects:
            data['projects'].append({
                'name': p.name,
                'technologies': list(p.technologies.values_list('name', flat=True)),
                'tools': list(p.tools.values_list('name', flat=True)),
                'description': p.description,
                'role_responsibilities': p.role_responsibilities,
                'start_date': p.start_date,
                'end_date': p.end_date,
            })
        return data
