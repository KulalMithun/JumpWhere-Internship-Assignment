from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_deleted')
    search_fields = ('name',)
    list_filter = ('status',)
