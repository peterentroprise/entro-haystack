
from fastapi import APIRouter

from models.item_model import Item
from service import item_service

router = APIRouter()


@router.get("/")
async def read_root():
    return {"Hello": "Universe"}

@router.post("/ask")
async def ask_haystack(item: Item):
    return item_service.ask_haystack(item)
