from rest_flex_fields.views import FlexFieldsModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Image
from .serializers import ImageSerializer


# Create your views here.
class ImageViewSet(FlexFieldsModelViewSet):

	serializer_class = ImageSerializer
	queryset = Image.objects.all()
	# permission_classes = [IsAuthenticated]
