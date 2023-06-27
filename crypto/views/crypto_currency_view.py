from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from ..models import CryptoCurrency
from ..serializers import CryptoSerializer
from ..managers import CryptoDataSyncManager


class ListCryptoView(generics.ListCreateAPIView):
    # queryset = CryptoCurrency.objects.all()
    serializer_class = CryptoSerializer

    def get_queryset(self):
        return CryptoCurrency.objects.order_by('-updated_on')[:100]

    def create(self, request, *args, **kwargs):
        data = request.data
        cdsm = CryptoDataSyncManager(refreshed_data=data)
        cdsm.data_sync()
        return Response({'message': 'data sync success'}, status=status.HTTP_201_CREATED)
