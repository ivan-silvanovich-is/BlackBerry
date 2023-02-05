from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register('deliverers', DelivererViewSet, basename='deliverer')
router.register('points', PointViewSet, basename='point')
router.register('', OrderViewSet, basename='order')

urlpatterns = router.urls
