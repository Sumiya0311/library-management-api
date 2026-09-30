from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models.borrow_record import BorrowRecord
from app.schemas.borrow_record import BorrowRecordCreate, BorrowRecordResponse
from app.services.borrow_service import create_borrow_record, return_book

router = APIRouter(
    prefix="/borrow-records",
    tags=["Borrow Records"]
)


@router.post("/", response_model=BorrowRecordResponse)
def create_record(
    record: BorrowRecordCreate,
    db: Session = Depends(get_db)
):
    return create_borrow_record(record, db)


@router.get("/", response_model=list[BorrowRecordResponse])
def get_borrow_records(db: Session = Depends(get_db)):
    return db.query(BorrowRecord).all()


@router.get("/overdue", response_model=list[BorrowRecordResponse])
def get_overdue_records(db: Session = Depends(get_db)):
    today = date.today()

    return (
        db.query(BorrowRecord)
        .filter(
            BorrowRecord.due_date < today,
            BorrowRecord.status != "Returned"
        )
        .all()
    )


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


@router.put("/{borrow_id}/return", response_model=BorrowRecordResponse)
def return_borrowed_book(
    borrow_id: int,
    db: Session = Depends(get_db)
):
    return return_book(borrow_id, db)


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