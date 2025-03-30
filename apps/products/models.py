from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

from apps.common.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=255, blank=False)
    abbreviation = models.CharField(max_length=3, blank=False)

    def __str__(self):
        return f"{self.name}"

class Product(BaseModel):

    name = models.CharField(max_length=255, blank=False, unique=True)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL, related_name="products"
    )
    sku = models.CharField(max_length=10, null=True, blank=False, unique=True)
    price = models.DecimalField(
        decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal("0.01"))]
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    stock_status = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.stock_status = bool(self.quantity)

        if not self.sku:
            base_sku = self.category.abbreviation
            sku = f"{base_sku}-{str(Product.objects.filter(category=self.category).count()+1).zfill(4)}"
            self.sku = sku.upper()

        super().save(*args, **kwargs)
