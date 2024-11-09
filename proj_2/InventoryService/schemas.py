from pydantic import BaseModel

class ProductBase(BaseModel):
    merchantId: int
    productName: str
    price: float
    quantity: int
    reserved: int = 0

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True  # Updated this line
