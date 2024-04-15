from sqlalchemy import create_engine, TEXT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app import test
from app.main import app
from fastapi import status
from app.db.database import Base
from app.routers.server import get_db, get_current_user
from fastapi.testclient import TestClient
import pytest
from app.model.models import Servers, Storage, Users

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def override_get_current_user():
    return {"username": "samperay", "id": 1, "user_role": "admin"}
        
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


client = TestClient(app)

@pytest.fixture
def test_inventory():

    server = Servers([
        {
            "ip_address": "192.168.1.1",
            "hostname": "server1",
            "os_version": "Ubuntu 20.04",
            "cpu_cores": 8,
            "location": "Data Center 1",
            "status": "Active",
            "userid": 1,
            "short_name": "s1",
            "id": 1,
            "os": "Linux",
            "cpu_model": "Intel Xeon",
            "ram_gb": 16,
            "owner": "Admin",
            "storage": [
            {
                "free_capacity_gb": "500",
                "id": 1,
                "server_id": 1,
                "total_capacity_gb": "1000",
                "used_capacity_gb": "500",
                "disk_type": "SSD"
            }
            ]
        }])
    
    db = TestingSessionLocal()
    db.add(server)
    db.commit()
    db.refresh(server)
    yield server

    # use teardown to clean up the database
    db.delete(server)
    db.commit()
    db.close()
    

def test_read_all_authenticated(test_inventory):
    response = client.get("/inventory")
    assert response.status_code == status.HTTP_200_OK
    
    assert response.json() == [
  {
    "ip_address": "192.168.1.1",
    "hostname": "server1",
    "os_version": "Ubuntu 20.04",
    "cpu_cores": 8,
    "location": "Data Center 1",
    "status": "Active",
    "userid": 1,
    "short_name": "s1",
    "id": 1,
    "os": "Linux",
    "cpu_model": "Intel Xeon",
    "ram_gb": 16,
    "owner": "Admin",
    "storage": [
      {
        "free_capacity_gb": "500",
        "id": 1,
        "server_id": 1,
        "total_capacity_gb": "1000",
        "used_capacity_gb": "500",
        "disk_type": "SSD"
      }
    ]
  }]
     