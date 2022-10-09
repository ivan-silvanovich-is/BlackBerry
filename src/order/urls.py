from rest_framework.routers import SimpleRouter

from .views import *


router = SimpleRouter()
router.register('orders', OrderViewSet, basename='order')
router.register('deliverers', DelivererViewSet, basename='deliverer')
router.register('points', PointViewSet, basename='point')
