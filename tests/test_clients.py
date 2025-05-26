import pytest

def test_create_get_update_delete_client(client):
    # 1) Registrar e logar como admin
    admin_payload = {"username": "admin", "email": "admin@example.com", "password": "adminpass", "is_admin": True}
    client.post("/auth/register", json=admin_payload)
    login_payload = {"username": "admin", "password": "adminpass"}
    response = client.post("/auth/login", json=login_payload)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2) Criar um cliente
    client_data = {"name": "Cliente A", "email": "clientea@example.com", "cpf": "12345678901", "phone": "11999999999"}
    response = client.post("/clients", json=client_data, headers=headers)
    assert response.status_code == 201
    created = response.json()
    assert created["name"] == "Cliente A"

    client_id = created["id"]

    # 3) Obter o cliente
    response = client.get(f"/clients/{client_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "clientea@example.com"

    # 4) Atualizar o cliente
    update_data = {"phone": "11888888888"}
    response = client.put(f"/clients/{client_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["phone"] == "11888888888"

    # 5) Listar clientes (filtro por email)
    response = client.get("/clients?email=clientea@example.com", headers=headers)
    assert response.status_code == 200
    clients = response.json()
    assert any(c["id"] == client_id for c in clients)

    # 6) Excluir cliente
    response = client.delete(f"/clients/{client_id}", headers=headers)
    assert response.status_code == 204

    # 7) Verificar que foi excluído
    response = client.get(f"/clients/{client_id}", headers=headers)
    assert response.status_code == 404
