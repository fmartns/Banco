from django.urls import path
from bank.views import WalletView, DepositView, TransferView, TransferHistory

urlpatterns = [
    path('api/v1/saldo/', WalletView.as_view(), name='wallet'),
    path('api/v1/depositar/', DepositView.as_view(), name='deposit'),
    path('api/v1/transferir/', TransferView.as_view(), name='transfer'),
    path('api/v1/historico-transferencias/', TransferHistory.as_view(), name='transfer_history')
]
