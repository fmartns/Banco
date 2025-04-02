from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.permissions import AllowAny
from bank.models import Wallet

# Signup
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if User.objects.filter(username=username).exists():
            raise ValidationError('Usuário já existe')

        if User.objects.filter(email=email).exists():
            raise ValidationError('E-mail já cadastrado')

        if password != confirm_password:
            raise ValidationError('Senhas não coincidem')

        try:
            validate_password(password=password)
        except ValidationError as e:
            raise ValidationError({'password': e.messages})

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=False,
            is_active=True,
            is_superuser=False,
        )

        Wallet.objects.create(user=user)

        return Response({'message': 'Usuário criado com sucesso'}, status=201)

# Login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            raise ValidationError('Usuário e senha são obrigatórios')

        user = authenticate(request, username=username, password=password)

        if user is None:
            raise ValidationError('Credenciais inválidas')

        if not user.is_active:
            raise ValidationError('Usuário inativo')

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
