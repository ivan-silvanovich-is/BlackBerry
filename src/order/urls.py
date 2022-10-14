from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register('orders', OrderViewSet, basename='order')
router.register('deliverers', DelivererViewSet, basename='deliverer')
router.register('points', PointViewSet, basename='point')

urlpatterns = router.urls
