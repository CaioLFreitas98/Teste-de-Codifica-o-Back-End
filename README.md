# API de Backend – Teste Técnico Python JR

> Uma API RESTful simples e modular, desenvolvida com FastAPI, PostgreSQL e JWT, para gerenciar clientes, produtos, pedidos e enviar notificações via WhatsApp.

---

## 🎯 Objetivo do Projeto
Construir uma aplicação de backend que demonstre:

- **Arquitetura Limpa**: separação de responsabilidades (routers, models, services).
- **Qualidade de Código**: aderência a PEP8, commits claros, tratamento consistente de erros.
- **Documentação Clara**: README, Swagger UI e exemplos de payload.
- **Testes Automatizados**: pytest para unitários e integração.
- **Deploy Contêinerizado**: Docker + docker-compose.

---

## 🛠 Tecnologias

| Camada           | Ferramentas                                          |
| ---------------- | ---------------------------------------------------- |
| Linguagem        | Python 3.10+                                         |
| Framework Web    | FastAPI                                              |
| Banco de Dados   | PostgreSQL                                           |
| ORM & Migrações  | SQLAlchemy + Alembic                                 |
| Autenticação     | JWT (PyJWT)                                          |
| Testes           | pytest + FastAPI TestClient                          |
| Containers       | Docker + docker-compose                              |
| Notificações     | API WhatsApp (Twilio ou WhatsApp Business API)       |

---

## 🚀 Estrutura de Pastas

```text
├── app
│   ├── api         # Routers (endpoints)
│   ├── core        # Configurações, JWT e logging
│   ├── models      # SQLAlchemy models
│   ├── schemas     # Pydantic schemas
│   ├── services    # Regras de negócio
│   └── tests       # Testes unitários e de integração
├── alembic         # Migrations do banco
├── Dockerfile      # Imagem da aplicação
├── docker-compose.yml
└── README.md       # Documentação do projeto
