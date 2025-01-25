from datetime import datetime
from pydantic import BaseModel


class Product(BaseModel):
    artikul: int


class ProductInDB(Product):
    name: str
    price: float
    rating: float
    count: int

    class Config:
        from_attributes = True


class ProductResponse(ProductInDB):
    id: int
    created_at: datetime
