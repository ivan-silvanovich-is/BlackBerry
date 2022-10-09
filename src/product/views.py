from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from config.permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly
from .filters import *
from .models import *
from .serializers.staff_serializers import *
from .serializers.user_serializers import *

__all__ = (
    'CategoryViewSet',
    'ProductViewSet',
    'ManufacturerViewSet',
    'MaterialViewSet',
    'ColorViewSet',
    'SizeViewSet',
    'ImageViewSet',
    'ReviewViewSet',
    'CouponViewSet',
)


# TODO: find way to disable filters in retrieve view


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.select_related('parent_category').all()
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter
    lookup_field = "slug"


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    permission_classes = (IsStaffOrReadOnly, )
    filterset_class = ProductFilter
    lookup_field = 'slug'

    def get_queryset(self):
        if self.request.user.is_staff:
            self.filterset_class = StaffProductFilter
        return self.filterset_class(self.request.GET, queryset=self.queryset).qs

    def get_serializer_class(self):
        if self.request.user.is_staff and self.action == 'list':
            return StaffProductListSerializer
        elif self.request.user.is_staff:
            return StaffProductItemSerializer
        elif self.action == 'list':
            return ProductListSerializer
        else:
            return ProductItemSerializer


class ManufacturerViewSet(ReadOnlyModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    filterset_class = ManufacturerFilter
    lookup_field = "slug"


class MaterialViewSet(ReadOnlyModelViewSet):
    queryset = MaterialProduct.objects.all()
    serializer_class = MaterialProductSerializer
    filterset_class = MaterialFilter
    lookup_field = "slug"

    def list(self, request, *args, **kwargs):
        if any(self.request.query_params.values()):
            filtered_qs = self.filterset_class(data=self.request.query_params, queryset=self.queryset).qs
            serializer = self.serializer_class(filtered_qs, many=True)
            return Response(serializer.data)

        return Response(MaterialSerializer(instance=Material.objects.all(), many=True).data)

    def retrieve(self, request, *args, **kwargs):
        material = get_object_or_404(Material, slug=kwargs['slug'])
        return Response(MaterialSerializer(instance=material).data)


class ColorViewSet(ReadOnlyModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    lookup_field = 'slug'


class SizeViewSet(ReadOnlyModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    lookup_field = 'name'


class ImageViewSet(ReadOnlyModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filterset_class = ImageFilter


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    filterset_class = ReviewFilter


class CouponViewSet(ReadOnlyModelViewSet):
    queryset = Coupon.objects.filter(is_active=True)
    serializer_class = CouponSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return IsAuthenticated(),
        else:
            return AllowAny(),

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(user=self.request.user.id)
        elif self.action == 'retrieve':
            return self.queryset.filter(Q(user=self.request.user.id) | Q(user=None))
        else:
            return self.queryset
