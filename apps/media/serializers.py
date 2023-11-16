from rest_flex_fields import FlexFieldsModelSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer
from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(sizes='media_headshot')
    name = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = '__all__'

    def get_name(self, obj):
        return obj.image.name
