from app.db.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship


class Servers(Base):
    __tablename__ = 'servers'
    
    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String)
    short_name = Column(String)
    ip_address = Column(String)
    os= Column(String)
    os_version = Column(String)
    cpu_model = Column(String)
    cpu_cores = Column(Integer)
    ram_gb = Column(Integer)
    location = Column(String)
    owner=Column(String)
    status=Column(String)
    storage=Column(String)
    
    storage = relationship("Storage", back_populates="server")
    
     
class Storage(Base):
    __tablename__ = 'storage'
    id = Column(Integer, primary_key=True, index=True)
    total_capacity_gb = Column(String)
    used_capacity_gb = Column(String)
    free_capacity_gb = Column(String)
    disk_type = Column(String)
    server_id = Column(Integer, ForeignKey('servers.id'))
    
    server = relationship("Servers", back_populates="storage")
    
    
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    