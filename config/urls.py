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
import os

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


API_PREFIX = os.getenv('API_PREFIX')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_PREFIX + 'auth/basic/', include('rest_framework.urls')),
    path(API_PREFIX + 'auth/', include('djoser.urls.authtoken')),
    path(API_PREFIX + 'orders/', include(('apps.orders.urls', 'apps.orders'))),
    path(API_PREFIX + 'products/', include(('apps.products.urls', 'apps.products'))),
    path(API_PREFIX + 'users/', include(('apps.users.urls', 'apps.users'))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
