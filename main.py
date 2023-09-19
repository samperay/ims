from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def get_item_id(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
       item["q"] = q
    if not short:
        item["description"]="This is an amazing item that has a long description"
    return item


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
