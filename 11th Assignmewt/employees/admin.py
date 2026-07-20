from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'status', 'is_deleted')
    search_fields = ('name', 'designation')
    list_filter = ('status',)
