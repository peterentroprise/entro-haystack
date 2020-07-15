from pydantic import BaseModel
from typing import Optional

class Question(BaseModel):
    question: str

class ItemData(BaseModel):
    id: str
    content: str
    question: str
    answer: str

class DeliveryInfo(BaseModel):
    max_retries: int
    current_retry: int

class Trigger(BaseModel):
    name: str

class Table(BaseModel):
    name: str

# class SessionVariables(BaseModel):
#     x-hasura-role: str

class Data(BaseModel):
    old: Optional[ItemData] = None
    new: Optional[ItemData] = None

class Event(BaseModel):
    # session_variables: Optional[SessionVariables] = None
    op: str
    data: Optional[Data] = None

class Item(BaseModel):
    event: Optional[Event] = None
    created_at: str
    id: str
    delivery_info: Optional[DeliveryInfo] = None
    trigger: Optional[Trigger] = None
    table: Optional[Table] = None
