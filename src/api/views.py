from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from .filters import *
from .models import *
from .permissions import IsOwner, IsOwnerOrReadOnly
from .serializers import *
from user.models import User, UserAddress

__all__ = (
    'CategoryViewSet',
    'ProductViewSet',
    'ManufacturerViewSet',
    'ProductMaterialViewSet',
    'ProductColorViewSet',
    'ProductSizeViewSet',
    'ProductImageViewSet',
    'ReviewViewSet',
    'CouponViewSet',
    'OrderViewSet',
    'DelivererViewSet',
    'PointViewSet',
    'UserViewSet',
    'UserAddressViewSet',
)


# TODO: find way to disable filters in retrieve view


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.select_related('parent_category').all()
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter
    lookup_field = "slug"


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductItemSerializer
    filterset_class = ProductFilter
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        else:
            return self.serializer_class


class ManufacturerViewSet(ReadOnlyModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    filterset_class = ManufacturerFilter
    lookup_field = "slug"


class ProductMaterialViewSet(ReadOnlyModelViewSet):
    queryset = ProductMaterialProduct.objects.all()
    serializer_class = ProductMaterialProductSerializer
    filterset_class = ProductMaterialFilter
    lookup_field = "slug"

    def list(self, request, *args, **kwargs):
        if any(self.request.query_params.values()):
            filtered_qs = self.filterset_class(data=self.request.query_params, queryset=self.queryset).qs
            serializer = self.serializer_class(filtered_qs, many=True)
            return Response(serializer.data)

        return Response(ProductMaterialSerializer(instance=ProductMaterial.objects.all(), many=True).data)

    def retrieve(self, request, *args, **kwargs):
        material = get_object_or_404(ProductMaterial, slug=kwargs['slug'])
        return Response(ProductMaterialSerializer(instance=material).data)


class ProductColorViewSet(ReadOnlyModelViewSet):
    queryset = ProductColor.objects.all()
    serializer_class = ProductColorSerializer
    lookup_field = 'slug'


class ProductSizeViewSet(ReadOnlyModelViewSet):
    queryset = ProductSize.objects.all()
    serializer_class = ProductSizeSerializer
    lookup_field = 'name'


class ProductImageViewSet(ReadOnlyModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    filterset_class = ProductImageFilter


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


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(user=self.request.user.id)
        else:
            return self.queryset


class DelivererViewSet(ReadOnlyModelViewSet):
    queryset = Deliverer.objects.all()
    serializer_class = DelivererSerializer
    lookup_field = 'slug'


class PointViewSet(ReadOnlyModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class UserAddressViewSet(ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = (IsOwner, )

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(user=self.request.user.id)
        else:
            return self.queryset
