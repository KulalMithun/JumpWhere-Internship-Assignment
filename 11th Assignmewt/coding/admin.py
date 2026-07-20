from django.contrib import admin
from .models import Coding


@admin.register(Coding)
class CodingAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_deleted', 'created_at')
    search_fields = ('name',)
