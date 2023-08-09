from fastapi import FastAPI, HTTPException
from models import User, Payment
from typing import List
from uuid import UUID, uuid4

api = FastAPI()

dbU: List[User] = [
    User(
        id = "cd0bdffa-9ee1-49a4-93bb-e93fb2e4d085",
        fullname = "John Johnson",
        wallet = 1000,
        currency = "TJS"
    ),
    User(
        id = "13bdecd0-1a4b-43c1-bc60-87a5e4972df5",
        fullname = "Don Carleon",
        wallet = 123.1,
        currency = "TJS"
    )
]

dbP: List[Payment] = [
    Payment(
        id = "cd0bdffa-9ee1-49a4-93bb-87a5e4972df5",
        amount = 123.1,
        currency = "TJS",
        time = 1691554986653,
        sender = "cd0bdffa-9ee1-49a4-93bb-e93fb2e4d085",
        receiver = "13bdecd0-1a4b-43c1-bc60-87a5e4972df5",
    )
]

# @api.post("/payment/?sender={sid}&receiver={rid}")
# async def process_payment()
@api.get("/users/")
async def users():
    return dbU

@api.post('/payment/')
async def add_payment(payment: Payment):
    for p in dbP:
        if p.id == payment.id:
            raise HTTPException(status_code=418)
            return
    sender   = next(user for user in dbU if user.id == payment.sender)
    receiver = next(user for user in dbU if user.id == payment.receiver)
    if sender.wallet - payment.amount >= 0:
        receiver.wallet += payment.amount
        sender.wallet -= payment.amount
        dbP.append(payment)
    return {"status": "success"}

@api.get('/payment/{payment_id}')
async def payment_status(payment_id: UUID):
    for payment in dbP:
        if payment.id == payment_id:
            return {"status": "found"}
    raise HTTPException(
        status_code=404,
        detail=f"Payment with id {payment_id} not found"
    )