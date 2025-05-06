from pydantic import BaseModel


class CategoriesCreate(BaseModel):
    title: str


class ResponseProduct(BaseModel):
    id: int
    title: str
