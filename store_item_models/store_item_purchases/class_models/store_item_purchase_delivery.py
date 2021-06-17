from decimal import Decimal
from enum import Enum

from django_datetime.datetime import datetime
from django.db import models
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from staff_models.staff_groups.class_models.staff_deliver import StaffDeliver
from wallet_models.class_models.wallet import Wallet
from wallet_models.class_apps.balances.outlets.balance_outlet_condition import balance_outlet_condition

from store_item_models.store_item_purchases.class_models.store_item_purchase import StoreItemPurchase


class DeliveryStatusChoice(Enum):
    UNFULFILLED = "unfulfilled"
    DELIVERING = "delivering"
    RETURNING = "returning"
    ARRIVED = "arrived"
    COLLECTED = "collected"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


# payment choice
class PaymentStatusChoice(Enum):
    OPTIONAL = "optional"
    EXPIRED = "expired"
    REFUND = "refund"
    FAILED = "failed"
    UNPAID = "unpaid"
    PAID = "paid"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class StoreItemPurchaseDelivery(models.Model):
    account = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    item_purchase = models.ForeignKey(
        StoreItemPurchase,
        on_delete=models.CASCADE,
        related_name='item_purchase_deliveries',
        blank=True,
        null=True
    )
    deliver = models.ForeignKey(StaffDeliver, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    cost_delivery = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    delivery_date = models.DateTimeField(default=datetime.dnow())
    arrived_date = models.DateTimeField(null=True, blank=True)
    payment_status = models.CharField(
        choices=PaymentStatusChoice.choices(),
        blank=True,
        null=True,
        max_length=120
    )

    delivery_status = models.CharField(
        choices=DeliveryStatusChoice.choices(),
        blank=True,
        null=True,
        max_length=120
    )

    class Meta:
        verbose_name = 'Store Item Purchase deliveries'
        verbose_name_plural = 'Store Item Purchase deliveries'

    def save(self, *args, **kwargs):
        super(StoreItemPurchaseDelivery, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.deliver)


@receiver(post_save, sender=StoreItemPurchaseDelivery)
def add(sender, instance, created, **kwargs):
    if created:
        # account
        print(instance.account.id)
        balance_outlet_condition.set_current_condition((instance.payment_status == PaymentStatusChoice.PAID.name))
        balance_outlet_condition.set_current_pk(instance.account.id)
        balance_outlet_condition.outlet_account(instance.cost_delivery)


@receiver(pre_save, sender=StoreItemPurchaseDelivery)
def update(sender, instance, **kwargs):
    if instance.id is None:
        pass
    else:
        old_value = StoreItemPurchaseDelivery.objects.get(id=instance.id)
        # account
        balance_outlet_condition.set_current_condition((instance.payment_status == PaymentStatusChoice.PAID.name))
        balance_outlet_condition.set_current_pk(instance.account.id)
        balance_outlet_condition.set_last_condition((old_value.payment_status == PaymentStatusChoice.PAID.name))
        balance_outlet_condition.set_last_pk(old_value.account.id)
        balance_outlet_condition.update_outlet_account(instance.cost_delivery, old_value.cost_delivery)


@receiver(pre_delete, sender=StoreItemPurchaseDelivery)
def delete(sender, instance, using, **kwargs):
    old_value = StoreItemPurchaseDelivery.objects.get(id=instance.id)
    # account
    balance_outlet_condition.set_last_condition(old_value.payment_status == PaymentStatusChoice.PAID.name)
    balance_outlet_condition.set_last_pk(old_value.account.id)
    balance_outlet_condition.refund_outlet_account(last_amount=old_value.cost_delivery)
    # if old_value.payment_status == PaymentStatusChoice.PAID.name:
    #     BalanceOutlet.refund(old_value.cost_delivery, old_value.account.id)
