from django.db import models
from django.template.defaultfilters import slugify
from phonenumber_field.modelfields import PhoneNumberField

from apps.authentication.models import User


# Create your models here.
class Address(models.Model):
    details = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    phone = PhoneNumberField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address', related_query_name='address')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Address"
        verbose_name_plural = "Address"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.details)
        super(Address, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {} - {}".format(self.details,
                                     self.city,
                                     self.created_at,
                                     self.updated_at)
