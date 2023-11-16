from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Order, Cart
from ..address.models import Address
from ..address.serializers import AddressSerializer
from ..authentication.models import User
from ..authentication.serializers import UsersSerializer


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = CartSerializer(read_only=True, many=True)
    shipping_info = AddressSerializer(read_only=True)
    user = UsersSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

