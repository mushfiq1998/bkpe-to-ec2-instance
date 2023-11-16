from django.urls import include, path
from rest_framework import routers

from .views import ProductViewSet, ProductCreate, ProductDelete, ProductUpdate, ProductList, ProductDetail, \
    FileUploadView

router = routers.DefaultRouter()
router.register('', ProductViewSet)

urlpatterns = [
    path('', include(router.urls,)),
    path('add/', ProductCreate.as_view(), name="product-add"),
    # path('add/', CreateProduct, name="product-add"),
    path('<int:pk>/', ProductDetail.as_view(), name="product-detail"),
    path('<int:pk>/update/', ProductUpdate.as_view(), name="product-update"),
    path('<int:pk>/delete/', ProductDelete.as_view(), name="product-delete"),
    path('list/', ProductList.as_view(), name="product-list"),
    path('importProduct', FileUploadView.as_view(), name="product-import")
]
