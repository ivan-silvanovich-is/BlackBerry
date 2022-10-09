"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from .routers import DefaultRouter
from order.urls import router as order_router
from product.urls import router as product_router
from user.urls import router as user_router


router = DefaultRouter()
router.extend(order_router)
router.extend(product_router)
router.extend(user_router)

api_prefix = 'api/v1/'
urlpatterns = [
    path('admin/', admin.site.urls),
    path(api_prefix + 'auth/', include('djoser.urls')),
    path(api_prefix + 'auth/', include('djoser.urls.authtoken')),
    path(api_prefix + 'auth/', include('rest_framework.urls')),
    path(api_prefix, include(router.urls)),
]
