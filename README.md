
# Desafio Backend

API desenvolvida para gerenciar **carteiras digitais** e **transações financeiras** entre usuários.

---

## Funcionalidades

- Autenticação com JWT
- Criação de usuários
- Consulta de saldo da carteira
- Adição de saldo (restrito a administradores)
- Transferência entre usuários
- Histórico de transferências (com filtro de data, restrito a administradores)

---

## Endpoints da API

Todos os endpoints abaixo seguem o padrão REST e retornam respostas em JSON. A autenticação é feita via JWT no formato:

```
Authorization: Bearer <token>
```

---

### Autenticação

#### POST `/api/v1/signup/`

Cria um novo usuário.

**Request:**
```json
{
  "username": "joao123",
  "first_name": "João",
  "last_name": "Silva",
  "email": "joao@email.com",
  "password": "SenhaForte123",
  "confirm_password": "SenhaForte123"
}
```

**Response:**
```json
{
  "message": "Usuário criado com sucesso"
}
```

---

#### POST `/api/v1/login/`

Autentica o usuário e retorna os tokens JWT.

**Request:**
```json
{
  "username": "joao123",
  "password": "SenhaForte123"
}
```

**Response:**
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

---

### Carteira

#### GET `/api/v1/saldo/`

Retorna o saldo da carteira do usuário autenticado.

**Response:**
```json
{
  "saldo": "150.00"
}
```

---

#### POST `/api/v1/depositar/` *(apenas superuser)*

Adiciona saldo à carteira de outro usuário.

**Request:**
```json
{
  "recipient_username": "maria88",
  "amount": "200.00"
}
```

**Response:**
```json
{
  "message": "Saldo adicionado com sucesso, novo saldo: 300.00"
}
```

---

#### POST `/api/v1/transferir/`

Realiza uma transferência entre carteiras.

**Request:**
```json
{
  "recipient_username": "maria88",
  "amount": "50.00"
}
```

**Response:**
```json
{
  "message": "Transferência realizada com sucesso"
}
```

---

### Histórico de Transferências

#### GET `/api/v1/historico-transferencias/` *(apenas superuser)*

Retorna as transferências realizadas por um usuário, com filtro opcional por data.

**Query Params:**

- `start_date`: (opcional) Ex: `2024-01-01`
- `end_date`: (opcional) Ex: `2024-12-31`

**Request Body:**
```json
{
  "username": "joao123"
}
```

**Response:**
```json
[
  {
    "Remetente": "joao123",
    "Destinatário": "maria88",
    "Valor": "50.00",
    "Horário": "2024-07-01T14:23:45Z"
  }
]
```

---

## Executando o Projeto

### 1. Clone o projeto e entre na pasta

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Instale e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o `.env`

Crie um `.env` com suas credenciais do PostgreSQL:

```
DB_NAME=nome_banco
DB_USER=usuario
DB_PASSWORD=senha
DB_HOST=localhost
DB_PORT=5432
```

### 5. Aplique as migrações

```bash
python manage.py migrate
```

### 6. Gere os usuários de teste
```bash
python manage.py criar_usuarios
```

Lista de usuários de teste: [Pastebin](https://pastebin.com/q5SsW1kU)


### 7. Rode o servidor

```bash
python manage.py runserver
```
