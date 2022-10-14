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


api_prefix = 'api/v1/'
urlpatterns = [
    path('admin/', admin.site.urls),
    path(api_prefix + 'auth/drf/', include(('rest_framework.urls', 'rest_framework'))),
    path(api_prefix + 'auth/', include(('djoser.urls', 'djoser'))),
    path(api_prefix + 'auth/', include(('djoser.urls.authtoken', 'djoser.urls.authtoken'))),
    path(api_prefix + 'order/', include(('order.urls', 'order'))),
    path(api_prefix + 'product/', include(('product.urls', 'product'))),
    path(api_prefix + 'user/', include(('user.urls', 'user'))),
]
