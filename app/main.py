# Description: This is the main file for the FastAPI application. It contains the code for the FastAPI application and the server inventory data.
from fastapi import FastAPI
# from pydantic import BaseModel, Field
from routers import hosts as hosts_router


app=FastAPI()

app.include_router(hosts_router.router)