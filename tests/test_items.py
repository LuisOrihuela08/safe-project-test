import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.store import store

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_store():
    """Wipe the store before each test for isolation."""
    store.clear()
    yield
    store.clear()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_item():
    payload = {"name": "Widget A", "price": 9.99, "stock": 50}
    response = client.post("/items/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Widget A"
    assert data["price"] == 9.99
    assert data["stock"] == 50
    assert "id" in data


def test_list_items_empty():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_items():
    client.post("/items/", json={"name": "Item 1", "price": 1.0})
    client.post("/items/", json={"name": "Item 2", "price": 2.0})
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_item():
    created = client.post("/items/", json={"name": "Gadget", "price": 19.99}).json()
    response = client.get(f"/items/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Gadget"


def test_get_item_not_found():
    response = client.get("/items/99999")
    assert response.status_code == 404


def test_update_item():
    created = client.post("/items/", json={"name": "Old Name", "price": 5.0}).json()
    response = client.put(f"/items/{created['id']}", json={"name": "New Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"
    assert response.json()["price"] == 5.0


def test_update_item_not_found():
    response = client.put("/items/99999", json={"name": "Ghost"})
    assert response.status_code == 404


def test_delete_item():
    created = client.post("/items/", json={"name": "To Delete", "price": 3.0}).json()
    response = client.delete(f"/items/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/items/{created['id']}").status_code == 404


def test_delete_item_not_found():
    response = client.delete("/items/99999")
    assert response.status_code == 404


def test_inactive_item_not_listed():
    created = client.post("/items/", json={"name": "Hidden", "price": 1.0}).json()
    client.put(f"/items/{created['id']}", json={"active": False})
    items = client.get("/items/").json()
    ids = [i["id"] for i in items]
    assert created["id"] not in ids
