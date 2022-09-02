from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *


# TODO: find a more beautiful way to add routes


router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='product')
router.register('manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register('materials', ProductMaterialViewSet, basename='material')
router.register('colors', ProductColorViewSet, basename='color')
router.register('sizes', ProductSizeViewSet, basename='size')
router.register('images', ProductImageViewSet, basename='image')
router.register('reviews', ReviewViewSet, basename='review')
router.register('coupons', CouponViewSet, basename='coupon')
router.register('orders', OrderViewSet, basename='order')
router.register('deliverers', DelivererViewSet, basename='deliverer')
router.register('points', PointViewSet, basename='point')
router.register('users', UserViewSet, basename='user')
router.register('user_addresses', UserAddressViewSet, basename='user_address')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]
