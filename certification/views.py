from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Certification
from .serializers import CertificationSerializer
from utils import get_object_or_404_response, success_response, error_response


class CertificationListCreateView(APIView):
    """Certification list and create endpoint."""

    @swagger_auto_schema(
        operation_summary="List all certifications",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search by name or code", type=openapi.TYPE_STRING),
        ],
        responses={200: CertificationSerializer(many=True)},
    )
    def get(self, request):
        items = Certification.objects.all()
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            items = items.filter(is_active=is_active.lower() == 'true')
        search = request.query_params.get('search')
        if search:
            items = items.filter(name__icontains=search) | items.filter(code__icontains=search)
        serializer = CertificationSerializer(items, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a certification",
        request_body=CertificationSerializer,
        responses={201: CertificationSerializer, 400: "Validation error"},
    )
    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status.HTTP_201_CREATED)
        return error_response(serializer.errors)


class CertificationDetailView(APIView):
    """Retrieve, update, or delete a certification by ID."""

    @swagger_auto_schema(
        operation_summary="Retrieve a certification",
        responses={200: CertificationSerializer, 404: "Not found"},
    )
    def get(self, request, pk):
        obj, err = get_object_or_404_response(Certification, pk)
        if err:
            return err
        return success_response(CertificationSerializer(obj).data)

    @swagger_auto_schema(
        operation_summary="Update a certification (full)",
        request_body=CertificationSerializer,
        responses={200: CertificationSerializer, 400: "Validation error", 404: "Not found"},
    )
    def put(self, request, pk):
        obj, err = get_object_or_404_response(Certification, pk)
        if err:
            return err
        serializer = CertificationSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Partial update a certification",
        request_body=CertificationSerializer,
        responses={200: CertificationSerializer, 400: "Validation error", 404: "Not found"},
    )
    def patch(self, request, pk):
        obj, err = get_object_or_404_response(Certification, pk)
        if err:
            return err
        serializer = CertificationSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Soft-delete a certification",
        responses={200: "Deleted (soft)", 404: "Not found"},
    )
    def delete(self, request, pk):
        obj, err = get_object_or_404_response(Certification, pk)
        if err:
            return err
        obj.is_active = False
        obj.save()
        return success_response({"detail": f"Certification {pk} deactivated (soft delete)."})
