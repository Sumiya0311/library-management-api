from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional


class MemberBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = Field(
        default=None,
        pattern=r"^\+?[0-9]{10,15}$"
    )
    address: Optional[str] = None
    membership_date: Optional[date] = None
    is_active: bool = True


class MemberCreate(MemberBase):
    pass


class MemberResponse(MemberBase):
    member_id: int

    class Config:
        from_attributes = True