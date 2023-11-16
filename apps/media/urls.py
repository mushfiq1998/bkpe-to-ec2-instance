from django.urls import include, path
from rest_framework import routers
from .views import ImageViewSet

router = routers.DefaultRouter()
router.register('', ImageViewSet, basename='Image')

urlpatterns = [
    path('', include(router.urls,)),
]
