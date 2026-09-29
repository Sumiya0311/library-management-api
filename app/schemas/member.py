from pydantic import BaseModel
from datetime import date

class MemberBase(BaseModel):
    name: str
    email: str
    phone: str | None = None
    address: str | None = None
    membership_date: date | None = None
    is_active: bool = True

class MemberCreate(MemberBase):
    pass

class MemberResponse(MemberBase):
    member_id: int
    
class Config:
    from_attributes = True 