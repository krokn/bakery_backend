from typing import List

from pydantic import BaseModel


class Item(BaseModel):
    count: int
    id: int
    imageUrl: str
    isAdded: bool
    name: str
    price: float

class OrderCreate(BaseModel):
    items: List[Item]
    totalPrice: float
