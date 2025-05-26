# 🛠️ Lu Estilo API - Backend

Este projeto consiste na implementação de uma API RESTful para gerenciamento de:

- ✅ Autenticação e autorização de usuários
- ✅ Cadastro e gerenciamento de clientes
- ✅ Cadastro e gerenciamento de produtos
- ✅ Processamento de pedidos (Orders)
- ✅ Envio de mensagens via integração com WhatsApp

Foi desenvolvida utilizando as seguintes tecnologias e práticas:

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy ORM**
- **PostgreSQL**
- **Docker & Docker Compose**
- **JWT Authentication**
- **Pytest para testes**
- **Pydantic para validação de dados**

---

## ✅ **Funcionalidades da API**

### ✅ Autenticação de Usuário

- Registro (`POST /auth/register`)
- Login (`POST /auth/login`)
- Refresh Token (`POST /auth/refresh-token`)

**Proteção de rotas** via **JWT Token**.  
Os usuários podem se autenticar e obter tokens para consumir endpoints protegidos.

---

### ✅ Clientes (`/clients`)

- Criar cliente (`POST /clients`)
- Listar clientes (`GET /clients`)
- Obter cliente pelo ID (`GET /clients/{client_id}`)
- Atualizar cliente (`PUT /clients/{client_id}`)
- Deletar cliente (`DELETE /clients/{client_id}`)

---

### ✅ Produtos (`/products`)

- Criar produto (`POST /products`)
- Listar produtos (`GET /products`)
- Obter produto pelo ID (`GET /products/{product_id}`)
- Atualizar produto (`PUT /products/{product_id}`)
- Deletar produto (`DELETE /products/{product_id}`)

---

### ✅ Pedidos (`/orders`)

- Criar pedido (`POST /orders`)
- Listar pedidos (`GET /orders`)
- Obter pedido pelo ID (`GET /orders/{order_id}`)
- Atualizar pedido (`PUT /orders/{order_id}`)
- Deletar pedido (`DELETE /orders/{order_id}`)

---

### ✅ Integração com WhatsApp (`/whatsapp/send`)

- Enviar mensagem para número informado (`POST /whatsapp/send`)

Payload:

```json
{
  "phone_number": "+5511999999999",
  "message": "Olá! Seu pedido foi recebido com sucesso."
}
✅ Como rodar o projeto
📦 Pré-requisitos
Python 3.10+

Docker e Docker Compose

Git

✅ 1. Clone o repositório
bash
Copiar
Editar
git clone https://github.com/CaioLFreitas98/Teste-de-Codifica-o-Back-End.git
cd Teste-de-Codifica-o-Back-End
✅ 2. Configurar variáveis de ambiente
Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:

env
Copiar
Editar
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=lu_estilo
POSTGRES_HOST=db
POSTGRES_PORT=5432

SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

WHATSAPP_API_URL=https://api.whatsapp.com/send
WHATSAPP_API_TOKEN=token_de_teste
ENVIRONMENT=development
✅ 3. Rodar com Docker
bash
Copiar
Editar
docker-compose up -d --build
O serviço FastAPI estará disponível em:
http://localhost:8000/docs

📚 Documentação automática via Swagger.

✅ 4. Rodar localmente sem Docker
Crie o ambiente virtual:

bash
Copiar
Editar
python -m venv sistemaProduto
Ative:

bash
Copiar
Editar
# Windows
.\sistemaProduto\Scripts\Activate.ps1

# Unix/macOS
source sistemaProduto/bin/activate
Instale as dependências:

bash
Copiar
Editar
pip install -r requirements.txt
pip install email-validator
Configure .env conforme acima.

Rode as migrações:

bash
Copiar
Editar
alembic upgrade head
Execute a API:

bash
Copiar
Editar
uvicorn app.main:app --reload
Acesse:
http://localhost:8000/docs

✅ Testes automatizados
✅ Como rodar os testes
Ative o ambiente virtual.

Execute:

bash
Copiar
Editar
pytest -q
Todos os testes unitários para autenticação, clientes, produtos, pedidos e integração devem passar.

✅ Fluxo de autenticação
Registro (/auth/register) → cria um novo usuário.

Login (/auth/login) → retorna JWT Token.

Refresh Token (/auth/refresh-token) → gera novo token válido.

Para acessar endpoints protegidos, envie:

makefile
Copiar
Editar
Authorization: Bearer <seu_token>
✅ Arquitetura do Projeto
bash
Copiar
Editar
.
├── app
│   ├── api            # Endpoints da API
│   ├── core           # Configurações, segurança, utilitários
│   ├── db             # Modelos, sessão, migrações
│   ├── schemas        # Pydantic Schemas
│   └── main.py        # Ponto de entrada FastAPI
├── tests              # Testes automatizados Pytest
├── docker-compose.yml # Configuração de containers
├── alembic.ini        # Configuração de migrações
├── .env               # Variáveis de ambiente
└── requirements.txt   # Dependências do projeto
✅ Exemplos de payloads
➡️ Registro de usuário
json
Copiar
Editar
{
  "username": "usuario1",
  "email": "usuario1@email.com",
  "password": "123456",
  "is_admin": false
}
➡️ Login de usuário
json
Copiar
Editar
{
  "username": "usuario1",
  "password": "123456"
}
➡️ Criar cliente
json
Copiar
Editar
{
  "name": "João Silva",
  "email": "joao@email.com",
  "cpf": "12345678901",
  "phone": "+551199999999"
}
➡️ Criar produto
json
Copiar
Editar
{
  "description": "Produto Teste",
  "sale_price": 29.99,
  "barcode": "1234567890123",
  "section": "Roupas",
  "initial_stock": 10
}
➡️ Criar pedido
json
Copiar
Editar
{
  "client_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
✅ Melhorias Futuras
✅ Implementar testes de integração mais robustos.

✅ Melhorar tratamento de exceções e validações.

✅ Implementar filtros e paginação.

✅ Automatizar deploy com CI/CD (GitHub Actions).

✅ Autor
Caio L. Freitas
GitHub - CaioLFreitas98

✅ Licença
Projeto licenciado sob MIT License.

yaml
Copiar
Editar

---

## ✅ **Como usar:**

1. Crie um arquivo chamado `README.md` na raiz do projeto.
2. Cole o conteúdo acima.
3. Salve.
4. Depois faça:

```bash
git add README.md
git commit -m "docs: adiciona README.md detalhado"
git push
