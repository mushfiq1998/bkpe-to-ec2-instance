import uuid

from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _
from django.utils.text import slugify

# Create your models here.
from djongo.models import ObjectIdField


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Parent Category"),
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("categories:category-detail", kwargs={"pk": self.id})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Category, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def children(self):
        """Return replies of a Category."""
        return Category.objects.filter(parent=self)

    @property
    def is_parent(self):
        """Return `True` if instance is a parent."""
        if self.parent is not None:
            return False
        return True

    def __str__(self):
        return "{} - {} - {}".format(self.name,
                                     self.created_at,
                                     self.updated_at)
