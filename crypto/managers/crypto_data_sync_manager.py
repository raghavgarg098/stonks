from django.db import transaction

from ..models import CryptoCurrency
from ..utils import (
    cached_property,
    extract_dollar_value,
    extract_percentage_value,
    extract_market_cap,
    extract_numeric_volume,
)


class CryptoDataSyncManager:
    def __init__(self, refreshed_data=[]):
        self.refreshed_data = self.refurbish_scrapper_data(refreshed_data)

    @cached_property
    def all_crypto_names(self):
        return [data.get('name') for data in self.refreshed_data if data.get('name')]

    @cached_property
    def refreshed_cryptos(self):
        return CryptoCurrency.objects.filter(name__in=self.all_crypto_names)

    @cached_property
    def crypto_name_refreshed_cryptos_map(self):
        return {crypto.name: crypto for crypto in self.refreshed_cryptos}

    @cached_property
    def refreshed_crypto_names(self):
        return [crypto.name for crypto in self.refreshed_cryptos]

    @cached_property
    def new_crypto_names(self):
        return list(set(self.all_crypto_names) - set(self.refreshed_crypto_names))

    @cached_property
    def crypto_name_crypto_data_map(self):
        return {data.get('name'): data for data in self.refreshed_data if data.get('name')}

    def refurbish_scrapper_data(self, refreshed_data):
        refurbished_data = []
        for data in refreshed_data:
            refurbished_data.append(
                {
                    'name': data.get('name'),
                    'price': extract_dollar_value(data.get('price')),
                    'last_hour_difference': extract_percentage_value(data.get('1h')),
                    'last_24_hour_difference': extract_percentage_value(data.get('24h')),
                    'last_7_day_difference': extract_percentage_value(data.get('7d')),
                    'market_cap': extract_market_cap(data.get('market_cap')),
                    'volume_last_24_hour': extract_numeric_volume(data.get('volume(24h)')),
                    'circulating_supply': extract_numeric_volume(data.get('circulating supply')),
                }
            )
        return refurbished_data

    def data_sync(self):
        with transaction.atomic():
            # Update existing records in batches
            for i in range(0, len(self.refreshed_crypto_names), 100):
                crypto_names_batch = self.refreshed_crypto_names[i:i + 100]
                cryptos_batch = [
                    self.crypto_name_refreshed_cryptos_map.get(crypto_name)
                    for crypto_name in crypto_names_batch
                ]
                crypto_data_batch = [
                    self.crypto_name_crypto_data_map.get(crypto_name)
                    for crypto_name in crypto_names_batch
                ]
                for crypto, crypto_data in zip(cryptos_batch, crypto_data_batch):
                    for key, value in crypto_data.items():
                        setattr(crypto, key, value)
                CryptoCurrency.objects.bulk_update(
                    cryptos_batch,
                    fields=[
                        'price',
                        'last_hour_difference',
                        'last_24_hour_difference',
                        'last_7_day_difference',
                        'market_cap',
                        'volume_last_24_hour',
                        'circulating_supply',
                    ],
                )

            # Create new records in batches
            new_crypto_names_batched = [
                self.new_crypto_names[i:i + 100]
                for i in range(0, len(self.new_crypto_names), 100)
            ]
            new_crypto_currencies = []
            for crypto_names_batch in new_crypto_names_batched:
                new_crypto_currencies_batch = [
                    CryptoCurrency(**self.crypto_name_crypto_data_map.get(crypto_name))
                    for crypto_name in crypto_names_batch
                ]
                new_crypto_currencies.extend(new_crypto_currencies_batch)
            CryptoCurrency.objects.bulk_create(new_crypto_currencies)

