def test_get_empty_cart(client, customer_token):
    response = client.get("/cart", headers={"Authorization": f"Bearer {customer_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


def test_add_item_to_cart(client, customer_token, menu_item_id):
    response = client.post(
        "/cart/items",
        json={"menu_item_id": menu_item_id, "quantity": 2},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 2
    assert data["subtotal"] == 200.0


def test_add_same_item_increases_quantity(client, customer_token, menu_item_id):
    client.post(
        "/cart/items",
        json={"menu_item_id": menu_item_id, "quantity": 2},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    response = client.post(
        "/cart/items",
        json={"menu_item_id": menu_item_id, "quantity": 1},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 3


def test_update_cart_item_quantity(client, customer_token, menu_item_id):
    add_response = client.post(
        "/cart/items",
        json={"menu_item_id": menu_item_id, "quantity": 2},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    item_id = add_response.json()["items"][0]["id"]

    response = client.patch(
        f"/cart/items/{item_id}",
        json={"quantity": 5},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert response.status_code == 200
    assert response.json()["items"][0]["quantity"] == 5


def test_remove_cart_item(client, customer_token, menu_item_id):
    add_response = client.post(
        "/cart/items",
        json={"menu_item_id": menu_item_id, "quantity": 2},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    item_id = add_response.json()["items"][0]["id"]

    response = client.delete(
        f"/cart/items/{item_id}",
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert response.status_code == 200
    assert response.json()["items"] == []


def test_cart_requires_auth(client):
    response = client.get("/cart")
    assert response.status_code == 401
    