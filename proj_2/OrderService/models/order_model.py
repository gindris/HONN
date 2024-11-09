from pydantic import BaseModel

class CreditCardModel(BaseModel):
    cardNumber: str
    expirationMonth: int
    expirationYear: int
    cvc: int

class OrderModel(BaseModel):
    productId: int
    merchantId: int
    buyerId: int
    creditCard: CreditCardModel
    discount: float

