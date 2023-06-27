from rest_framework import serializers
from ..models import CryptoCurrency


class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoCurrency
        fields = ('name',
                  'price',
                  'last_hour_difference',
                  'last_24_hour_difference',
                  'last_7_day_difference',
                  'market_cap',
                  'volume_last_24_hour',
                  'circulating_supply')

