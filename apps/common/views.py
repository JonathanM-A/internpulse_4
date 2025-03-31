from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet
from django.http import Http404


class CustomModelViewSet(ModelViewSet):
    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound(self.get_not_found_response())

    def get_not_found_response(self):
        return {
            "status": "error",
            "code": 404,
            "message": f"{self.queryset.model._meta.verbose_name} not found",
            "errors": {
                "details": f"Invalid {self.queryset.model._meta.verbose_name} ID"
            },
        }
