import pytest

def test_create_get_update_delete_order(client):
    # 1) Registrar e logar como admin e usuário normal
    admin_payload = {"username": "orderadmin", "email": "orderadmin@example.com", "password": "adminorder", "is_admin": True}
    client.post("/auth/register", json=admin_payload)
    login_payload_admin = {"username": "orderadmin", "password": "adminorder"}
    token_admin = client.post("/auth/login", json=login_payload_admin).json()["access_token"]
    headers_admin = {"Authorization": f"Bearer {token_admin}"}

    user_payload = {"username": "orderuser", "email": "orderuser@example.com", "password": "userorder", "is_admin": False}
    client.post("/auth/register", json=user_payload)
    token_user = client.post("/auth/login", json={"username": "orderuser", "password": "userorder"}).json()["access_token"]
    headers_user = {"Authorization": f"Bearer {token_user}"}

    # 2) Criar cliente e produto para usar no pedido
    client_data = {"name": "Cliente Pedido", "email": "clientepedido@example.com", "cpf": "11122233344", "phone": "11999990000"}
    response = client.post("/clients", json=client_data, headers=headers_admin)
    client_id = response.json()["id"]

    product_data = {
        "description": "Calça Jeans",
        "sale_price": 120.0,
        "barcode": "9876543210987",
        "section": "Roupas",
        "initial_stock": 20,
        "expiration_date": None,
        "image_url": None
    }
    response = client.post("/products", json=product_data, headers=headers_admin)
    product_id = response.json()["id"]

    # 3) Criar pedido (usuário comum pode criar)
    order_payload = {
        "client_id": client_id,
        "items": [{"product_id": product_id, "quantity": 2}]
    }
    response = client.post("/orders", json=order_payload, headers=headers_user)
    assert response.status_code == 201
    created_order = response.json()
    order_id = created_order["id"]
    assert created_order["total_price"] == 240.0

    # 4) Obter pedido
    response = client.get(f"/orders/{order_id}", headers=headers_user)
    assert response.status_code == 200
    assert response.json()["id"] == order_id

    # 5) Atualizar status do pedido (usuário comum pode)
    update_payload = {"status": "PROCESSING"}
    response = client.put(f"/orders/{order_id}", json=update_payload, headers=headers_user)
    assert response.status_code == 200
    assert response.json()["status"] == "PROCESSING"

    # 6) Listar pedidos (filtro por client_id)
    response = client.get(f"/orders?client_id={client_id}", headers=headers_user)
    assert response.status_code == 200
    orders = response.json()
    assert any(o["id"] == order_id for o in orders)

    # 7) Deletar pedido (somente admin)
    response = client.delete(f"/orders/{order_id}", headers=headers_admin)
    assert response.status_code == 204

    # 8) Verificar exclusão
    response = client.get(f"/orders/{order_id}", headers=headers_user)
    assert response.status_code == 404
