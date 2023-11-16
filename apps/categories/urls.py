from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, CategoryCreate, CategoryDelete, CategoryUpdate, CategoryList, CategoryDetail

router = routers.DefaultRouter()
router.register('', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls,)),
    path('add/', CategoryCreate.as_view(), name="category-add"),
    path('<int:pk>/', CategoryDetail.as_view(), name="category-detail"),
    path('<int:pk>/update/', CategoryUpdate.as_view(), name="category-update"),
    path('<int:pk>/delete/', CategoryDelete.as_view(), name="category-delete"),
    path('', CategoryList.as_view(), name="category-list"),
]
