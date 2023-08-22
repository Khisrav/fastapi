from pydantic import BaseModel
from enum import Enum
from uuid import UUID, uuid4
from typing import Optional
import time

class Payment(BaseModel):
    id: Optional[int]
    uuid: Optional[UUID] = uuid4()
    amount: Optional[float] = 0
    currency: Optional[str] = "TJS"
    time: Optional[int] = time.time()
    wallet_id: int
    service_id: int
