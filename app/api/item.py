
from fastapi import APIRouter

from models.item_model import Item
from models.item_model import Question
from service import item_service

router = APIRouter()


@router.get("/")
async def read_root():
    return {"Hello": "Universe"}

@router.post("/indexitem")
async def index_item(item: Item):
    return item_service.index_item(item)

@router.post("/askquestion")
async def ask_question(question: Question):
    return item_service.ask_question(question)
