from django.db import models
from rest_framework.response import Response
from rest_framework import status


# ── Abstract base model ───────────────────────────────────────────────────────

class BaseModel(models.Model):
    """Shared timestamp fields for every model in the project."""
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ── Generic object-fetch helper ───────────────────────────────────────────────

def get_object_or_404_response(model, pk):
    """
    Return (instance, None) on success or (None, Response) on not found.
    Usage in views:
        obj, err = get_object_or_404_response(Vendor, pk)
        if err:
            return err
    """
    try:
        return model.objects.get(pk=pk), None
    except model.DoesNotExist:
        return None, Response(
            {"detail": f"{model.__name__} with id={pk} not found."},
            status=status.HTTP_404_NOT_FOUND,
        )


def success_response(data, status_code=status.HTTP_200_OK):
    return Response({"success": True, "data": data}, status=status_code)


def error_response(errors, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({"success": False, "errors": errors}, status=status_code)
