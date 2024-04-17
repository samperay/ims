from fastapi.testclient import TestClient
from app.main import app
from fastapi import status

client = TestClient(app)

def test_healtz():
    response = client.get("/healtz")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status":"ok"}

def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message":"Welcome to the Server Inventory API"}