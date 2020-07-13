from pydantic import BaseModel

class Item(BaseModel):
    question: str
    answer: str
    content: str

class Question(BaseModel):
    question: str