from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor


class VendorSerializerTest(TestCase):
    def test_valid_vendor_creation(self):
        from .serializers import VendorSerializer
        data = {'name': 'Test Vendor', 'code': 'TST001', 'description': 'Test'}
        serializer = VendorSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_duplicate_code_rejected(self):
        from .serializers import VendorSerializer
        Vendor.objects.create(name='Existing', code='DUP001')
        data = {'name': 'New Vendor', 'code': 'DUP001'}
        serializer = VendorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('code', serializer.errors)

    def test_blank_name_rejected(self):
        from .serializers import VendorSerializer
        data = {'name': '   ', 'code': 'BLK001'}
        serializer = VendorSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class VendorAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name='Alpha', code='ALP001', description='Alpha vendor')

    def test_list_vendors(self):
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])

    def test_create_vendor(self):
        response = self.client.post('/api/vendors/', {'name': 'Beta', 'code': 'BET001'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_vendor(self):
        response = self.client.get(f'/api/vendors/{self.vendor.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['code'], 'ALP001')

    def test_update_vendor(self):
        response = self.client.put(
            f'/api/vendors/{self.vendor.pk}/',
            {'name': 'Alpha Updated', 'code': 'ALP001'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_vendor(self):
        response = self.client.patch(
            f'/api/vendors/{self.vendor.pk}/',
            {'name': 'Alpha Patched'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_soft_delete_vendor(self):
        response = self.client.delete(f'/api/vendors/{self.vendor.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertFalse(self.vendor.is_active)

    def test_vendor_not_found(self):
        response = self.client.get('/api/vendors/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_by_is_active(self):
        response = self.client.get('/api/vendors/?is_active=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
