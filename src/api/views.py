import re

from django.shortcuts import render
from django.db.models import Min, Max
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response

from .models import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import *


class ProductViewSet(ReadOnlyModelViewSet):
    serializer_class = ProductItemSerializer

    def material_filter(self, products_ids):
        materials_slugs = self.request.GET.getlist('material')

        if not materials_slugs:
            return products_ids

        materials_ids = ProductMaterial.objects.filter(slug__in=materials_slugs).values_list("pk", flat=True)

        return ProductMaterialProduct.objects.filter(
            product__in=products_ids,
            product_material__in=materials_ids
        ).values_list("product", flat=True)

    def color_filter(self, products_ids):
        colors_slugs = self.request.GET.getlist('color')

        if not colors_slugs:
            return products_ids

        colors_ids = ProductColor.objects.filter(slug__in=colors_slugs)
        return ProductDetails.objects.filter(
            product__in=products_ids,
            product_color__in=colors_ids
        ).values_list("product", flat=True)

    def size_filter(self, products_ids):
        sizes_names = self.request.GET.getlist('size')

        if not sizes_names:
            return products_ids

        sizes_ids = ProductSize.objects.filter(name__in=sizes_names)
        return ProductDetails.objects.filter(
            product__in=products_ids,
            product_size__in=sizes_ids
        ).values_list("product", flat=True)

    def price_filter(self, products_ids):
        min_price, max_price = self.request.GET.get('min_price'), self.request.GET.get('max_price')

        if not min_price and not max_price:
            return products_ids

        min_price = int(min_price) or Product.objects.aggregate(Min('price'))
        max_price = int(max_price) or Product.objects.aggregate(Max('price'))

        return Product.objects.filter(
            id__in=products_ids,
            price__range=(min_price, max_price)
        ).values_list("id", flat=True)

    def remain_filters(self, products_ids=None):
        filters = {
            "category": Category.objects.filter(
                slug=self.request.GET.get("category")
            ).values_list("id", flat=True).first(),
            "manufacturer": Manufacturer.objects.filter(
                slug=self.request.GET.get("manufacturer")
            ).values_list("id", flat=True).first(),
            "gender": self.request.GET.get("gender")
        }

        if products_ids:
            return Product.objects.filter(id__in=products_ids, **filters).values_list("id", flat=True)
        else:
            return Product.objects.filter(**filters).values_list("id", flat=True)

    def gender_filter(self, products_ids):
        gender = self.request.GET.get("gender")

        if gender not in ("m", "f"):
            return products_ids

        return Product.objects.filter(id__in=products_ids, gender=gender).values_list("id", flat=True)

    def category_filter(self, products_ids):
        category = self.request.GET.get("category")
        category = Category.objects.filter(slug=category).first()

        if not category:
            return products_ids

        return Product.objects.filter(id__in=products_ids, category=category).values_list("id", flat=True)

    def manufacturer_filter(self, products_ids):
        manufacturer = self.request.GET.get("manufacturer")
        manufacturer = Manufacturer.objects.filter(slug=manufacturer).first()

        if not manufacturer:
            return products_ids

        return Product.objects.filter(id__in=products_ids, manufacturer=manufacturer).values_list("id", flat=True)

    def get_queryset(self):
        filters = (
            self.category_filter,
            self.manufacturer_filter,
            self.price_filter,
            self.gender_filter,
            self.material_filter,
            self.color_filter,
            self.size_filter
        )

        product_ids = Product.objects.all().values_list("id", flat=True)
        for filter in filters:
            product_ids = filter(product_ids)

        return Product.objects.filter(id__in=product_ids)

    def list(self, request, *args, **kwargs):
        serializer = ProductListSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class ReviewViewSet(ModelViewSet):
    serializer_class = ProductReviewSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def filter(self, queryset):
        params = {
            "user": User.objects.filter(username=self.request.GET.get("user")).first(),
            "product": Product.objects.filter(slug=self.request.GET.get("product")).first(),
            "rating": self.request.GET.get("rating")
        }

        if not params["rating"].isdigit() or 0 > int(params["rating"]) > 10:
            params["rating"] = None

        for param in list(params):
            if params[param] is None:
                params.pop(param)

        return Review.objects.filter(**params)

    def get_queryset(self):
        return self.filter(Review.objects.all())

