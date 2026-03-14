from django.urls import path
from .views import ProductCourseMappingListCreateView, ProductCourseMappingDetailView

urlpatterns = [
    path('product-course-mappings/', ProductCourseMappingListCreateView.as_view(), name='product-course-mapping-list-create'),
    path('product-course-mappings/<int:pk>/', ProductCourseMappingDetailView.as_view(), name='product-course-mapping-detail'),
]
