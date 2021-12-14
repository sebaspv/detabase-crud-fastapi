from dotenv import dotenv_values
from deta import Deta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

deta_key = dotenv_values(".env")["DETA_PROJECT_KEY"]
deta = Deta(deta_key)
deta_db = deta.Base("sampleDB")

app = FastAPI()


class SampleSchema(BaseModel):
    name: str
    price: int


@app.post("/items")
async def create_item(item: SampleSchema):
    item = deta_db.put({"name": item.name, "price": item.price})
    return {"message": "Item created successfully"}


@app.get("/items/{key}")
async def get_item(key):
    item = deta_db.get(key)
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/items")
async def get_items():
    items = deta_db.fetch()
    return items


@app.delete("/items/{key}")
async def delete_item(key):
    deta_db.delete(key)
    return {"message": f"Item with key {key} deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
