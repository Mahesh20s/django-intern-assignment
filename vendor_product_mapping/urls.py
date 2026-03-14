from django.urls import path
from .views import VendorProductMappingListCreateView, VendorProductMappingDetailView

urlpatterns = [
    path('vendor-product-mappings/', VendorProductMappingListCreateView.as_view(), name='vendor-product-mapping-list-create'),
    path('vendor-product-mappings/<int:pk>/', VendorProductMappingDetailView.as_view(), name='vendor-product-mapping-detail'),
]
