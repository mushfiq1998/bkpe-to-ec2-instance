import datetime
import json
import os
import random
import re
import tempfile
import uuid
from _pydecimal import Decimal
from contextlib import suppress

import excel2dict
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.rest_framework import DjangoFilterBackend, filters, FilterSet
from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from xl2dict import XlToDict
from django.utils.text import slugify

from apps.categories.models import Category
from apps.media.models import Image
from apps.products.models import Product, Variant
from apps.products.serializers import ProductSerializer, VariantSerializer


class ProductFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    min_price = filters.NumberFilter(field_name="unit_price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="unit_price", lookup_expr='lte')
    min_sale_price = filters.NumberFilter(field_name="unit_cost", lookup_expr='gte')
    max_sale_price = filters.NumberFilter(field_name="unit_cost", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['name']
        # fields = ['brand', 'type', 'year', 'new', 'onSale']


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["name", "category"]

    # filter_backends = [SearchFilter]
    # search_fields = ('^price', '^name')

    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

    # def retrieve(self, request, pk=None):
    #     queryset = Product.objects.all()
    #     product = get_object_or_404(queryset, pk=pk)
    #     serializer = ProductSerializer(product)
    #     context = serializer.data
    #     context['category'] = CategorySerializer(product.category).data
    #     return Response(context)

    def create(self, request):
        today = datetime.date.today()
        todays_records = Product.objects.filter(created_at=today)[:10]
        if todays_records.count() > 10:
            raise APIException("today limit reached")
        data = request.data.copy()
        uploaded_files = []
        files = request.FILES.getlist('images')
        if files:
            request.data.pop('images')

            for index, file in enumerate(files):
                content = Image.objects.create(
                    name=f"{data['slug']}{index}",
                    image=file
                )
                uploaded_files.append(content)

            data['images'] = [file.id for file in uploaded_files][0]

        serializer = ProductSerializer(data=data)

        print("-------------")
        print(serializer.is_valid())
        print("-------------")

        if serializer.is_valid():
            serializer.save()
            # files = request.FILES.getlist('images')
            # if files:
            #     prod_qs = Product.objects.get(id=serializer.data['id'])
            #     prod_qs.images.add(*uploaded_files)
            #     context = serializer.data
            #
            #     context["images"] = [file.id for file in uploaded_files]
            #
            #     return Response(context, status=status.HTTP_201_CREATED)

            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        today = datetime.date.today()

        todays_records = Product.objects.filter(updated_at__gt=today)[:10]
        if todays_records.count() > 10:
            raise APIException("today limit reached")

        serializer.save()
        return Response(serializer.data)


class ProductCreate(CreateView):
    # class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = ["name", "unit_price", "quantity_needed", "category"]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdate(UpdateView):
    model = Product
    # fields = ["name"]
    fields = ["name", "unit_price", "quantity_needed", "category"]


class ProductDelete(DeleteView):
    model = Product
    success_url = reverse_lazy("products:product-list")


class ProductList(ListView):
    model = Product


class ProductDetail(DetailView):
    model = Product


class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all().order_by("-created_at")
    serializer_class = VariantSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "product"]


class FileUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        file = request.FILES['file']
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        ext = file.name.split('.')[-1]
        if ext not in ['xls']:
            return Response({'error': 'File not supported'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the uploaded file to a temporary file path
        temp_file = tempfile.NamedTemporaryFile(delete=False)

        for chunk in file.chunks():
            temp_file.write(chunk)

        file_path = temp_file.name

        # Read Excel Sheets
        data_dict = excel2dict.to_dict(file_path)

        camaro_parts = data_dict["Camaro Parts"]

        i = 1

        for row in camaro_parts:
            major_category = re.sub(r'\s*-\s*', '-', str(row['MAJOR CATEGORY']).strip())
            sub_category = re.sub(r'\s*-\s*', '-', str(row['SUB-CATEGORIES']).strip())
            sub_sub_category = re.sub(r'\s*-\s*', '-', str(row['SUB-SUB CATEGORIES']).strip())
            sub_sub_sub_category = re.sub(r'\s*-\s*', '-', str(row['SUB-SUB-SUB CATEGORIES']).strip())

            with suppress(Exception):
                major_category, created = Category.objects.get_or_create(name=major_category, defaults={
                    'name': major_category,
                    'slug': major_category.replace(" ", "-"),
                })

            with suppress(Exception):
                sub_category, created = Category.objects.get_or_create(name=sub_category, defaults={
                    'name': sub_category,
                    'slug': sub_category.replace(" ", "-"),
                    'parent': major_category
                })

            with suppress(Exception):
                sub_sub_category, created = Category.objects.get_or_create(name=sub_sub_category, defaults={
                    'name': sub_sub_category,
                    'slug': sub_sub_category.replace(" ", "-"),
                    'parent': sub_category
                })

            with suppress(Exception):
                sub_sub_sub_category, created = Category.objects.get_or_create(name=sub_sub_sub_category, defaults={
                    'name': sub_sub_sub_category,
                    'slug': sub_sub_sub_category.replace(" ", "-"),
                    'parent': sub_sub_category
                })

            with suppress(Exception):
                Product.objects.update_or_create(bkpp_p_n=str(row['BKPP P/N']), defaults={
                    'product_id': str(row[1.0]),
                    'part_type': str(row['PART TYPE']),
                    'bkpp_p_n': str(row['BKPP P/N']),
                    'category': sub_sub_sub_category,
                    'publish': True if row['PUBLISH'] == "Yes" else False,
                    'year_1967': True if row[1967.0] == "X" else False,
                    'year_1968': True if row[1968.0] == "X" else False,
                    'year_1969': True if row[1969.0] == "X" else False,
                    'name': str(row['NAME']),
                    'slug': slugify(str(row['BKPP P/N'])),
                    'description': str(row['DESCRIPTION']),
                    'notes': str(row['NOTES']),
                    'gm_part_numbers': str(row['GM PART NUMBERS']),
                    'aim_numbers': str(row['AIM NUMBERS']),
                    'years': str(row['YEARS']),
                    'body_style': str(row['BODY STYLE']),
                    'trim': str(row['TRIM']),
                    'interior': row['INTERIOR'],
                    'engine': row['ENGINE'],
                    'transmission': str(row['TRANSMISSION']),
                    'part_manufacturer': str(row['PART MANUFACTURER']),
                    'manufacturer_part_name': str(row['MANFACTURER\'S PART NAME']),
                    'manufacturer_part_number': str(row['PART NUMBER']),
                    'suppliers_name': str(row['SUPPLIER\'S NAME']),
                    'suppliers_part_name': str(row['SUPPLIER\'S PART NAME']),
                    'suppliers_part_number': str(row['PART NUMBER']),
                    'email_to_tim': True if row['E-MAIL TO TIM'] == "Yes" else False,
                    'email_address': str(row['E-MAIL ADDRESS']),
                    'street_address': str(row['STREET ADDRESS']),
                    'city_state_zip': str(row['CITY, STATE & ZIP']),
                    'quantity_included': (re.findall(r'\d+', str(row['QTY INCLUDED'])) or ['0'])[0],
                    'quantity_needed': (re.findall(r'\d+', str(row['QTY NEEDED'])) or ['0'])[0],
                    'to_whom': str(row['TO WHOM']),
                    # 'cost': float(row['COST '] or 0 if row['COST '] != 'N/A' else 0),
                    'cost': (re.findall(r'\d+', str(row['COST '])) or ['0'])[0],
                    'msrp': float(row['MSRP'] or 0 if row['MSRP'] != 'N/A' else 0),
                    'unit_cost': float(row['UNIT COST'] or 0 if row['UNIT COST'] not in ['N/A', '', 'N/.A'] else 0),
                    'unit_price': float(row['UNIT PRICE'] or 0 if row['UNIT PRICE'] not in ['N/A', ''] else 0),
                    'photo_p_n': str(row['PHOTO P/N']),
                    'fixed_shipping': True if row['FIXED SHIPPING'] == "Yes" else False,
                    'multiple_fixed_shipping': True if row['MULTIPLE FIXED SHIP'] == "Yes" else False,
                    'inventory': int(row['INVENTORY'] or 0),
                    'gm_affiliation': True if row['GM AFFILIATION'] == "Yes" else False,
                    'remanufactured': True if row['REMANUFACTURED?'] == "Yes" else False,
                    'made_in_the_usa': True if row['MADE IN THE USA?'] == "Yes" else False,
                    'sold_as': str(row['SOLD AS']),
                    'shipping_method': str(row['SHIPPING METHOD']),
                    'help': str(row['HELP']),
                    'special_handling': str(row['SPECIAL HANDLING']),
                    'h': str(row['H']),
                    'l': str(row['L']),
                    'w': str(row['W']),
                    'weight': int(row['WEIGHT'] or 0),
                })

            i += 1
            print(i)

        temp_file.close()
        os.unlink(temp_file.name)

        return JsonResponse({'msg': 'File uploaded'}, safe=False)
        # return JsonResponse(json.dumps(camaro_parts), safe=False)
