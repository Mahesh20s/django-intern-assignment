from django.core.management.base import BaseCommand
from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certification.models import Certification
from vendor_product_mapping.models import VendorProductMapping
from product_course_mapping.models import ProductCourseMapping
from course_certification_mapping.models import CourseCertificationMapping


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Vendors
        v1, _ = Vendor.objects.get_or_create(code='VND001', defaults={'name': 'Alpha Vendor', 'description': 'First vendor'})
        v2, _ = Vendor.objects.get_or_create(code='VND002', defaults={'name': 'Beta Vendor', 'description': 'Second vendor'})

        # Products
        p1, _ = Product.objects.get_or_create(code='PRD001', defaults={'name': 'Product Alpha', 'description': 'Core product'})
        p2, _ = Product.objects.get_or_create(code='PRD002', defaults={'name': 'Product Beta', 'description': 'Secondary product'})

        # Courses
        c1, _ = Course.objects.get_or_create(code='CRS001', defaults={'name': 'Intro to Django', 'description': 'Django basics'})
        c2, _ = Course.objects.get_or_create(code='CRS002', defaults={'name': 'Advanced DRF', 'description': 'DRF deep dive'})

        # Certifications
        cert1, _ = Certification.objects.get_or_create(code='CERT001', defaults={'name': 'Django Developer', 'description': 'Certified Django Developer'})
        cert2, _ = Certification.objects.get_or_create(code='CERT002', defaults={'name': 'DRF Expert', 'description': 'Certified DRF Expert'})

        # Vendor → Product mappings
        VendorProductMapping.objects.get_or_create(vendor=v1, product=p1, defaults={'primary_mapping': True})
        VendorProductMapping.objects.get_or_create(vendor=v1, product=p2, defaults={'primary_mapping': False})
        VendorProductMapping.objects.get_or_create(vendor=v2, product=p1, defaults={'primary_mapping': True})

        # Product → Course mappings
        ProductCourseMapping.objects.get_or_create(product=p1, course=c1, defaults={'primary_mapping': True})
        ProductCourseMapping.objects.get_or_create(product=p1, course=c2, defaults={'primary_mapping': False})
        ProductCourseMapping.objects.get_or_create(product=p2, course=c2, defaults={'primary_mapping': True})

        # Course → Certification mappings
        CourseCertificationMapping.objects.get_or_create(course=c1, certification=cert1, defaults={'primary_mapping': True})
        CourseCertificationMapping.objects.get_or_create(course=c2, certification=cert2, defaults={'primary_mapping': True})

        self.stdout.write(self.style.SUCCESS('Seed data created successfully!'))
        self.stdout.write(f'  Vendors: {Vendor.objects.count()}')
        self.stdout.write(f'  Products: {Product.objects.count()}')
        self.stdout.write(f'  Courses: {Course.objects.count()}')
        self.stdout.write(f'  Certifications: {Certification.objects.count()}')
        self.stdout.write(f'  VendorProductMappings: {VendorProductMapping.objects.count()}')
        self.stdout.write(f'  ProductCourseMappings: {ProductCourseMapping.objects.count()}')
        self.stdout.write(f'  CourseCertificationMappings: {CourseCertificationMapping.objects.count()}')
