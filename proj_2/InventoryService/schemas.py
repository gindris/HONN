from pydantic import BaseModel

class ProductBase(BaseModel):
    merchantId: int
    productName: str
    price: float
    quantity: int
    reserved: int

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
