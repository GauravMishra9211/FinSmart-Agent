from pydantic import BaseModel, Field
from typing import Optional

class VerifyRequest(BaseModel):
    phone: str
    address: Optional[str] = None

class UnderwriteRequest(BaseModel):
    phone: str
    amount: int
    tenure_months: int = Field(ge=6, le=60)
    salary: Optional[int] = None

class Decision(BaseModel):
    approved: bool
    reason: str
    emi: float = 0.0
    rate_pa: float = 14.0
    approval_id: Optional[str] = None
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None

class SanctionRequest(BaseModel):
    approval_id: str
    customer_name: str
    amount: int
    tenure_months: int
    rate_pa: float
    emi: float
