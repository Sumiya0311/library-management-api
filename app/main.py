from fastapi import FastAPI
from app.database import Base, engine
from app.models.category import Category
from app.models.book import Book
from app.models.member import Member
from app.models.borrow_record import BorrowRecord
from app.routers import category, book, member, borrow_record
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System")
app.include_router(category.router)
app.include_router(book.router)
app.include_router(member.router)
app.include_router(borrow_record.router)

@app.get("/")
def home():
    return {"message": "Library Management System API is running"}