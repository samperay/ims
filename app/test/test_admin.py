from fastapi import status
from app.routers.admin import get_db, get_current_user
from app.test.utils import override_get_db, override_get_current_user, mock_server_inventory, Servers
from app.test.utils import TestingSessionLocal, client, app

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_list_all_authenticated_servers(mock_server_inventory):
    response = client.get("/admin/inventory")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'hostname': 'server1.example.com','ip_address':'192.168.56.101','os_version':'Ubuntu 20.04', 'cpu_cores': 8,'location': 'Data Center 1','status': 'Active','root_disk_type':'SSD', 'used_capacity_gb': 500, 'userid': 1, 'short_name': 'server1', 'os': 'Linux', 'cpu_model': 'Intel Xeon', 'ram_gb': 16, 'owner': 'Admin', 'root_disk': '/dev/sda', 'total_capacity_gb':1000, 'free_capacity_gb': 500, "id": mock_server_inventory.id}]