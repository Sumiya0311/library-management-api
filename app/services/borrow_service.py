from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.borrow_record import BorrowRecord
from app.models.book import Book
from app.models.member import Member
from app.schemas.borrow_record import BorrowRecordCreate


def create_borrow_record(
    record: BorrowRecordCreate,
    db: Session
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


def return_book(
    borrow_id: int,
    db: Session
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