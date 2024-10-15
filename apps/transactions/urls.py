from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TransactionViewSet

app_name = 'transactions'

router = DefaultRouter()
router.register(r'', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
