import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Patient Registration API"}

def test_register_patient(monkeypatch, tmp_path):
    # Mock email sending
    monkeypatch.setattr("app.email_utils.send_confirmation_email", lambda *a, **kw: None)
    # Create a dummy image file
    img_path = tmp_path / "test.jpg"
    img_path.write_bytes(b"\xff\xd8\xff\xe0" + b"0" * 100)  # minimal JPEG header
    with open(img_path, "rb") as img_file:
        response = client.post(
            "/patients",
            data={
                "name": "Test User",
                "email": "testuser@example.com",
                "phone": "1234567890"
            },
            files={"document_photo": ("test.jpg", img_file, "image/jpeg")}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "testuser@example.com"
    assert data["phone"] == "1234567890"
    assert data["document_photo"].endswith("testuser_at_example.com.jpg") 