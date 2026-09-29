from sqlalchemy import Column, Integer, String, Date, Boolean
from app.database import Base

class Member(Base):
    __tablename__ = "members"
    member_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    address = Column(String(255))
    membership_date = Column(Date) 
    is_active = Column(Boolean, default=True)