from django.urls import path
from .views import ListCryptoView


urlpatterns = [
    path('cryptos/', ListCryptoView.as_view(), name="crypto-all")
]