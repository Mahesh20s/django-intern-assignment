from django.contrib import admin
from .models import CourseCertificationMapping

@admin.register(CourseCertificationMapping)
class CourseCertificationMappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'course', 'certification', 'primary_mapping', 'is_active', 'created_at']
    list_filter = ['is_active', 'primary_mapping']
    search_fields = ['course__name', 'certification__name']
