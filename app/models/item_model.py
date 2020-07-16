from pydantic import BaseModel
from typing import Optional

class Question(BaseModel):
    question: str

class ItemData(BaseModel):
    id: str
    content: str
    question: str
    answer: str


class Data(BaseModel):
    new: ItemData

class Event(BaseModel):
    data: Data

class Payload(BaseModel):
    event: Event