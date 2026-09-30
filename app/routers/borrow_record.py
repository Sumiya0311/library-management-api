from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models.borrow_record import BorrowRecord
from app.models.book import Book
from app.models.member import Member
from app.schemas.borrow_record import (
    BorrowRecordCreate,
    BorrowRecordResponse
)


router = APIRouter(
    prefix="/borrow-records",
    tags=["Borrow Records"]
)


# 1. BORROW BOOK
@router.post("/", response_model=BorrowRecordResponse)
def create_borrow_record(
    record: BorrowRecordCreate,
    db: Session = Depends(get_db)
):
    book = (
        db.query(Book)
        .filter(Book.book_id == record.book_id)
        .first()
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    member = (
        db.query(Member)
        .filter(Member.member_id == record.member_id)
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    if not member.is_active:
        raise HTTPException(
            status_code=400,
            detail="Member is not active"
        )

    if book.available_copies <= 0:
        raise HTTPException(
            status_code=400,
            detail="No available copies of this book"
        )

    new_record = BorrowRecord(
        book_id=record.book_id,
        member_id=record.member_id,
        borrow_date=record.borrow_date,
        due_date=record.due_date,
        return_date=None,
        status="Borrowed"
    )

    book.available_copies -= 1

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


# 2. GET ALL BORROW RECORDS
@router.get("/", response_model=list[BorrowRecordResponse])
def get_borrow_records(
    db: Session = Depends(get_db)
):
    return db.query(BorrowRecord).all()


# 3. GET OVERDUE RECORDS
@router.get("/overdue", response_model=list[BorrowRecordResponse])
def get_overdue_records(
    db: Session = Depends(get_db)
):
    today = date.today()

    return (
        db.query(BorrowRecord)
        .filter(
            BorrowRecord.due_date < today,
            BorrowRecord.status != "Returned"
        )
        .all()
    )


# 4. GET BORROW RECORD BY ID
@router.get("/{borrow_id}", response_model=BorrowRecordResponse)
def get_borrow_record(
    borrow_id: int,
    db: Session = Depends(get_db)
):
    record = (
        db.query(BorrowRecord)
        .filter(BorrowRecord.borrow_id == borrow_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Borrow record not found"
        )

    return record


# 5. RETURN BOOK
@router.put(
    "/{borrow_id}/return",
    response_model=BorrowRecordResponse
)
def return_book(
    borrow_id: int,
    db: Session = Depends(get_db)
):
    record = (
        db.query(BorrowRecord)
        .filter(BorrowRecord.borrow_id == borrow_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Borrow record not found"
        )

    if record.status == "Returned":
        raise HTTPException(
            status_code=400,
            detail="Book has already been returned"
        )

    book = (
        db.query(Book)
        .filter(Book.book_id == record.book_id)
        .first()
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    record.return_date = date.today()
    record.status = "Returned"

    book.available_copies += 1

    db.commit()
    db.refresh(record)

    return record


# 6. UPDATE BORROW RECORD
@router.put("/{borrow_id}", response_model=BorrowRecordResponse)
def update_borrow_record(
    borrow_id: int,
    record_data: BorrowRecordCreate,
    db: Session = Depends(get_db)
):
    record = (
        db.query(BorrowRecord)
        .filter(BorrowRecord.borrow_id == borrow_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Borrow record not found"
        )

    record.book_id = record_data.book_id
    record.member_id = record_data.member_id
    record.borrow_date = record_data.borrow_date
    record.due_date = record_data.due_date
    record.status = record_data.status

    if record_data.status == "Returned":
        record.return_date = record_data.return_date
    else:
        record.return_date = None

    db.commit()
    db.refresh(record)

    return record


# 7. DELETE BORROW RECORD
@router.delete("/{borrow_id}")
def delete_borrow_record(
    borrow_id: int,
    db: Session = Depends(get_db)
):
    record = (
        db.query(BorrowRecord)
        .filter(BorrowRecord.borrow_id == borrow_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Borrow record not found"
        )

    db.delete(record)
    db.commit()

    return {
        "message": "Borrow record deleted successfully"
    }