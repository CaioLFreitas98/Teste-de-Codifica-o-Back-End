import pytest
from unittest.mock import patch

def test_send_whatsapp_message(client):
    # 1) Registrar e logar usuário comum
    user_payload = {"username": "wa_user", "email": "wauser@example.com", "password": "wapass", "is_admin": False}
    client.post("/auth/register", json=user_payload)
    token_user = client.post("/auth/login", json={"username":"wa_user","password":"wapass"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token_user}"}

    # 2) Criar cliente com telefone
    # Primeiro, registrar e logar como admin para criar cliente
    admin_payload = {"username": "wa_admin", "email": "waadmin@example.com", "password": "adminwa", "is_admin": True}
    client.post("/auth/register", json=admin_payload)
    token_admin = client.post("/auth/login", json={"username":"wa_admin","password":"adminwa"}).json()["access_token"]
    headers_admin = {"Authorization": f"Bearer {token_admin}"}

    client_data = {"name": "Cliente WA", "email": "clientewa@example.com", "cpf": "55566677788", "phone": "11912341234"}
    response = client.post("/clients", json=client_data, headers=headers_admin)
    client_id = response.json()["id"]

    # 3) Mock do requests.post utilizado por send_whatsapp_message
    with patch("app.services.whatsapp_service.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        payload = {"client_id": client_id, "message": "Olá, promoção!"}
        response = client.post("/whatsapp/send", json=payload, headers=headers)
        assert response.status_code == 200
        assert response.json()["detail"] == "Mensagem enviada com sucesso"
