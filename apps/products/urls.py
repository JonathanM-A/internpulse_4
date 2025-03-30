from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductViewset, ProductCategoryViewset

router = DefaultRouter()
router.register(r"products", ProductViewset, basename="products")
router.register(
    r"categories", ProductCategoryViewset, basename="categories"
)

urlpatterns = [path("", include(router.urls))]
