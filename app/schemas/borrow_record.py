from pydantic import BaseModel
from datetime import date

class BorrowRecordBase(BaseModel):
    book_id: int
    member_id: int
    borrow_date: date
    due_date: date
    return_date: date | None = None
    status: str | None = "Borrowed"

class BorrowRecordCreate(BorrowRecordBase):
    pass

class BorrowRecordResponse(BorrowRecordBase):
    borrow_id: int
    
    class Config:
        from_attributes = True