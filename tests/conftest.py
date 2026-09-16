from sqlalchemy.pool import StaticPool
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.db.session import Base, get_db

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def customer_token(client):
    client.post("/auth/register", json={
        "first_name": "Test", "last_name": "Customer",
        "email": "cust@example.com", "phone_number": "9876543210",
        "password": "test123", "role": "CUSTOMER",
    })
    response = client.post("/auth/login", json={"email": "cust@example.com", "password": "test123"})
    return response.json()["access_token"]


@pytest.fixture
def owner_token(client):
    client.post("/auth/register", json={
        "first_name": "Test", "last_name": "Owner",
        "email": "owner@example.com", "phone_number": "9876543211",
        "password": "test123", "role": "RESTAURANT_OWNER",
    })
    response = client.post("/auth/login", json={"email": "owner@example.com", "password": "test123"})
    return response.json()["access_token"]


@pytest.fixture
def menu_item_id(client, owner_token):
    restaurant_response = client.post(
        "/restaurants",
        json={
            "name": "Test Restaurant",
            "description": "Test",
            "address": {"display_name": "Test Address", "latitude": 28.99, "longitude": 77.01},
            "cuisine_type": "Test",
            "image_url": None,
            "category_id": None,
        },
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    restaurant_id = restaurant_response.json()["id"]

    item_response = client.post(
        f"/restaurants/{restaurant_id}/menu",
        json={
            "name": "Test Dish",
            "description": "Test",
            "price": 100.0,
            "image_url": None,
            "category_id": None,
            "is_available": True,
        },
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    return item_response.json()["id"]