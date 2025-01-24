from pydantic import ConfigDict, BaseModel


class ProductSchema(BaseModel):
    name: str
    artikul: int
    price: int
    rating: float
    quantity: int


class ProductItemSchema(BaseModel):
    artikul: int