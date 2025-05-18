import pytest
from datetime import datetime
from models import Task, User, TaskStatus
from security import get_password_hash, verify_password, create_access_token

def test_password_hashing():
    password = "testpassword"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)

def test_token_creation():
    data = {"sub": "testuser"}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0

def test_task_creation():
    task = Task(
        title="Test Task",
        description="Test Description",
        status=TaskStatus.PENDING,
        priority=1
    )
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == TaskStatus.PENDING
    assert task.priority == 1
    assert isinstance(task.created_at, datetime)

def test_user_creation():
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("password123")
    )
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert verify_password("password123", user.hashed_password) 