def add_address(client, token):
    response = client.post(
        "/addresses",
        json={
            "label": "Home",
            "location": {"display_name": "Test Address", "latitude": 28.99, "longitude": 77.01},
            "is_default": True,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    return response.json()["id"]


def add_item_to_cart(client, token, menu_item_id, quantity=2):
    client.post(
        "/cart/items",
        json={"menu_item_id": menu_item_id, "quantity": quantity},
        headers={"Authorization": f"Bearer {token}"},
    )


def test_create_order_success(client, customer_token, menu_item_id):
    address_id = add_address(client, customer_token)
    add_item_to_cart(client, customer_token, menu_item_id)

    response = client.post(
        "/orders",
        json={"address_id": address_id},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "PLACED"
    assert len(data["items"]) == 1
    assert data["subtotal"] == 200.0


def test_create_order_empty_cart_fails(client, customer_token):
    address_id = add_address(client, customer_token)

    response = client.post(
        "/orders",
        json={"address_id": address_id},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert response.status_code == 400


def test_cart_cleared_after_order(client, customer_token, menu_item_id):
    address_id = add_address(client, customer_token)
    add_item_to_cart(client, customer_token, menu_item_id)

    client.post(
        "/orders",
        json={"address_id": address_id},
        headers={"Authorization": f"Bearer {customer_token}"},
    )

    cart_response = client.get("/cart", headers={"Authorization": f"Bearer {customer_token}"})
    assert cart_response.json()["items"] == []


def test_customer_sees_own_orders(client, customer_token, menu_item_id):
    address_id = add_address(client, customer_token)
    add_item_to_cart(client, customer_token, menu_item_id)
    client.post(
        "/orders",
        json={"address_id": address_id},
        headers={"Authorization": f"Bearer {customer_token}"},
    )

    response = client.get("/orders", headers={"Authorization": f"Bearer {customer_token}"})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_owner_can_update_order_status(client, customer_token, owner_token, menu_item_id):
    address_id = add_address(client, customer_token)
    add_item_to_cart(client, customer_token, menu_item_id)
    order_response = client.post(
        "/orders",
        json={"address_id": address_id},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    order_id = order_response.json()["id"]

    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "CONFIRMED"},
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "CONFIRMED"


def test_customer_cannot_update_order_status(client, customer_token, menu_item_id):
    address_id = add_address(client, customer_token)
    add_item_to_cart(client, customer_token, menu_item_id)
    order_response = client.post(
        "/orders",
        json={"address_id": address_id},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    order_id = order_response.json()["id"]

    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "CONFIRMED"},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert response.status_code == 403