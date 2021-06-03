from decimal import Decimal
from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from wallet_models.class_models.wallet import Wallet

from store_item_models.class_projects.item_accounts.item_account_outlet import item_account_outlet
from store_item_models.class_projects.item_stocks.item_stock_supply import item_stock_supply
from store_item_models.store_item_purchases.class_models.store_item_purchase import StoreItemPurchase
from store_item_models.store_item_stocks.models import StoreItemStock
from store_item_models.store_item_suppliers.models import StoreItemSupplier


class StoreItemPurchaseStock(models.Model):
    account = models.ForeignKey(
        Wallet, on_delete=models.CASCADE
    )
    item_purchase = models.ForeignKey(
        StoreItemPurchase,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='store_item_purchase_stock'
    )
    item_stock = models.ForeignKey(
        StoreItemStock,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    item_supplier = models.ForeignKey(StoreItemSupplier, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    price_per_unit = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal(0.00)
    )
    is_transferred = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Store Item purchase stocks'
        verbose_name_plural = 'Store Item purchase stocks'

    def __str__(self):
        return "{}".format(self.item_stock)


@receiver(post_save, sender=StoreItemPurchaseStock)
def add(sender, instance, created, **kwargs):
    if created:
        # stock
        item_stock_supply.supply_stock(instance)
        # account
        item_account_outlet.outlet_account(
            instance,
            (instance.price_per_unit * instance.quantity)
        )


@receiver(pre_save, sender=StoreItemPurchaseStock)
def update(sender, instance, **kwargs):
    if instance.id is None:
        pass
    else:
        old_value = StoreItemPurchaseStock.objects.get(id=instance.id)
        # stock
        item_stock_supply.update_stock(
            current_instance=instance,
            last_instance=old_value
        )
        # account
        item_account_outlet.update_outlet_account(
            current_instance=instance,
            last_instance=old_value,
            current_amount=(instance.price_per_unit * instance.quantity),
            last_amount=(old_value.price_per_unit * instance.quantity)
        )


@receiver(pre_delete, sender=StoreItemPurchaseStock)
def delete(sender, instance, using, **kwargs):
    # stock
    old_value = StoreItemPurchaseStock.objects.get(id=instance.id)
    item_stock_supply.return_stock(old_value)
    # account
    item_account_outlet.refund_outlet_account(old_value, (old_value.price_per_unit * instance.quantity))
