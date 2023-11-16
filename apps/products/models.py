import datetime
import uuid
import magic

from django.db import models
from multiselectfield import MultiSelectField

from apps.categories.models import Category
from django.urls import reverse
from django.template.defaultfilters import slugify
from apps.media.models import Image
from apps.products.utils import Util
from django.utils.text import slugify


def variants_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<username>/<filename>
    return "products/variants/{0}/{1}".format(instance.name, filename)


# Create your models here.
class Product(models.Model):
    """
    Product Model class
    """

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Product"
        verbose_name_plural = "Products"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.TextField(null=True, blank=True)
    part_type = models.TextField(null=True, blank=True)
    bkpp_p_n = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, db_column='category', on_delete=models.CASCADE)
    publish = models.BooleanField(default=False)
    year_1967 = models.BooleanField(null=True, blank=True)
    year_1968 = models.BooleanField(null=True, blank=True)
    year_1969 = models.BooleanField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    gm_part_numbers = models.TextField(null=True, blank=True)
    aim_numbers = models.TextField(null=True, blank=True)
    years = models.TextField(null=True, blank=True)
    body_style = models.TextField(null=True, blank=True)
    trim = models.TextField(null=True, blank=True)
    interior = models.TextField(null=True, blank=True)
    engine = models.TextField(null=True, blank=True)
    transmission = models.TextField(null=True, blank=True)
    part_manufacturer = models.TextField(null=True, blank=True)
    manufacturer_part_name = models.TextField(null=True, blank=True)
    manufacturer_part_number = models.TextField(null=True, blank=True)
    suppliers_name = models.TextField(null=True, blank=True)
    suppliers_part_name = models.TextField(null=True, blank=True)
    suppliers_part_number = models.TextField(null=True, blank=True)
    email_to_tim = models.BooleanField(default=False)
    email_address = models.EmailField(null=True, blank=True)
    customer_number = models.TextField(null=True, blank=True)
    street_address = models.TextField(null=True, blank=True)
    city_state_zip = models.TextField(null=True, blank=True)
    quantity_included = models.PositiveIntegerField(null=True, blank=True)
    quantity_needed = models.PositiveIntegerField(null=True, blank=True)
    to_whom = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    msrp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    photo_p_n = models.TextField(null=True, blank=True)
    fixed_shipping = models.BooleanField(default=False)
    multiple_fixed_shipping = models.BooleanField(default=False)
    inventory = models.PositiveIntegerField(default=0)
    gm_affiliation = models.TextField(null=True, blank=True)
    remanufactured = models.BooleanField(default=False)
    made_in_the_usa = models.BooleanField(default=False)
    sold_as = models.TextField(null=True, blank=True)
    shipping_method = models.TextField(null=True, blank=True)
    help = models.TextField(null=True, blank=True)
    special_handling = models.TextField(null=True, blank=True)
    h = models.TextField(null=True, blank=True)
    l = models.TextField(null=True, blank=True)
    w = models.TextField(null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    images = models.ManyToManyField(Image, related_name='products')
    sku = models.CharField(max_length=8, db_index=True)
    new = models.BooleanField(default=False)
    onSale = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:product-detail", kwargs={"pk": self.slug})

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.name,
                                               # self.category,
                                               self.unit_price,
                                               self.quantity_needed,
                                               self.created_at,
                                               self.updated_at)


class Variant(models.Model):
    name = models.CharField(max_length=9, choices=(
        ("Color", "Color"),
        ("Size", "Size"),
    ), blank=True)
    value = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to=variants_directory_path, blank=True)
    product = models.ForeignKey(Product, related_name="variant", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return "{} - {} - {}".format(self.product.name,
                                     self.name,
                                     self.value,
                                     self.price,
                                     self.created_at,
                                     self.updated_at)
