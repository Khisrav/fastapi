from pydantic import BaseModel
from enum import Enum
from uuid import UUID, uuid4
from typing import Optional

class User(BaseModel):
    id: Optional[UUID] = uuid4()
    fullname: str
    wallet: float
    currency: str

class Payment(BaseModel):
    id: Optional[UUID] = uuid4()
    amount: float
    currency: str
    time: int
    sender: UUID
    receiver: UUID
