from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberResponse

router = APIRouter(prefix="/members", tags=["Members"])

@router.post("/", response_model=MemberResponse)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    new_member = Member(
      name=member.name, 
      email=member.email, 
      phone=member.phone, 
      address = member.address, 
      membership_date=member.membership_date,
      is_active=member.is_active
    )
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member

@router.get("/", response_model=list[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    return db.query(Member).all()

@router.get("/{member_id}", response_model=MemberResponse)
def get_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    member = db.query(Member).filter(Member.member_id == member_id).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return member

@router.put("/{member_id}", response_model=MemberResponse)
def update_member(
    member_id: int,
    member_data: MemberCreate,
    db: Session = Depends(get_db)
):
    member = db.query(Member).filter(Member.member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    member.name = member_data.name
    member.email = member_data.email
    member.address = member_data.address
    member.membership_date = member_data.membership_date
    member.is_active = member_data.is_active
    db.commit()
    db.refresh(member)
    return member

@router.delete("/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.member_id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(member)
    db.commit()
    return {"message": "Member deleted successfully"}
