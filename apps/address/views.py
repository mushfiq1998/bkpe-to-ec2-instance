# Create your views here.

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .models import Address
from .serializers import AddressSerializer


# Create your views here.
class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["details"]
