from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer
from utils import get_object_or_404_response, success_response, error_response


class CourseCertificationMappingListCreateView(APIView):
    """List and create Course→Certification mappings."""

    @swagger_auto_schema(
        operation_summary="List course-certification mappings",
        operation_description="Filter by course_id or certification_id using query params.",
        manual_parameters=[
            openapi.Parameter('course_id', openapi.IN_QUERY, description="Filter by course ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('certification_id', openapi.IN_QUERY, description="Filter by certification ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('primary_mapping', openapi.IN_QUERY, description="Filter primary mappings only", type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: CourseCertificationMappingSerializer(many=True)},
    )
    def get(self, request):
        qs = CourseCertificationMapping.objects.all()
        course_id = request.query_params.get('course_id')
        certification_id = request.query_params.get('certification_id')
        is_active = request.query_params.get('is_active')
        primary_mapping = request.query_params.get('primary_mapping')

        if course_id:
            qs = qs.filter(course_id=course_id)
        if certification_id:
            qs = qs.filter(certification_id=certification_id)
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        if primary_mapping is not None:
            qs = qs.filter(primary_mapping=primary_mapping.lower() == 'true')

        serializer = CourseCertificationMappingSerializer(qs, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a course-certification mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={201: CourseCertificationMappingSerializer, 400: "Validation error"},
    )
    def post(self, request):
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status.HTTP_201_CREATED)
        return error_response(serializer.errors)


class CourseCertificationMappingDetailView(APIView):
    """Retrieve, update, or delete a Course→Certification mapping."""

    @swagger_auto_schema(
        operation_summary="Retrieve a course-certification mapping",
        responses={200: CourseCertificationMappingSerializer, 404: "Not found"},
    )
    def get(self, request, pk):
        obj, err = get_object_or_404_response(CourseCertificationMapping, pk)
        if err:
            return err
        return success_response(CourseCertificationMappingSerializer(obj).data)

    @swagger_auto_schema(
        operation_summary="Update a course-certification mapping (full)",
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer, 400: "Validation error", 404: "Not found"},
    )
    def put(self, request, pk):
        obj, err = get_object_or_404_response(CourseCertificationMapping, pk)
        if err:
            return err
        serializer = CourseCertificationMappingSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Partial update a course-certification mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer, 400: "Validation error", 404: "Not found"},
    )
    def patch(self, request, pk):
        obj, err = get_object_or_404_response(CourseCertificationMapping, pk)
        if err:
            return err
        serializer = CourseCertificationMappingSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Soft-delete a course-certification mapping",
        responses={200: "Deleted (soft)", 404: "Not found"},
    )
    def delete(self, request, pk):
        obj, err = get_object_or_404_response(CourseCertificationMapping, pk)
        if err:
            return err
        obj.is_active = False
        obj.save()
        return success_response({"detail": f"CourseCertificationMapping {pk} deactivated."})
