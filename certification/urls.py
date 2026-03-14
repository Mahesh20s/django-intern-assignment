from django.urls import path
from .views import CertificationListCreateView, CertificationDetailView

urlpatterns = [
    path('certifications/', CertificationListCreateView.as_view(), name='certification-list-create'),
    path('certifications/<int:pk>/', CertificationDetailView.as_view(), name='certification-detail'),
]
