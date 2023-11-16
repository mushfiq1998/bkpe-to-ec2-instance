from django.contrib import admin

# Register your models here.
from .models import Order, Cart

admin.site.register(Cart)
admin.site.register(Order)
