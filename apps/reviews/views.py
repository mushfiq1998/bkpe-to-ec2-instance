# Create your views here.

import datetime

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .models import Review
from .serializers import ReviewSerializer


# Create your views here.
# class ReviewViewSet(viewsets.ModelViewSet):
#     serializer_class = ReviewSerializer
#     queryset = Review.objects.all()
#     # permission_classes = [IsAuthenticated]
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ["product"]


# Create your views here.
class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user_name"]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        today = datetime.date.today()

        todays_records = Review.objects.filter(updated_at__gt=today)[:10]
        if todays_records.count() > 10:
            raise APIException("today limit reached")

        serializer.save()
        return Response(serializer.data)


class ReviewCreate(CreateView):
    model = Review
    fields = ["name", "parent"]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ReviewUpdate(UpdateView):
    model = Review
    queryset = Review.objects.filter()
    fields = ["name", "parent"]


class ReviewDelete(DeleteView):
    model = Review
    queryset = Review.objects.filter()
    success_url = reverse_lazy("products:product-list")


class ReviewList(ListView):
    model = Review


class ReviewDetail(DetailView):
    model = Review
