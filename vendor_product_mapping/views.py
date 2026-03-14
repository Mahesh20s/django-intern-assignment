from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer
from utils import get_object_or_404_response, success_response, error_response


class VendorProductMappingListCreateView(APIView):
    """List and create Vendor→Product mappings."""

    @swagger_auto_schema(
        operation_summary="List vendor-product mappings",
        operation_description="Filter by vendor_id or product_id using query params.",
        manual_parameters=[
            openapi.Parameter('vendor_id', openapi.IN_QUERY, description="Filter by vendor ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('product_id', openapi.IN_QUERY, description="Filter by product ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('primary_mapping', openapi.IN_QUERY, description="Filter primary mappings only", type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: VendorProductMappingSerializer(many=True)},
    )
    def get(self, request):
        qs = VendorProductMapping.objects.all()
        vendor_id = request.query_params.get('vendor_id')
        product_id = request.query_params.get('product_id')
        is_active = request.query_params.get('is_active')
        primary_mapping = request.query_params.get('primary_mapping')

        if vendor_id:
            qs = qs.filter(vendor_id=vendor_id)
        if product_id:
            qs = qs.filter(product_id=product_id)
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        if primary_mapping is not None:
            qs = qs.filter(primary_mapping=primary_mapping.lower() == 'true')

        serializer = VendorProductMappingSerializer(qs, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a vendor-product mapping",
        request_body=VendorProductMappingSerializer,
        responses={201: VendorProductMappingSerializer, 400: "Validation error"},
    )
    def post(self, request):
        serializer = VendorProductMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status.HTTP_201_CREATED)
        return error_response(serializer.errors)


class VendorProductMappingDetailView(APIView):
    """Retrieve, update, or delete a Vendor→Product mapping by ID."""

    @swagger_auto_schema(
        operation_summary="Retrieve a vendor-product mapping",
        responses={200: VendorProductMappingSerializer, 404: "Not found"},
    )
    def get(self, request, pk):
        obj, err = get_object_or_404_response(VendorProductMapping, pk)
        if err:
            return err
        return success_response(VendorProductMappingSerializer(obj).data)

    @swagger_auto_schema(
        operation_summary="Update a vendor-product mapping (full)",
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer, 400: "Validation error", 404: "Not found"},
    )
    def put(self, request, pk):
        obj, err = get_object_or_404_response(VendorProductMapping, pk)
        if err:
            return err
        serializer = VendorProductMappingSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Partial update a vendor-product mapping",
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer, 400: "Validation error", 404: "Not found"},
    )
    def patch(self, request, pk):
        obj, err = get_object_or_404_response(VendorProductMapping, pk)
        if err:
            return err
        serializer = VendorProductMappingSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Soft-delete a vendor-product mapping",
        responses={200: "Deleted (soft)", 404: "Not found"},
    )
    def delete(self, request, pk):
        obj, err = get_object_or_404_response(VendorProductMapping, pk)
        if err:
            return err
        obj.is_active = False
        obj.save()
        return success_response({"detail": f"VendorProductMapping {pk} deactivated."})
