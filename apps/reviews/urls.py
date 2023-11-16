from django.urls import include, path
from rest_framework import routers
# from .views import ReviewViewSet
#
# router = routers.DefaultRouter()
# router.register('', ReviewViewSet, basename='Review')
#
# urlpatterns = [
#     path('', include(router.urls,)),
# ]
#

from .views import ReviewViewSet, ReviewCreate, ReviewDelete, ReviewUpdate, ReviewList, ReviewDetail

router = routers.DefaultRouter()
router.register('', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls,)),
    path('add/', ReviewCreate.as_view(), name="review-add"),
    path('<int:pk>/', ReviewDetail.as_view(), name="review-detail"),
    path('<int:pk>/update/', ReviewUpdate.as_view(), name="review-update"),
    path('<int:pk>/delete/', ReviewDelete.as_view(), name="review-delete"),
    path('', ReviewList.as_view(), name="review-list"),
]
