from pydantic import BaseModel

class Item(BaseModel):
    id: str
    question: str
    answer: str
    content: str

class Question(BaseModel):
    question: str