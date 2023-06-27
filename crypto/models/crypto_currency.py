from django.db import models
from .base import BaseModelMixin


class CryptoCurrency(BaseModelMixin, models.Model):
    name = models.CharField(max_length=250, unique=True)
    price = models.FloatField(null=True)
    last_hour_difference = models.FloatField(null=True)
    last_24_hour_difference = models.FloatField(null=True)
    last_7_day_difference = models.FloatField(null=True)
    market_cap = models.CharField(max_length=250, null=True)
    volume_last_24_hour = models.CharField(max_length=250, null=True)
    circulating_supply = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.name
