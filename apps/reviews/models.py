from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _

from apps.authentication.models import User
from apps.products.models import Product


# Create your models here.
class Review(models.Model):
    user_name = models.CharField(max_length=255)
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews',
                                related_query_name='reviews')
    rating = models.PositiveIntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
    isApproved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', related_query_name='reviews')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Parent Review"),
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user_name)
        super(Review, self).save(*args, **kwargs)

    def children(self):
        """Return replies of a Category."""
        return Review.objects.filter(parent=self)

    @property
    def is_parent(self):
        """Return `True` if instance is a parent."""
        if self.parent is not None:
            return False
        return True

    def __str__(self):
        return "{} - {} - {}".format(self.user_name,
                                     self.product.name,
                                     self.user.name,
                                     self.created_at,
                                     self.updated_at)
