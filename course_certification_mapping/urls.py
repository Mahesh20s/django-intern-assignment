from django.urls import path
from .views import CourseCertificationMappingListCreateView, CourseCertificationMappingDetailView

urlpatterns = [
    path('course-certification-mappings/', CourseCertificationMappingListCreateView.as_view(), name='course-certification-mapping-list-create'),
    path('course-certification-mappings/<int:pk>/', CourseCertificationMappingDetailView.as_view(), name='course-certification-mapping-detail'),
]
