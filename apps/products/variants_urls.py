from django.urls import include, path
from rest_framework import routers

from .views import VariantViewSet

router = routers.DefaultRouter()
router.register('', VariantViewSet)

urlpatterns = [
    path('', include(router.urls,)),
]
