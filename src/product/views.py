from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from config.permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly, IsOwnerOrIsStaff
from .filters.staff_filters import *
from .filters.user_filters import *
from .models import *
from .serializers.staff_serializers import *
from .serializers.user_serializers import *

__all__ = (
    'CategoryViewSet',
    'ProductViewSet',
    'ProductDetailsViewSet',
    'ManufacturerViewSet',
    'MaterialViewSet',
    'ProductMaterialViewSet',
    'ColorViewSet',
    'SizeViewSet',
    'ImageViewSet',
    'ReviewViewSet',
    'CouponViewSet',
)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.select_related('parent_category').all()
    permission_classes = (IsStaffOrReadOnly, )
    filterset_class = CategoryFilter
    staff_filterset_class = StaffCategoryFilter
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StaffCategorySerializer
        else:
            return CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    permission_classes = (IsStaffOrReadOnly, )
    filterset_class = ProductFilter
    staff_filterset_class = StaffProductFilter
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.user.is_staff and self.action == 'list':
            return StaffProductListSerializer
        elif self.request.user.is_staff:
            return StaffProductItemSerializer
        elif self.action == 'list':
            return ProductListSerializer
        else:
            return ProductItemSerializer


class ProductDetailsViewSet(ModelViewSet):
    queryset = ProductDetails.objects.all()
    serializer_class = StaffProductDetailsSerializer
    permission_classes = (IsAdminUser, )
    filterset_class = StaffProductDetailsFilter


class ManufacturerViewSet(ModelViewSet):
    queryset = Manufacturer.objects.all()
    permission_classes = (IsStaffOrReadOnly, )
    filterset_class = ManufacturerFilter
    staff_filterset_class = StaffManufacturerFilter
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StaffManufacturerSerializer
        else:
            return ManufacturerSerializer


class MaterialViewSet(ModelViewSet):
    queryset = Material.objects.all()
    permission_classes = (IsStaffOrReadOnly,)
    staff_filterset_class = StaffMaterialFilter
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StaffMaterialSerializer
        else:
            return MaterialSerializer
    
    
class ProductMaterialViewSet(ModelViewSet):
    queryset = ProductMaterial.objects.all()
    permission_classes = (IsStaffOrReadOnly,)
    filterset_class = ProductMaterialFilter
    staff_filterset_class = StaffProductMaterialFilter

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StaffProductMaterialSerializer
        else:
            return ProductMaterialSerializer


class ColorViewSet(ModelViewSet):
    queryset = Color.objects.all()
    permission_classes = (IsStaffOrReadOnly,)
    staff_filterset_class = StaffColorFilter
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StaffColorSerializer
        else:
            return ColorSerializer


class SizeViewSet(ModelViewSet):
    queryset = Size.objects.all()
    permission_classes = (IsStaffOrReadOnly,)
    staff_filterset_class = StaffSizeFilter
    lookup_field = 'name'

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StaffSizeSerializer
        else:
            return SizeSerializer


class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    permission_classes = (IsStaffOrReadOnly, )
    filterset_class = ImageFilter
    staff_filterset_class = StaffImageFilter

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StaffImageSerializer
        else:
            return ImageSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    filterset_class = ReviewFilter
    staff_filterset_class = StaffReviewFilter

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StaffReviewSerializer
        else:
            return ReviewSerializer


class CouponViewSet(ModelViewSet):
    queryset = Coupon.objects.all()
    staff_filterset_class = StaffCouponFilter
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StaffCouponSerializer
        else:
            return CouponSerializer

    def get_permissions(self):
        if self.action == 'list':
            return IsAuthenticated(),
        elif self.action == 'retrieve':
            return IsOwnerOrIsStaff(),
        else:
            return IsStaffOrReadOnly(),

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        elif self.action == 'list':
            return self.queryset.filter(user=self.request.user.id, is_active=True)
        else:
            return self.queryset.filter(is_active=True)
