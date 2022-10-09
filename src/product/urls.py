from rest_framework.routers import SimpleRouter

from .views import *

# TODO: find a more beautiful way to add routes


router = SimpleRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='product')
router.register('manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register('materials', MaterialViewSet, basename='material')
router.register('colors', ColorViewSet, basename='color')
router.register('sizes', SizeViewSet, basename='size')
router.register('images', ImageViewSet, basename='image')
router.register('reviews', ReviewViewSet, basename='review')
router.register('coupons', CouponViewSet, basename='coupon')
