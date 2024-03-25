from fastapi import FastAPI


app=FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Welcome to server inventory management systems"}

