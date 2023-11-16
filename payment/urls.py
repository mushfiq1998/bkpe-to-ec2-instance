from django.urls import path
from .views import CreatePaymentIntent
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('create-payment-intent/<amount>/', CreatePaymentIntent.as_view(), name='payment-intent')
]
