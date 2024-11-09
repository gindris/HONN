from pydantic import BaseModel


class ProductModel(BaseModel):
    merchantId: int
    productName: str
    price: float
    quantity: int
    reserved: int = 0