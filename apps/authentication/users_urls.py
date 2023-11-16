from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, UserProfile

router = routers.DefaultRouter()
router.register('', UserViewSet)
# router.register('profile', ProfileAPIView)


urlpatterns = [
    path('', include(router.urls,)),
    # path("profile/<int:pk>/", ProfileAPIView.as_view()),
]
