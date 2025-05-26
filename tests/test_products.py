import pytest

def test_create_get_update_delete_product(client):
    # 1) Registrar e logar como admin
    admin_payload = {"username": "prodadmin", "email": "prodadmin@example.com", "password": "adminprod", "is_admin": True}
    client.post("/auth/register", json=admin_payload)
    login_payload = {"username": "prodadmin", "password": "adminprod"}
    response = client.post("/auth/login", json=login_payload)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2) Criar produto
    product_data = {
        "description": "Camisa Polo",
        "sale_price": 79.9,
        "barcode": "1234567890123",
        "section": "Roupas",
        "initial_stock": 50,
        "expiration_date": None,
        "image_url": None
    }
    response = client.post("/products", json=product_data, headers=headers)
    assert response.status_code == 201
    created = response.json()
    assert created["description"] == "Camisa Polo"
    product_id = created["id"]

    # 3) Obter produto
    response = client.get(f"/products/{product_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["barcode"] == "1234567890123"

    # 4) Atualizar produto (ex: mudar preço)
    update_data = {"sale_price": 89.9}
    response = client.put(f"/products/{product_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["sale_price"] == 89.9

    # 5) Listar produtos (usando filtro de seção)
    response = client.get("/products?category=Roupas", headers=headers)
    assert response.status_code == 200
    products = response.json()
    assert any(p["id"] == product_id for p in products)

    # 6) Excluir produto
    response = client.delete(f"/products/{product_id}", headers=headers)
    assert response.status_code == 204

    # 7) Verificar exclusão
    response = client.get(f"/products/{product_id}", headers=headers)
    assert response.status_code == 404
