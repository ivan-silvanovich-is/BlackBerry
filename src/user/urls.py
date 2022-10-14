from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('user_addresses', UserAddressViewSet, basename='user_address')

urlpatterns = router.urls
