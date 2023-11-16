from bson import ObjectId
from django.contrib import admin

# Register your models here.
from apps.products.models import Product, Variant

admin.site.register(Variant)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = (
        "name",
        "category",
    )
    list_filter = (("category", admin.RelatedOnlyFieldListFilter),)

