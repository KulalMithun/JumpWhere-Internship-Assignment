from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from coding.models import Coding
from tools.models import Tool
from employees.models import Employee
from projects.models import Project


@login_required
def dashboard(request):
    stats = {
        'total_employees': Employee.objects.filter(is_deleted=False).count(),
        'total_projects': Project.objects.filter(is_deleted=False).count(),
        'total_coding': Coding.objects.filter(is_deleted=False).count(),
        'total_tools': Tool.objects.filter(is_deleted=False).count(),
    }
    return render(request, 'core/dashboard.html', {'stats': stats})
