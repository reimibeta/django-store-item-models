from django.db import models
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver

from store_item_models.class_projects.item_stocks.item_stock_outlet import item_stock_outlet
from store_item_models.store_item_stocks.models import StoreItemStock
from store_item_models.store_item_uses.class_models.store_item_use import StoreItemUse


class StoreItemUseStock(models.Model):
    item_use = models.ForeignKey(
        StoreItemUse, on_delete=models.CASCADE,
    )
    note = models.TextField(
        blank=True, null=True
    )
    item_stock = models.ForeignKey(
        StoreItemStock, on_delete=models.CASCADE,
        related_name='store_item_use_stock'
    )
    quantity = models.IntegerField(default=0)
    is_move_from_stock = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Store Item use Stocks'
        verbose_name_plural = 'Store Item use Stocks'

    def save(self, *args, **kwargs):
        super(StoreItemUseStock, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.item_stock)


@receiver(post_save, sender=StoreItemUseStock)
def add(sender, instance, created, **kwargs):
    if created:
        item_stock_outlet.outlet_stock(instance)


@receiver(pre_save, sender=StoreItemUseStock)
def update(sender, instance, **kwargs):
    if instance.id is None:
        pass
    else:
        # stock
        old_value = StoreItemUseStock.objects.get(id=instance.id)
        item_stock_outlet.update_stock(
            current_instance=instance,
            last_instance=old_value
        )


@receiver(pre_delete, sender=StoreItemUseStock)
def delete(sender, instance, using, **kwargs):
    old_value = StoreItemUseStock.objects.get(id=instance.id)
    # refund product stock
    item_stock_outlet.refund_stock(
        last_instance=old_value
    )
