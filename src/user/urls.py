from rest_framework.routers import SimpleRouter

from .views import *


router = SimpleRouter()
router.register('users', UserViewSet, basename='user')
router.register('user_addresses', UserAddressViewSet, basename='user_address')
