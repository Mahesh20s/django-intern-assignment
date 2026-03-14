from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Vendor
from .serializers import VendorSerializer
from utils import get_object_or_404_response, success_response, error_response


class VendorListCreateView(APIView):
    """List all vendors or create a new vendor."""

    @swagger_auto_schema(
        operation_summary="List all vendors",
        operation_description="Returns a list of all vendors. Filter by is_active using ?is_active=true/false.",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by name or code", type=openapi.TYPE_STRING),
        ],
        responses={200: VendorSerializer(many=True)},
    )
    def get(self, request):
        vendors = Vendor.objects.all()

        is_active = request.query_params.get('is_active')
        if is_active is not None:
            vendors = vendors.filter(is_active=is_active.lower() == 'true')

        search = request.query_params.get('search')
        if search:
            vendors = vendors.filter(name__icontains=search) | vendors.filter(code__icontains=search)

        serializer = VendorSerializer(vendors, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a vendor",
        operation_description="Create a new vendor. Code must be unique.",
        request_body=VendorSerializer,
        responses={
            201: VendorSerializer,
            400: "Validation error",
        },
    )
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status.HTTP_201_CREATED)
        return error_response(serializer.errors)


class VendorDetailView(APIView):
    """Retrieve, update, or delete a vendor by ID."""

    @swagger_auto_schema(
        operation_summary="Retrieve a vendor",
        responses={200: VendorSerializer, 404: "Not found"},
    )
    def get(self, request, pk):
        vendor, err = get_object_or_404_response(Vendor, pk)
        if err:
            return err
        return success_response(VendorSerializer(vendor).data)

    @swagger_auto_schema(
        operation_summary="Update a vendor (full)",
        request_body=VendorSerializer,
        responses={200: VendorSerializer, 400: "Validation error", 404: "Not found"},
    )
    def put(self, request, pk):
        vendor, err = get_object_or_404_response(Vendor, pk)
        if err:
            return err
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Partial update a vendor",
        request_body=VendorSerializer,
        responses={200: VendorSerializer, 400: "Validation error", 404: "Not found"},
    )
    def patch(self, request, pk):
        vendor, err = get_object_or_404_response(Vendor, pk)
        if err:
            return err
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Soft-delete a vendor",
        responses={200: "Deleted (soft)", 404: "Not found"},
    )
    def delete(self, request, pk):
        vendor, err = get_object_or_404_response(Vendor, pk)
        if err:
            return err
        vendor.is_active = False
        vendor.save()
        return success_response({"detail": f"Vendor {pk} deactivated (soft delete)."})
