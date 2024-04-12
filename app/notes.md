## Pydantic v1 vs Pydantic v2

- `.dict()` function is now renamed to `.model_dump()`

- `schema_extra` function within a Config class is now renamed to `json_schema_extra`

- `Optional` variables need a `=None` example: id: Optional[int] = None





## development test data

<!-- # server_database = {
#   "servers": [
#     {
#       "hostname": "server1.example.com",
#       "short_name": "server1",
#       "ip_address": "192.168.1.101",
#       "os": "Linux",
#       "os_version": "Ubuntu 20.04",
#       "cpu_model": "Intel Xeon E5-2670",
#       "cpu_cores": 8,
#       "ram_gb": 16,
#       "storage": {
#         "total_capacity_gb": 500,
#         "used_capacity_gb": 200,
#         "free_capacity_gb": 300,
#         "disk_type": "SSD"
#       },
#       "location": "Data Center A",
#       "owner": "IT Department",
#       "status": "active"
#     },
#     {
#       "hostname": "server2.example.com",
#       "short_name": "server2",
#       "ip_address": "192.168.1.102",
#       "os": "Windows",
#       "os_version": "Windows Server 2019",
#       "cpu_model": "Intel Core i7-8700",
#       "cpu_cores": 6,
#       "ram_gb": 32,
#       "storage": {
#         "total_capacity_gb": 1000,
#         "used_capacity_gb": 400,
#         "free_capacity_gb": 600,
#         "disk_type": "HDD"
#       },
#       "location": "Data Center B",
#       "owner": "Finance Department",
#       "status": "active"
#     }
#   ]
# } -->


<!-- # @router.get("/")
# def list_server_inventory():
#     return server_database.get("servers") -->


<!-- # @router.get("/server/{hostname}", response_model=Server, status_code=200)
# async def get_server_by_hostname(hostname: str):
#     for server in server_database.get("servers"):
#         if server.get("hostname") == hostname or server.get("short_name") == hostname.split(".")[0]:
#             return server
#     raise HTTPException(status_code=404, detail="Server not found")
        
# @router.post("/server", response_model=Server, status_code=201)
# async def add_server_to_inventory(server: dict):
#     server_database.get("servers").append(server)
#     return server


# @router.delete("/server/{hostname}", status_code=204)
# async def delete_server_from_inventory(hostname: str):
#     for server in server_database.get("servers"):
#         if server.get("hostname") == hostname or server.get("short_name") == hostname.split(".")[0]:
#             server_database.get("servers").remove(server)
#             return {"message": "Server deleted successfully"}
#     raise HTTPException(status_code=404, detail="Server not found")

# @router.put("/server/{hostname}", response_model=Server, status_code=201)
# async def update_server_inventory(hostname: str, server: Server):
#     for server_data in server_database.get("servers"):
#         if server_data.get("hostname") == hostname or server_data.get("short_name") == hostname.split(".")[0]:
#             server_data.update(server.model_dump())
#             return server_data
#         raise HTTPException(status_code=404, detail="server not found") -->


<!-- CREATE TABLE servers (
    id INTEGER PRIMARY KEY,
    hostname TEXT,
    short_name TEXT,
    ip_address TEXT,
    os TEXT,
    os_version TEXT,
    cpu_model TEXT,
    cpu_cores INTEGER,
    ram_gb INTEGER,
    location TEXT,
    owner TEXT,
    status TEXT,
    userid TEXT
);

CREATE TABLE storage (
    id INTEGER PRIMARY KEY,
    server_id INTEGER,
    total_capacity_gb TEXT,
    used_capacity_gb TEXT,
    free_capacity_gb TEXT,
    disk_type TEXT,
    FOREIGN KEY (server_id) REFERENCES servers(id)
); -->


<!-- INSERT INTO servers (hostname, short_name, ip_address, os, os_version, cpu_model, cpu_cores, ram_gb, location, owner, status, userid)
VALUES 
    ('server1', 's1', '192.168.1.1', 'Linux', 'Ubuntu 20.04', 'Intel Xeon', 8, 16, 'Data Center 1', 'Admin', 'Active',1),
    ('server2', 's2', '192.168.1.2', 'Windows', 'Windows Server 2019', 'AMD Ryzen', 6, 32, 'Data Center 2', 'Dev', 'Active',1),
    ('server3', 's3', '192.168.1.3', 'Linux', 'CentOS 7', 'ARM Cortex', 4, 8, 'Office', 'User', 'Inactive',2);


INSERT INTO storage (server_id, total_capacity_gb, used_capacity_gb, free_capacity_gb, disk_type)
VALUES
    (1, '1000', '500', '500', 'SSD'),
    (2, '2000', '1500', '500', 'HDD'),
    (3, '500', '300', '200', 'SSD'); -->