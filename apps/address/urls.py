from django.urls import include, path
from rest_framework import routers
from .views import AddressViewSet

router = routers.DefaultRouter()
router.register('', AddressViewSet, basename='Address')

urlpatterns = [
    path('', include(router.urls,)),
]

