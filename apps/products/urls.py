from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register('products_details', ProductDetailsViewSet, basename='product_details')
router.register('categories', CategoryViewSet, basename='category')
router.register('manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register('materials', MaterialViewSet, basename='material')
router.register('products_materials', ProductMaterialViewSet, basename='product_material')
router.register('colors', ColorViewSet, basename='color')
router.register('sizes', SizeViewSet, basename='size')
router.register('images', ImageViewSet, basename='image')
router.register('reviews', ReviewViewSet, basename='review')
router.register('coupons', CouponViewSet, basename='coupon')
router.register('', ProductViewSet, basename='product')

urlpatterns = router.urls
