from django.db import models


class StoreItemUse(models.Model):
    note = models.TextField(
        blank=True, null=True
    )
    request_date = models.DateField(blank=True, null=True)
    take_out_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Store Item uses'
        verbose_name_plural = 'Store Item uses'

    def save(self, *args, **kwargs):
        super(StoreItemUse, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.take_out_date)
