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
from app.model.models import Servers

SQLALCHEMY_DATABASE_URL = "sqlite:///./imstestdb.db"

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
    return {"username": "user1", "id": 1, "user_role": "admin"}
        
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


client = TestClient(app)

@pytest.fixture
def test_inventory():
    server = Servers(hostname="server1.example.com", ip_address="192.168.56.101", os_version="Ubuntu 20.04", cpu_cores=8, location="Data Center 1", status="Active", short_name="server1", os="Linux", cpu_model="Intel Xeon", ram_gb=16, owner="Admin", userid=1,root_disk="/dev/sda",root_disk_type="SSD",total_capacity_gb=1000,used_capacity_gb=500,free_capacity_gb=500)
    
    db = TestingSessionLocal()
    db.add(server)
    db.commit()
    db.refresh(server)
    yield server
        
    db.delete(server)
    db.commit()
    db.close()
    

def test_read_all_server_inventory(test_inventory):
    response = client.get("/inventory")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'hostname': 'server1.example.com','ip_address':'192.168.56.101','os_version':'Ubuntu 20.04', 'cpu_cores': 8,'location': 'Data Center 1','status': 'Active','root_disk_type':'SSD', 'used_capacity_gb': 500, 'userid': 1, 'short_name': 'server1', 'os': 'Linux', 'cpu_model': 'Intel Xeon', 'ram_gb': 16, 'owner': 'Admin', 'root_disk': '/dev/sda', 'total_capacity_gb':1000, 'free_capacity_gb': 500, "id": test_inventory.id}]
    

def test_read_one_server_inventory(test_inventory):
    response = client.get("/inventory/server1.example.com")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'hostname': 'server1.example.com', 'ip_address': '192.168.56.101', 'os_version': 'Ubuntu 20.04', 'cpu_cores': 8, 'location': 'Data Center 1', 'status': 'Active', 'root_disk_type': 'SSD', 'used_capacity_gb': 500, 'userid': 1, 'short_name': 'server1', 'os': 'Linux', 'cpu_model': 'Intel Xeon', 'ram_gb': 16, 'owner': 'Admin', 'root_disk': '/dev/sda', 'total_capacity_gb': 1000, 'free_capacity_gb':500, "id": test_inventory.id}
        

def test_read_one_server_inventory_not_found(test_inventory):
    response = client.get("/inventory/server99.example.com")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Server not found'}
    
    
def test_create_server_inventory(test_inventory):
    new_server_details = {
        "hostname": "server2.example.com",
        "short_name": "server2",
        "ip_address": "192.168.56.102",
        "os": "Linux",
        "os_version": "Ubuntu 20.04",
        "cpu_model": "Intel Xeon E5-2670",
        "cpu_cores": 8,
        "ram_gb": 16,
        "location": "Data Center A",
        "owner": "IT Department",
        "status": "active",
        "root_disk": "/dev/sda",
        "root_disk_type": "SSD",
        "total_capacity_gb": 1000,
        "used_capacity_gb": 500,
        "free_capacity_gb": 500,
        "userid": 1
    }
    
    response = client.post("/inventory", json=new_server_details)
    assert response.status_code == status.HTTP_201_CREATED
    