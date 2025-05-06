from typing import Optional

from pydantic import BaseModel


class ProductsCreate(BaseModel):
    title: str
    category_id: int
    description: str
    price: float


class ResponseProduct(BaseModel):
    id: int
    category_id: int
    description: str
    price: float


class ProductsID(BaseModel):
    id: int


class ProductsUpdate(ProductsID):
    title: Optional[str]
    category_id: Optional[int]
    description: Optional[str]
    price: Optional[float]
