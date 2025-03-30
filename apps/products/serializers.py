from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["id", "created_at", "modified_at"]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source="category", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["sku", "id", "created_at", "modified_at", "category_name"]

    def to_representation(self, instance):
        instance_rep = super().to_representation(instance)
        if instance_rep["stock_status"]:
            instance_rep["stock_status"] = _("In Stock")
        else:
            instance_rep["stock_status"] = _("Out of Stock")
        return instance_rep
