from django.contrib import admin
from .models import ProductCourseMapping

@admin.register(ProductCourseMapping)
class ProductCourseMappingAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'course', 'primary_mapping', 'is_active', 'created_at']
    list_filter = ['is_active', 'primary_mapping']
    search_fields = ['product__name', 'course__name']
