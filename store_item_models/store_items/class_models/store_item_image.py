from uuid import uuid4

from django.db import models
from image_utils.compress.compress_image import compress_image

from store_item_models.store_items.class_models.store_item import StoreItem


class StoreItemImage(models.Model):
    item = models.ForeignKey(StoreItem, on_delete=models.CASCADE, related_name='store_item_image')
    image = models.ImageField(upload_to='images/store_items/', null=True)
    thumbnail = models.ImageField(
        upload_to='images/store_items/thumbnails/',
        blank=True, null=True,
        editable=False
    )

    def save(self, *args, **kwargs):
        if str(self.image.path) == str(self.image.file):
            print('return true when on new file uploaded!')
        else:
            self.image = compress_image.resize(self.image, 900)
            self.thumbnail = compress_image.resize(self.image, 500)
        super(StoreItemImage, self).save(*args, **kwargs)

    def __str__(self):
        return self.image.url
