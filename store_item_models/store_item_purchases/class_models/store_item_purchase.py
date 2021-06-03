from datetime_utils.date_time import DateTime
from django.db import models

from store_item_models.store_item_suppliers.models import StoreItemSupplier


class StoreItemPurchase(models.Model):
    note = models.TextField(blank=True, null=True)
    # item_supplier = models.ForeignKey(StoreItemSupplier, on_delete=models.CASCADE, blank=True, null=True)
    request_date = models.DateField(default=DateTime.datenow)
    purchase_date = models.DateField(blank=True, null=True)
    received_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Store Item purchases'
        verbose_name_plural = 'Store Item purchases'

    def __str__(self):
        return "{} (id:{})".format(self.request_date, self.id)
