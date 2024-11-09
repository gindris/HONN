from pydantic import BaseModel

class MerchantBase(BaseModel):
    name: str
    ssn: str
    email: str
    phoneNumber: str
    allowsDiscount: bool

class MerchantCreate(MerchantBase):
    pass

class MerchantResponse(MerchantBase):
    id: int

    class Config:
        from_attributes = True  # Updated this line
