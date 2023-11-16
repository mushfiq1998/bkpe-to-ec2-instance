from django.db import models
from django.template.defaultfilters import slugify

from apps.address.models import Address
from apps.authentication.models import User


class Cart(models.Model):
    product_id = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return "{} - {} - {}".format(self.product_id,
                                     self.product_name,
                                     self.quantity,
                                     self.created_at,
                                     self.updated_at)


# Create your models here.
class Order(models.Model):
    payment_status = models.CharField(max_length=255)
    order_status = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_info = models.ForeignKey(Address, related_name="order", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order', related_query_name='order')
    products = models.ManyToManyField(Cart, related_name='order')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Order"
        verbose_name_plural = "Order"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.total_price)
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {} - {}".format(self.total_price,
                                     self.created_at,
                                     self.updated_at)
