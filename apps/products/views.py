from django.utils.translation import gettext_lazy as _
from django.db import transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from ..common.views import CustomModelViewSet


class ProductViewset(CustomModelViewSet):
    throttle_classes = [AnonRateThrottle]
    throttle_scope = "anon"
    permission_classes = [AllowAny]
    queryset = Product.objects.all().order_by("name")
    serializer_class = ProductSerializer
    http_method_names = [m for m in ModelViewSet.http_method_names if m != "patch"]
    search_fields = ["name", "sku"]
    ordering_fields = ["name", "sku"]
    filterset_fields = ["category", "stock_status"]


class ProductCategoryViewset(ModelViewSet):
    throttle_scope = "anon"
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = [
        m for m in ModelViewSet.http_method_names if m not in ["patch", "put"]
    ]
