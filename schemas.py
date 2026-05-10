from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    title: str
    price: float
    taxes: float
    ads: float
    discount: float
    category: str
