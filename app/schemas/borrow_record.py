from pydantic import BaseModel
from datetime import date
from typing import Optional


class BorrowRecordBase(BaseModel):
    book_id: int
    member_id: int
    borrow_date: date
    due_date: date
    return_date: Optional[date] = None
    status: str = "Borrowed"


class BorrowRecordCreate(BorrowRecordBase):
    pass


class BorrowRecordResponse(BorrowRecordBase):
    borrow_id: int

    class Config:
        from_attributes = True