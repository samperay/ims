# Description: This is the main file for the FastAPI application. It contains the code for the FastAPI application and the server inventory data.
from fastapi import FastAPI
from app.routers import server as server_router
from app.routers import auth as auth_router
from app.routers import admin as admin_router
from app.routers import users as users_router



app=FastAPI()

@app.get("/healtz")
async def healtz():
    return {"status":"ok"}

app.include_router(server_router.router)
app.include_router(auth_router.router)
app.include_router(admin_router.router)
app.include_router(users_router.router)