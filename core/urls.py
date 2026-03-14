from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Modular Entity & Mapping API",
        default_version='v1',
        description="Django REST Framework backend for managing Vendors, Products, Courses, Certifications and their mappings.",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', RedirectView.as_view(url='/swagger/', permanent=False)),
    path('admin/', admin.site.urls),

    # Swagger / ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # Master entity APIs
    path('api/', include('vendor.urls')),
    path('api/', include('product.urls')),
    path('api/', include('course.urls')),
    path('api/', include('certification.urls')),

    # Mapping APIs
    path('api/', include('vendor_product_mapping.urls')),
    path('api/', include('product_course_mapping.urls')),
    path('api/', include('course_certification_mapping.urls')),
]
