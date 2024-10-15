"""
URL configuration for wallet_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

DEBUG = getattr(settings, 'DEBUG', True)


schema_view = get_schema_view(
    openapi.Info(
        title="Wallet API",
        default_version='v1',
        description="API documentation for Wallet and Transaction models",
        contact=openapi.Contact(email="iambrkkdn@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

app_name = 'Wallet'

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    # API
    re_path(r'^api/wallets/', include('apps.wallets.urls', namespace='wallets')),
    re_path(r'^api/transactions/', include('apps.transactions.urls', namespace='transactions')),
]

if DEBUG:
    urlpatterns += [
        # Docs
        re_path(r'^api/v1/docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        re_path(
            r'^api/v1/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'
        ),
        re_path(
            r'^api/v1/swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json',
        ),
    ]
