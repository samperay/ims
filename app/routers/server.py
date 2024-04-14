from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from app.db.database import engine, sessionLocal
import app.model.models as models
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.db.curd import get_server_by_hostname
from .auth import get_current_user


router=APIRouter(prefix="/inventory",tags=["inventory"])


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
        
class Storage(BaseModel):
    total_capacity_gb: int = Field(gt=0,le=10000, description="Total storage capacity in GB")
    used_capacity_gb: int = Field(ge=0,le=10000, description="Used storage capacity in GB")
    free_capacity_gb: int = Field(ge=0,le=10000, description="Free storage capacity in GB")
    disk_type: str = Field(description="Type of disk storage (e.g. SSD, HDD)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_capacity_gb": 500,
                "used_capacity_gb": 200,
                "free_capacity_gb": 300,
                "disk_type": "SSD"
            }
        }

class Server(BaseModel):
    hostname: str = Field(description="Fully qualified domain name (FQDN) of the server")
    short_name: str = Field(description="Short name of the server")
    ip_address: str = Field(description="IP address of the server")
    os: str = Field(description="Operating system of the server")
    os_version: str = Field(description="Version of the operating system")
    cpu_model: str = Field(description="Model of the CPU")
    cpu_cores: int = Field(gt=0,le=108, description="Number of CPU cores")
    ram_gb: int = Field(gt=0,le=1000, description="Amount of RAM in GB")
    storage: Storage = Field(description="Storage details")
    location: str = Field(description="Location of the server")
    owner: str = Field(description="Owner of the server")
    status: str = Field(description="Status of the server")
    userid: int = Field(description="User ID of the user who added the server inventory")
    
    class Config:
        json_schema_extra = {
          "example": {
            "hostname": "server3.example.com",
            "short_name": "server3",
            "ip_address": "192.168.56.103",
            "os": "Linux",
            "os_version": "Ubuntu 20.04",
            "cpu_model": "Intel Xeon E5-2670",
            "cpu_cores": 8,
            "ram_gb": 16,
            "userid": 1,
            "storage": {
              "total_capacity_gb": 500,
              "used_capacity_gb": 200,
              "free_capacity_gb": 300,
              "disk_type": "SSD"
            },
            "location": "Data Center A",
            "owner": "IT Department",
            "status": "active"
            
        }
        }



@router.get("/", status_code=status.HTTP_200_OK, description="List all servers in inventory")
async def list_all_servers(db: db_dependency): 
    servers = db.query(models.Servers).options(joinedload(models.Servers.storage)).all()   
    # servers = db.query(models.Servers).options(joinedload(models.Servers.storage)).filter(models.Servers.userid == user.get("id")).all()
    if servers is None:
        raise HTTPException(status_code=404, detail="No servers found")
    return servers

@router.get("/{hostname}", status_code=status.HTTP_200_OK, description="Get server by hostname")
async def get_server_by_hostname(hostname:str, db:db_dependency):
    server = db.query(models.Servers).filter(models.Servers.hostname == hostname).first()
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    return db.query(models.Servers).filter(models.Servers.hostname == hostname).options(joinedload(models.Servers.storage)).first()


@router.post("/", status_code=status.HTTP_201_CREATED, description="Create new server to inventory")
async def create_server(server_data:Server, db:db_dependency, user:user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    server = models.Servers(
        hostname=server_data.hostname,
        short_name=server_data.short_name,
        ip_address=server_data.ip_address,
        os=server_data.os,
        os_version=server_data.os_version,
        cpu_model=server_data.cpu_model,
        cpu_cores=server_data.cpu_cores,
        ram_gb=server_data.ram_gb,
        location=server_data.location,
        owner=server_data.owner,
        status=server_data.status,
        userid=user.get("id")
    )
    
    storage_data = server_data.storage
    storage = models.Storage(
        disk_type=storage_data.disk_type,
        free_capacity_gb=storage_data.free_capacity_gb,
        total_capacity_gb=storage_data.total_capacity_gb,
        used_capacity_gb=storage_data.used_capacity_gb
    )
    
    server.storage.append(storage)
    
    db.add(server)
    db.add(storage)
    db.commit()
    db.refresh(server)
    
    return server

@router.put("/{hostname}", status_code=status.HTTP_200_OK, description="Update an existing server inventory")
async def update_server(hostname:str, server_data:Server, db:db_dependency):
    server = db.query(models.Servers).filter(models.Servers.hostname == hostname).first()
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    
    server.short_name = server_data.short_name
    server.ip_address = server_data.ip_address
    server.os = server_data.os
    server.os_version = server_data.os_version
    server.cpu_model = server_data.cpu_model
    server.cpu_cores = server_data.cpu_cores
    server.ram_gb = server_data.ram_gb
    server.location = server_data.location
    server.owner = server_data.owner
    server.status = server_data.status
    
    storage_data = server_data.storage
    storage = db.query(models.Storage).filter(models.Storage.server_id == server.id).first()
    storage.disk_type = storage_data.disk_type
    storage.free_capacity_gb = storage_data.free_capacity_gb
    storage.total_capacity_gb = storage_data.total_capacity_gb
    storage.used_capacity_gb = storage_data.used_capacity_gb
    
    db.commit()
    db.refresh(server)
    
    return server

@router.delete("/{hostname}", status_code=status.HTTP_200_OK, description="Delete an existing server from inventory")
async def delete_server(hostname:str, db:db_dependency):
    server = db.query(models.Servers).filter(models.Servers.hostname == hostname).first()
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    
    db.delete(server)
    db.commit()
    
    return {"message": "Server deleted successfully"}
    
