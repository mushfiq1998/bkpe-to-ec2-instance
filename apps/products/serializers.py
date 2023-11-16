from rest_framework import serializers

from apps.categories.serializers import CategorySerializer
from apps.media.serializers import ImageSerializer
from apps.products.models import Product, Variant
from apps.reviews.serializers import ReviewSerializer


class ProductSerializer(serializers.ModelSerializer):
    product_category = serializers.SerializerMethodField()
    # product_image = serializers.SerializerMethodField()
    # brand = serializers.SerializerMethodField()
    # type = serializers.SerializerMethodField()

    # images = ImageSerializer()

    class Meta:
        model = Product

        fields = "__all__"
        extra_kwargs = {
            "category": {
                "required": True,
            },
            # "images": {
            #     "required": True,
            # }
        }

        expandable_fields = {
            'reviews': (ReviewSerializer, {'many': True}),
            # 'image': (ImageSerializer, {'many': True}),
        }

    def get_product_category(self, obj):
        data = {
            'id': obj.category.id,
            'name': obj.category.name
        }
        return data

    # def get_product_image(self, obj):
    #     request = self.context.get('request')
    #     images = obj.images.all()
    #
    #     print("----------------")
    #     print(obj.images)
    #     print("----------------")
    #
    #     serializer = ImageSerializer(images, many=True, context={"request": request})
    #
    #     return serializer.data

        # images = [{'id': data['id'], 'name': data['name']} for data in serializer.data]
        # return images if images else ['https://www.electrosolutions.in/wp-content/uploads/2018/08/product-image-dummy'
        #                               '-600x353.jpg']

    # def get_brand(self, obj):
    #     data = {
    #         'id': obj.brand.id,
    #         'name': obj.brand.brand
    #     }
    #     return data
    #
    # def get_type(self, obj):
    #     data = {
    #         'id': obj.type.id,
    #         'name': obj.type.type
    #     }
    #     return data


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'
