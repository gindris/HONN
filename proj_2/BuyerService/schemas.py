from pydantic import BaseModel

class BuyerBase(BaseModel):
    name: str
    ssn: str
    email: str
    phoneNumber: str
    allowsDiscount: bool

class BuyerCreate(BuyerBase):
    pass

class BuyerResponse(BuyerBase):
    id: int

    class Config:
        from_attributes = True  # Updated this line
