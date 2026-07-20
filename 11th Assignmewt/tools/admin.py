from django.contrib import admin
from .models import Tool


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_deleted', 'created_at')
    search_fields = ('name',)
