from rest_framework.routers import SimpleRouter

from .views import *

# TODO: find a more beautiful way to add routes


router = SimpleRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='product')
router.register('manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register('materials', ProductMaterialViewSet, basename='material')
router.register('colors', ProductColorViewSet, basename='color')
router.register('sizes', ProductSizeViewSet, basename='size')
router.register('images', ProductImageViewSet, basename='image')
router.register('reviews', ReviewViewSet, basename='review')
router.register('coupons', CouponViewSet, basename='coupon')
