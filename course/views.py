from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Course
from .serializers import CourseSerializer
from utils import get_object_or_404_response, success_response, error_response


class CourseListCreateView(APIView):
    """Course list and create endpoint."""

    @swagger_auto_schema(
        operation_summary="List all courses",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by name or code", type=openapi.TYPE_STRING),
        ],
        responses={200: CourseSerializer(many=True)},
    )
    def get(self, request):
        items = Course.objects.all()
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            items = items.filter(is_active=is_active.lower() == 'true')
        search = request.query_params.get('search')
        if search:
            items = items.filter(name__icontains=search) | items.filter(code__icontains=search)
        serializer = CourseSerializer(items, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a course",
        request_body=CourseSerializer,
        responses={201: CourseSerializer, 400: "Validation error"},
    )
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status.HTTP_201_CREATED)
        return error_response(serializer.errors)


class CourseDetailView(APIView):
    """Retrieve, update, or delete a course by ID."""

    @swagger_auto_schema(
        operation_summary="Retrieve a course",
        responses={200: CourseSerializer, 404: "Not found"},
    )
    def get(self, request, pk):
        obj, err = get_object_or_404_response(Course, pk)
        if err:
            return err
        return success_response(CourseSerializer(obj).data)

    @swagger_auto_schema(
        operation_summary="Update a course (full)",
        request_body=CourseSerializer,
        responses={200: CourseSerializer, 400: "Validation error", 404: "Not found"},
    )
    def put(self, request, pk):
        obj, err = get_object_or_404_response(Course, pk)
        if err:
            return err
        serializer = CourseSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Partial update a course",
        request_body=CourseSerializer,
        responses={200: CourseSerializer, 400: "Validation error", 404: "Not found"},
    )
    def patch(self, request, pk):
        obj, err = get_object_or_404_response(Course, pk)
        if err:
            return err
        serializer = CourseSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Soft-delete a course",
        responses={200: "Deleted (soft)", 404: "Not found"},
    )
    def delete(self, request, pk):
        obj, err = get_object_or_404_response(Course, pk)
        if err:
            return err
        obj.is_active = False
        obj.save()
        return success_response({"detail": f"Course {pk} deactivated (soft delete)."})
