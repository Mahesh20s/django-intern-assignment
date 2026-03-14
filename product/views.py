from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Product
from .serializers import ProductSerializer
from utils import get_object_or_404_response, success_response, error_response


class ProductListCreateView(APIView):
    """Product list and create endpoint."""

    @swagger_auto_schema(
        operation_summary="List all products",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by name or code", type=openapi.TYPE_STRING),
        ],
        responses={200: ProductSerializer(many=True)},
    )
    def get(self, request):
        items = Product.objects.all()
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            items = items.filter(is_active=is_active.lower() == 'true')
        search = request.query_params.get('search')
        if search:
            items = items.filter(name__icontains=search) | items.filter(code__icontains=search)
        serializer = ProductSerializer(items, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a product",
        request_body=ProductSerializer,
        responses={201: ProductSerializer, 400: "Validation error"},
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status.HTTP_201_CREATED)
        return error_response(serializer.errors)


class ProductDetailView(APIView):
    """Retrieve, update, or delete a product by ID."""

    @swagger_auto_schema(
        operation_summary="Retrieve a product",
        responses={200: ProductSerializer, 404: "Not found"},
    )
    def get(self, request, pk):
        obj, err = get_object_or_404_response(Product, pk)
        if err:
            return err
        return success_response(ProductSerializer(obj).data)

    @swagger_auto_schema(
        operation_summary="Update a product (full)",
        request_body=ProductSerializer,
        responses={200: ProductSerializer, 400: "Validation error", 404: "Not found"},
    )
    def put(self, request, pk):
        obj, err = get_object_or_404_response(Product, pk)
        if err:
            return err
        serializer = ProductSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Partial update a product",
        request_body=ProductSerializer,
        responses={200: ProductSerializer, 400: "Validation error", 404: "Not found"},
    )
    def patch(self, request, pk):
        obj, err = get_object_or_404_response(Product, pk)
        if err:
            return err
        serializer = ProductSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Soft-delete a product",
        responses={200: "Deleted (soft)", 404: "Not found"},
    )
    def delete(self, request, pk):
        obj, err = get_object_or_404_response(Product, pk)
        if err:
            return err
        obj.is_active = False
        obj.save()
        return success_response({"detail": f"Product {pk} deactivated (soft delete)."})
