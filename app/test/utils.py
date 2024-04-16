"""Reusable code for testing."""

from sqlalchemy import create_engine
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.database import Base
from fastapi.testclient import TestClient
from app.main import app
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

client = TestClient(app)

@pytest.fixture
def mock_server_inventory():
    server = Servers(hostname="server1.example.com", ip_address="192.168.56.101", os_version="Ubuntu 20.04", cpu_cores=8, location="Data Center 1", status="Active", short_name="server1", os="Linux", cpu_model="Intel Xeon", ram_gb=16, owner="Admin", userid=1,root_disk="/dev/sda",root_disk_type="SSD",total_capacity_gb=1000,used_capacity_gb=500,free_capacity_gb=500)
    
    db = TestingSessionLocal()
    db.add(server)
    db.commit()
    db.refresh(server)
    yield server
        
    with engine.connect() as con:
        con.execute(sa.text("DELETE FROM servers;"))
        con.commit()
    con.close()