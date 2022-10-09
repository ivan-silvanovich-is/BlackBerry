from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('user_addresses', UserAddressViewSet, basename='user_address')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]
