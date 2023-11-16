from rest_framework import serializers

from apps.categories.models import Category


class CategorySerializer(serializers.ModelSerializer):

    # parent = serializers.SerializerMethodField()

    class Meta:
        model = Category

        fields = "__all__"

    # def get_parent(self, obj):
    #     request = self.context.get('request')
    #     parent = obj.parent
    #     serializer = CategorySerializer(parent)
    #     return serializer.data
