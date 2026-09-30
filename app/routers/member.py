from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.member import Member
from app.models.book import Book
from app.models.borrow_record import BorrowRecord

from app.schemas.member import MemberCreate, MemberResponse
from app.schemas.book import BookResponse
from app.schemas.borrow_record import BorrowRecordResponse


router = APIRouter(
    prefix="/members",
    tags=["Members"]
)


# CREATE MEMBER
@router.post("/", response_model=MemberResponse)
def create_member(
    member: MemberCreate,
    db: Session = Depends(get_db)
):
    # Check duplicate email
    existing_member = (
        db.query(Member)
        .filter(Member.email == member.email)
        .first()
    )

    if existing_member:
        raise HTTPException(
            status_code=409,
            detail="Member with this email already exists"
        )

    new_member = Member(
        name=member.name,
        email=member.email,
        phone=member.phone,
        address=member.address,
        membership_date=member.membership_date,
        is_active=member.is_active
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


# GET ALL MEMBERS
@router.get("/", response_model=list[MemberResponse])
def get_members(
    db: Session = Depends(get_db)
):
    return db.query(Member).all()


# GET MEMBER'S CURRENTLY BORROWED BOOKS
@router.get("/{member_id}/books", response_model=list[BookResponse])
def get_member_books(
    member_id: int,
    db: Session = Depends(get_db)
):
    member = (
        db.query(Member)
        .filter(Member.member_id == member_id)
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    books = (
        db.query(Book)
        .join(
            BorrowRecord,
            Book.book_id == BorrowRecord.book_id
        )
        .filter(
            BorrowRecord.member_id == member_id,
            BorrowRecord.status != "Returned"
        )
        .all()
    )

    return books


# GET MEMBER BORROW HISTORY
@router.get(
    "/{member_id}/borrow-history",
    response_model=list[BorrowRecordResponse]
)
def get_member_borrow_history(
    member_id: int,
    db: Session = Depends(get_db)
):
    member = (
        db.query(Member)
        .filter(Member.member_id == member_id)
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    history = (
        db.query(BorrowRecord)
        .filter(BorrowRecord.member_id == member_id)
        .all()
    )

    return history


# GET MEMBER BY ID
@router.get("/{member_id}", response_model=MemberResponse)
def get_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    member = (
        db.query(Member)
        .filter(Member.member_id == member_id)
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return member


# UPDATE MEMBER
@router.put("/{member_id}", response_model=MemberResponse)
def update_member(
    member_id: int,
    member_data: MemberCreate,
    db: Session = Depends(get_db)
):
    member = (
        db.query(Member)
        .filter(Member.member_id == member_id)
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    # Check duplicate email
    existing_member = (
        db.query(Member)
        .filter(
            Member.email == member_data.email,
            Member.member_id != member_id
        )
        .first()
    )

    if existing_member:
        raise HTTPException(
            status_code=409,
            detail="Member with this email already exists"
        )

    member.name = member_data.name
    member.email = member_data.email
    member.phone = member_data.phone
    member.address = member_data.address
    member.membership_date = member_data.membership_date
    member.is_active = member_data.is_active

    db.commit()
    db.refresh(member)

    return member


# DELETE MEMBER
@router.delete("/{member_id}")
def delete_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    member = (
        db.query(Member)
        .filter(Member.member_id == member_id)
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    db.delete(member)
    db.commit()

    return {
        "message": "Member deleted successfully"
    }