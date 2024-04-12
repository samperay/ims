# Description: This is the main file for the FastAPI application. It contains the code for the FastAPI application and the server inventory data.
from fastapi import FastAPI
from app.routers import server as server_router
from app.routers import auth as auth_router


app=FastAPI()

app.include_router(server_router.router, prefix="/inventory",tags=["inventory"])
app.include_router(auth_router.router, prefix="/auth",tags=["auth"])