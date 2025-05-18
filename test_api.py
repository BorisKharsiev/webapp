import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app
from models import User, TaskStatus
from security import get_password_hash

# Создаем тестовую базу данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user(client):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def test_token(client, test_user):
    response = client.post("/token", data={
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    return response.json()["access_token"]

def test_create_user(client):
    response = client.post("/users/", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"

def test_create_task(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "pending",
        "priority": 1
    }
    response = client.post("/tasks/", json=task_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["status"] == "pending"
    assert data["priority"] == 1

def test_get_tasks(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_top_tasks(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/tasks/top/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_search_tasks(client, test_token):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/tasks/?search=test", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_invalid_token(client):
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 401 