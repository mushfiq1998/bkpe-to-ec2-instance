import stripe
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response

from core import settings

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentIntent(APIView):
    # token_param_config = openapi.Parameter(
    #     'amount', in_=openapi.IN_QUERY, description='Products amount', type=openapi.TYPE_STRING)

    def get(self, request, amount, **kwargs):

        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount),
                currency='usd',
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return Response({'clientSecret': intent['client_secret']}, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=400)


