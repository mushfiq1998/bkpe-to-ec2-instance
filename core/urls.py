"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include



from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.authentication.views import UserProfile
from core import settings

schema_view = get_schema_view(
    openapi.Info(
        title="BKPE Multi Vendor Ecommerce",
        default_version='v1',
        description="API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    # url='http://bkpe-env.eba-hezmw5qh.ap-northeast-1.elasticbeanstalk.com/',
    # url='https://bkpe-multi-ven-prod-test-k5p06h.mo6.mogenius.io/',
    url='http://127.0.0.1:8000/',
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('payment/', include("payment.urls")),
    path('admin/', admin.site.urls),
    path('auth/', include('apps.authentication.urls')),
    path('users/', include('apps.authentication.users_urls')),
    path('user/profile/', UserProfile.as_view(), name="profile"),
    path('products/', include('apps.products.urls')),
    # path('variants/', include('apps.products.variants_urls')),
    path('categories/', include('apps.categories.urls')),
    # path('media/', include('apps.media.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('address/', include('apps.address.urls')),
    path('order/', include('apps.order.urls')),
    # path('cart/', include('apps.cart.urls')),
    # path('discounts/', include('apps.discounts.urls')),
    path('chat/', include('apps.chat.api.urls', namespace='chat')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
# +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
