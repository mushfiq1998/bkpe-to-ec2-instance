# Create your views here.

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .models import Order
from .serializers import OrderSerializer
from rest_framework.response import Response


# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["payment_status"]

    # def create(self, request):
    #     data = request.data.copy()
    #     user = data["user"]
    #
    #     serializer = ProductSerializer(data=data)
    #
    #     if serializer.is_valid():
    #         serializer.save()
    #         files = request.FILES.getlist('images')
    #         if files:
    #             request.data.pop('images')
    #
    #             prod_qs = Product.objects.get(id=serializer.data['id'])
    #             # category_qs = Category.objects.get(id=serializer.data['category'])
    #
    #             uploaded_files = []
    #             for index, file in enumerate(files):
    #                 content = Image.objects.create(
    #                     name=f"{serializer.data['slug']}{index}",
    #                     image=file
    #                 )
    #                 uploaded_files.append(content)
    #
    #             prod_qs.images.add(*uploaded_files)
    #             context = serializer.data
    #
    #             context["images"] = [file.id for file in uploaded_files]
    #
    #             # serializer = ImageSerializer(uploaded_files, many=True, context={"request": request})
    #             # context["images"] = [data['image'] for data in serializer.data]
    #             # context["category"] = CategorySerializer(category_qs).data
    #
    #             return Response(context, status=status.HTTP_201_CREATED)
    #
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors)
