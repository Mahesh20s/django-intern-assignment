from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer
from utils import get_object_or_404_response, success_response, error_response


class ProductCourseMappingListCreateView(APIView):
    """List and create Product→Course mappings."""

    @swagger_auto_schema(
        operation_summary="List product-course mappings",
        operation_description="Filter by product_id or course_id using query params.",
        manual_parameters=[
            openapi.Parameter('product_id', openapi.IN_QUERY, description="Filter by product ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('course_id', openapi.IN_QUERY, description="Filter by course ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('primary_mapping', openapi.IN_QUERY, description="Filter primary mappings only", type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: ProductCourseMappingSerializer(many=True)},
    )
    def get(self, request):
        qs = ProductCourseMapping.objects.all()
        product_id = request.query_params.get('product_id')
        course_id = request.query_params.get('course_id')
        is_active = request.query_params.get('is_active')
        primary_mapping = request.query_params.get('primary_mapping')

        if product_id:
            qs = qs.filter(product_id=product_id)
        if course_id:
            qs = qs.filter(course_id=course_id)
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        if primary_mapping is not None:
            qs = qs.filter(primary_mapping=primary_mapping.lower() == 'true')

        serializer = ProductCourseMappingSerializer(qs, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a product-course mapping",
        request_body=ProductCourseMappingSerializer,
        responses={201: ProductCourseMappingSerializer, 400: "Validation error"},
    )
    def post(self, request):
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status.HTTP_201_CREATED)
        return error_response(serializer.errors)


class ProductCourseMappingDetailView(APIView):
    """Retrieve, update, or delete a Product→Course mapping."""

    @swagger_auto_schema(
        operation_summary="Retrieve a product-course mapping",
        responses={200: ProductCourseMappingSerializer, 404: "Not found"},
    )
    def get(self, request, pk):
        obj, err = get_object_or_404_response(ProductCourseMapping, pk)
        if err:
            return err
        return success_response(ProductCourseMappingSerializer(obj).data)

    @swagger_auto_schema(
        operation_summary="Update a product-course mapping (full)",
        request_body=ProductCourseMappingSerializer,
        responses={200: ProductCourseMappingSerializer, 400: "Validation error", 404: "Not found"},
    )
    def put(self, request, pk):
        obj, err = get_object_or_404_response(ProductCourseMapping, pk)
        if err:
            return err
        serializer = ProductCourseMappingSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Partial update a product-course mapping",
        request_body=ProductCourseMappingSerializer,
        responses={200: ProductCourseMappingSerializer, 400: "Validation error", 404: "Not found"},
    )
    def patch(self, request, pk):
        obj, err = get_object_or_404_response(ProductCourseMapping, pk)
        if err:
            return err
        serializer = ProductCourseMappingSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Soft-delete a product-course mapping",
        responses={200: "Deleted (soft)", 404: "Not found"},
    )
    def delete(self, request, pk):
        obj, err = get_object_or_404_response(ProductCourseMapping, pk)
        if err:
            return err
        obj.is_active = False
        obj.save()
        return success_response({"detail": f"ProductCourseMapping {pk} deactivated."})
