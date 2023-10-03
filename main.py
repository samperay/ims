from dataclasses import dataclass
import uuid
from fastapi import Body, FastAPI
from uuid import UUID
import uvicorn
from faker import Faker


# create a faker object for generating fake data
fake = Faker()


# fastapi application instance
app = FastAPI()

# Create class object for inventory and initialize


@dataclass
class Server:
    id: int
    host_name: str
    domain_name: str
    server_type: str
    hosted_on: str
    region_on: str
    os_type: str
    os_version: str
    cpu: str
    ram: str
    storage: str
    cpu_cores: int
    disk_type: str
    disk_size: str
    uuid: UUID
    serial_number: str
    manufacturer: str
    model: str
    public_ip_address: str
    private_ip_address: str
    disk_partitions: list[dict]
    network_interfaces: list


INVENTORY = [Server(1,
                    "laptop-60.diaz-jennings.com",
                    "cunningham.net",
                    "virtual",
                    "lt-55.hess.info",
                    "Mumbai",
                    "linux",
                    "ubuntu 20.04",
                    "intel i5",
                    "8gb",
                    "1tb",
                    4,
                    "ssd",
                    "1tb",
                    "91bc6650-151a-42eb-b7cb-e6c7ec99e0e2",
                    "123456789",
                    "dell",
                    "poweredge",
                    "106.31.149.235",
                    "172.29.183.71",
                    [{"name": "/dev/sda1", "size": "1tb", "mount_point": "/"},
                     {"name": "/dev/sda2", "size": "1tb", "mount_point": "/home"}],
                    [{"name": "eth0", "mac_address": "d9:11:59:28:40:2e", "ip_address": "177.132.37.144"}, {"name": "eth1", "mac_address": "3a:2e:a9:69:4c:49", "ip_address": "103.1.14.130"}])]


@app.get("/api/v1/inventory")
async def read_inventory():
    print(INVENTORY)
    return INVENTORY


@app.get("/api/v1/inventory/{id}")
async def read_inventory_by_id(id: int):
    for each_server in INVENTORY:
        if each_server.id == id:
            return each_server
        else:
            return {"msg": "id not found"}


@app.post("/api/v1/inventory")
async def create_inventory(new_inventory=Body()):
    for item in INVENTORY:
        if item.id == new_inventory["id"]:
            return {"msg": "id already exists"}
    INVENTORY.append(new_inventory)
    return {"msg": "server added to inventory successfully"}


@app.put("/api/v1/inventory")
async def update_inventory(inventory: dict, id: int):
    for item in INVENTORY:
        if item.id == id:
            item.host_name = inventory["host_name"]
            item.domain_name = inventory["domain_name"]
            item.server_type = inventory["server_type"]
            item.hosted_on = inventory["hosted_on"]
            item.region_on = inventory["region_on"]
            item.os_type = inventory["os_type"]
            item.os_version = inventory["os_version"]
            item.cpu = inventory["cpu"]
            item.ram = inventory["ram"]
            item.storage = inventory["storage"]
            item.cpu_cores = inventory["cpu_cores"]
            item.disk_type = inventory["disk_type"]
            item.disk_size = inventory["disk_size"]
            item.uuid = inventory["uuid"]
            item.serial_number = inventory["serial_number"]
            item.manufacturer = inventory["manufacturer"]
            item.model = inventory["model"]
            item.public_ip_address = inventory["public_ip_address"]
            item.private_ip_address = inventory["private_ip_address"]
            item.disk_partitions = inventory["disk_partitions"]
            item.network_interfaces = inventory["network_interfaces"]
            return {"msg": "item updated successfully"}
    return {"msg": "id not found"}


@app.delete("/api/v1/inventory")
async def delete_inventory(id: int):
    for item in INVENTORY:
        if item.id == id:
            INVENTORY.remove(item)
            return {"msg": "item deleted successfully"}
    return {"error": "id not found"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
