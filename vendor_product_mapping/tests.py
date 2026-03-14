from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from vendor.models import Vendor
from product.models import Product
from .models import VendorProductMapping


class VendorProductMappingTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name='V1', code='V001')
        self.vendor2 = Vendor.objects.create(name='V2', code='V002')
        self.product = Product.objects.create(name='P1', code='P001')
        self.product2 = Product.objects.create(name='P2', code='P002')

    def test_create_mapping(self):
        response = self.client.post('/api/vendor-product-mappings/', {
            'vendor': self.vendor.pk,
            'product': self.product.pk,
            'primary_mapping': True
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_mapping_rejected(self):
        VendorProductMapping.objects.create(vendor=self.vendor, product=self.product)
        response = self.client.post('/api/vendor-product-mappings/', {
            'vendor': self.vendor.pk,
            'product': self.product.pk,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_two_primary_mappings_rejected(self):
        VendorProductMapping.objects.create(vendor=self.vendor, product=self.product, primary_mapping=True)
        response = self.client.post('/api/vendor-product-mappings/', {
            'vendor': self.vendor.pk,
            'product': self.product2.pk,
            'primary_mapping': True
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_different_vendor_can_have_own_primary(self):
        VendorProductMapping.objects.create(vendor=self.vendor, product=self.product, primary_mapping=True)
        response = self.client.post('/api/vendor-product-mappings/', {
            'vendor': self.vendor2.pk,
            'product': self.product.pk,
            'primary_mapping': True
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filter_by_vendor_id(self):
        VendorProductMapping.objects.create(vendor=self.vendor, product=self.product)
        response = self.client.get(f'/api/vendor-product-mappings/?vendor_id={self.vendor.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_soft_delete(self):
        m = VendorProductMapping.objects.create(vendor=self.vendor, product=self.product)
        response = self.client.delete(f'/api/vendor-product-mappings/{m.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        m.refresh_from_db()
        self.assertFalse(m.is_active)
