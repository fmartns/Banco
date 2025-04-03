import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bank.models import Wallet

class Command(BaseCommand):
    help = 'Cria usuários de teste com carteiras e saldo aleatório'

    def handle(self, *args, **kwargs):
        usuarios = [
            {"username": "fernandasilva35", "first_name": "Fernanda", "last_name": "Silva", "email": "fernandasilva35@mail.com"},
            {"username": "mariasouza46", "first_name": "Maria", "last_name": "Souza", "email": "mariasouza46@testmail.com"},
            {"username": "lucasmartins16", "first_name": "Lucas", "last_name": "Martins", "email": "lucasmartins16@testmail.com"},
            {"username": "joãopereira95", "first_name": "João", "last_name": "Pereira", "email": "joãopereira95@testmail.com"},
            {"username": "carlosoliveira7", "first_name": "Carlos", "last_name": "Oliveira", "email": "carlosoliveira7@testmail.com"},
            {"username": "mariaalmeida56", "first_name": "Maria", "last_name": "Almeida", "email": "mariaalmeida56@testmail.com"},
            {"username": "analima13", "first_name": "Ana", "last_name": "Lima", "email": "analima13@example.com"},
            {"username": "carlosmartins61", "first_name": "Carlos", "last_name": "Martins", "email": "carlosmartins61@mail.com"},
            {"username": "mariaalmeida34", "first_name": "Maria", "last_name": "Almeida", "email": "mariaalmeida34@example.com"},
        ]

        for u in usuarios:
            user = User.objects.create_user(
                username=u["username"],
                first_name=u["first_name"],
                last_name=u["last_name"],
                email=u["email"],
                password="SenhaForte123"
            )
            user.is_active = True
            user.is_staff = False
            user.is_superuser = False
            user.save()

            saldo = round(random.uniform(50.00, 500.00), 2)
            Wallet.objects.create(user=user, balance=saldo)
            print(f'Usuário criado: {u["username"]} | Saldo: R$ {saldo:.2f}')

        # Criar superusuário admin
        admin = User.objects.create_user(
            username="admin",
            first_name="Admin",
            last_name="Master",
            email="admin@example.com",
            password="SenhaForte123"
        )
        admin.is_active = True
        admin.is_staff = True
        admin.is_superuser = True
        admin.save()

        saldo = round(random.uniform(1000.00, 5000.00), 2)
        Wallet.objects.create(user=admin, balance=saldo)
        print(f'Superusuário criado: {admin.username} | Saldo: R$ {saldo:.2f}')
