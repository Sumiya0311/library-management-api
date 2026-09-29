from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.borrow_record import BorrowRecord
from app.schemas.borrow_record import BorrowRecordCreate, BorrowRecordResponse


router = APIRouter(prefix="/borrow-records", tags=["Borrow Records"])

@router.post("/", response_model=BorrowRecordResponse)
def create_borrow_record(
    record: BorrowRecordCreate,
    db: Session = Depends(get_db)
):
    new_record = BorrowRecord(
        book_id=record.book_id,
        member_id=record.member_id,
        borrow_date=record.borrow_date,
        due_date=record.due_date,
        return_date=record.return_date,
        status=record.status
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


@router.get("/", response_model=list[BorrowRecordResponse])
def get_borrow_records(db: Session = Depends(get_db)):
    return db.query(BorrowRecord).all()


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
    record.return_date = record_data.return_date
    record.status = record_data.status

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

    return {"message": "Borrow record deleted successfully"}