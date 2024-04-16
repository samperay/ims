from fastapi import status
from app.routers.server import get_db, get_current_user
from app.test.utils import override_get_db, override_get_current_user, mock_server_inventory, Servers
from app.test.utils import TestingSessionLocal, client, app

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_list_all_servers(mock_server_inventory):
    response = client.get("/inventory")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'hostname': 'server1.example.com','ip_address':'192.168.56.101','os_version':'Ubuntu 20.04', 'cpu_cores': 8,'location': 'Data Center 1','status': 'Active','root_disk_type':'SSD', 'used_capacity_gb': 500, 'userid': 1, 'short_name': 'server1', 'os': 'Linux', 'cpu_model': 'Intel Xeon', 'ram_gb': 16, 'owner': 'Admin', 'root_disk': '/dev/sda', 'total_capacity_gb':1000, 'free_capacity_gb': 500, "id": mock_server_inventory.id}]
    

def test_list_one_server(mock_server_inventory):
    response = client.get("/inventory/server1.example.com")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'hostname': 'server1.example.com', 'ip_address': '192.168.56.101', 'os_version': 'Ubuntu 20.04', 'cpu_cores': 8, 'location': 'Data Center 1', 'status': 'Active', 'root_disk_type': 'SSD', 'used_capacity_gb': 500, 'userid': 1, 'short_name': 'server1', 'os': 'Linux', 'cpu_model': 'Intel Xeon', 'ram_gb': 16, 'owner': 'Admin', 'root_disk': '/dev/sda', 'total_capacity_gb': 1000, 'free_capacity_gb':500, "id": mock_server_inventory.id}
        

def test_list_server_not_found(mock_server_inventory):
    response = client.get("/inventory/server99.example.com")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Server not found'}
    
    
def test_create_server(mock_server_inventory):
    new_request = {
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
    
    response = client.post("/inventory", json=new_request)
    assert response.status_code == status.HTTP_201_CREATED
    
    db=TestingSessionLocal()
    server_model = db.query(Servers).filter(Servers.id==2).first()
    assert server_model.hostname == "server2.example.com"
    assert server_model.ip_address == "192.168.56.102"
    assert server_model.os_version == "Ubuntu 20.04"
    assert server_model.cpu_cores == 8
    assert server_model.location == "Data Center A"
    assert server_model.status == "active"
    assert server_model.short_name == "server2"
    assert server_model.os == "Linux"
    assert server_model.cpu_model == "Intel Xeon E5-2670"
    assert server_model.ram_gb == 16
    assert server_model.owner == "IT Department"
    assert server_model.userid == 1
    assert server_model.root_disk == "/dev/sda"
    assert server_model.root_disk_type == "SSD"
    assert server_model.total_capacity_gb == 1000
    assert server_model.used_capacity_gb == 500
    assert server_model.free_capacity_gb == 500
    

def test_update_server(mock_server_inventory):
    update_request = {
        "hostname": "update_server.example.com",
        "short_name": "update_server",
        "ip_address": "192.168.100.1",
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
    
    response = client.put("/inventory/server1.example.com", json=update_request)
    assert response.status_code == status.HTTP_200_OK
    
    db = TestingSessionLocal()
    server_model = db.query(Servers).filter(Servers.id==1).first()
    assert server_model.hostname == "update_server.example.com"
    

def test_update_server_not_found(mock_server_inventory):
    update_request = {
        "hostname": "update_server.example.com",
        "short_name": "update_server",
        "ip_address": "192.168.100.1",
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
    
    response = client.put("/inventory/ser999", json=update_request)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Server not found'}
    
    
def test_delete_server(mock_server_inventory):
    response = client.delete("/inventory/server1.example.com")
    assert response.status_code == status.HTTP_200_OK
    
    db = TestingSessionLocal()
    server_model = db.query(Servers).filter(Servers.id==1).first()
    assert server_model is None
    
def test_delete_server_not_found(mock_server_inventory):
    response = client.delete("/inventory/ser1.example.com")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Server not found'}
