from rest_framework.routers import SimpleRouter

from .views import *


router = SimpleRouter()
router.register('addresses', AddressViewSet, basename='address')
router.register('', UserViewSet, basename='user')

urlpatterns = router.urls
