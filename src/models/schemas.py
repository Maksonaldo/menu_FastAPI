from pydantic import BaseModel


class MenuCreate(BaseModel):
    title: str
    description: str


class SubenuCreate(BaseModel):
    title: str
    description: str


class DishCreate(BaseModel):
    title: str
    description: str
    price: str
