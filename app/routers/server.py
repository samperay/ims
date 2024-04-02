# Description: This is the main file for the FastAPI application. It contains the code for the FastAPI application and the server inventory data.
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


router=APIRouter()

class Storage(BaseModel):
    total_capacity_gb: int = Field(gt=0,le=10000, description="Total storage capacity in GB")
    used_capacity_gb: int = Field(ge=0,le=10000, description="Used storage capacity in GB")
    free_capacity_gb: int = Field(ge=0,le=10000, description="Free storage capacity in GB")
    disk_type: str = Field(description="Type of disk storage (e.g. SSD, HDD)")

class Server(BaseModel):
    hostname: str
    short_name: str
    ip_address: str
    os: str
    os_version: str
    cpu_model: str
    cpu_cores: int
    ram_gb: int
    storage: Storage
    location: str
    owner: str
    status: str

server_database = {
  "servers": [
    {
      "hostname": "server1.example.com",
      "short_name": "server1",
      "ip_address": "192.168.1.101",
      "os": "Linux",
      "os_version": "Ubuntu 20.04",
      "cpu_model": "Intel Xeon E5-2670",
      "cpu_cores": 8,
      "ram_gb": 16,
      "storage": {
        "total_capacity_gb": 500,
        "used_capacity_gb": 200,
        "free_capacity_gb": 300,
        "disk_type": "SSD"
      },
      "location": "Data Center A",
      "owner": "IT Department",
      "status": "active"
    },
    {
      "hostname": "server2.example.com",
      "short_name": "server2",
      "ip_address": "192.168.1.102",
      "os": "Windows",
      "os_version": "Windows Server 2019",
      "cpu_model": "Intel Core i7-8700",
      "cpu_cores": 6,
      "ram_gb": 32,
      "storage": {
        "total_capacity_gb": 1000,
        "used_capacity_gb": 400,
        "free_capacity_gb": 600,
        "disk_type": "HDD"
      },
      "location": "Data Center B",
      "owner": "Finance Department",
      "status": "active"
    }
  ]
}



@router.get("/")
def list_server_inventory():
    return server_database.get("servers")


@router.get("/server/{hostname}", response_model=Server, status_code=200)
async def get_server_by_hostname(hostname: str):
    for server in server_database.get("servers"):
        if server.get("hostname") == hostname or server.get("short_name") == hostname.split(".")[0]:
            return server
    raise HTTPException(status_code=404, detail="Server not found")
        
@router.post("/server", response_model=Server, status_code=201)
async def add_server_to_inventory(server: dict):
    server_database.get("servers").append(server)
    return server


@router.delete("/server/{hostname}", status_code=204)
async def delete_server_from_inventory(hostname: str):
    for server in server_database.get("servers"):
        if server.get("hostname") == hostname or server.get("short_name") == hostname.split(".")[0]:
            server_database.get("servers").remove(server)
            return {"message": "Server deleted successfully"}
    raise HTTPException(status_code=404, detail="Server not found")

@router.put("/server/{hostname}", response_model=Server, status_code=201)
async def update_server_inventory(hostname: str, server: Server):
    for server_data in server_database.get("servers"):
        if server_data.get("hostname") == hostname or server_data.get("short_name") == hostname.split(".")[0]:
            server_data.update(server.model_dump())
            return server_data
        raise HTTPException(status_code=404, detail="server not found")