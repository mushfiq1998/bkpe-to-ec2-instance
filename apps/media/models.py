from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField


# Create your models here.
class Image(models.Model):
    name = models.TextField(null=True, blank=True)
    image = VersatileImageField(
        'Image',
        upload_to='',
        ppoi_field='image_ppoi'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    image_ppoi = PPOIField()

    def __str__(self):
        return "{} - {} - {}".format(self.image.name,
                                     self.created_at,
                                     self.updated_at)
