from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from bank.models import Wallet, Transaction, Deposit
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
from datetime import datetime

class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user is None:
            return Response({'error': 'User not found'}, status=404)
        else:
            wallet = Wallet.objects.get(user=user)
            return Response({'saldo': wallet.balance}, status=200)
        
class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        amount = request.data.get('amount')
        recipient_username = request.data.get('recipient_username')

        if not request.user.is_superuser:
            return Response({'error': 'Apenas administradores podem adicionar saldo'}, status=403)
        
        if recipient_username is None:
            return Response({'error': 'Usuário destinatário não fornecido'}, status=400)
        
        if not User.objects.filter(username=recipient_username).exists():
            return Response({'error': 'Usuário destinatário não encontrado'}, status=404)
        
        recipient = User.objects.get(username=recipient_username)
        
        wallet = Wallet.objects.get(user=recipient)
        wallet.balance += Decimal(amount)
        wallet.save()
        
        Deposit.objects.create(wallet=wallet, amount=amount)
        
        return Response({'message': 'Saldo adicionado com sucesso, novo saldo: {}'.format(wallet.balance)}, status=200)
    
class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = request.user
        recipient_username = request.data.get('recipient_username')
        amount = request.data.get('amount')

        if recipient_username is None:
            return Response({'error': 'Usuário destinatário não fornecido'}, status=400)
        
        if not User.objects.filter(username=recipient_username).exists():
            return Response({'error': 'Usuário destinatário não encontrado'}, status=404)
        
        recipient = User.objects.get(username=recipient_username)
        
        if sender == recipient:
            return Response({'error': 'Você não pode transferir dinheiro para si mesmo'}, status=400)
        
        sender_wallet = Wallet.objects.get(user=sender)
        print(sender_wallet)
        recipient_wallet = Wallet.objects.get(user=recipient)
        print(recipient_wallet)

        if sender_wallet.balance < Decimal(amount):
            return Response({'error': 'Saldo insuficiente'}, status=400)

        sender_wallet.balance -= Decimal(amount)
        recipient_wallet.balance += Decimal(amount)

        sender_wallet.save()
        recipient_wallet.save()

        Transaction.objects.create(sender=sender_wallet, receiver=recipient_wallet, amount=amount)

        return Response({'message': 'Transferência realizada com sucesso'}, status=200)
    
# Listar transferências realizadas por um usuário, com filtro opcional por período de data
class TransferHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.data.get('username')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        user = User.objects.filter(username=username).first()

        if not request.user.is_superuser:
            return Response({'error': 'Apenas administradores podem acessar o histórico de transferências'}, status=403)

        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                if start_date > end_date:
                    return Response({'error': 'A data de início deve ser anterior à data de término'}, status=400)
            except ValueError:
                return Response({'error': 'Formato de data inválido. Use YYYY-MM-DD'}, status=400)

            transactions = Transaction.objects.filter(sender__user=user, timestamp__range=[start_date, end_date])
        else:
            transactions = Transaction.objects.filter(sender__user=user)

        transaction_list = []
        for transaction in transactions:
            transaction_list.append({
                'Remetente': transaction.sender.user.username,
                'Destinatário': transaction.receiver.user.username,
                'Valor': transaction.amount,
                'Horário': transaction.timestamp
            })

        return Response(transaction_list, status=200)

# Create your views here.


# Você deve criar uma API para gerenciar carteiras digitais e transações financeiras. Essa API será utilizada por uma aplicação front-end e deve incluir as seguintes funcionalidades:

# Autenticação
# Criar um usuário
# Consultar saldo da carteira de um usuário
# Adicionar saldo à carteira
# Criar uma transferência entre usuários (carteiras)

