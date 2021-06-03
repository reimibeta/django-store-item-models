from django.db import models

from store_item_models.store_items.class_models.store_item import StoreItem


class StoreItemStock(models.Model):
    item = models.OneToOneField(
        StoreItem,
        on_delete=models.CASCADE,
        related_name='store_item_stock',
        blank=True,
        null=True
    )
    quantity = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = (('id', 'item'),)

    def save(self, *args, **kwargs):
        super(StoreItemStock, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.item)
