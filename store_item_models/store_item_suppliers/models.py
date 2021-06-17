from django_datetime.datetime import datetime
from django.db import models


class StoreItemSupplier(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_date = models.DateField(default=datetime.dnow())
    updated_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
