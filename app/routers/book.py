from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book
from app.schemas.book import BookCreate, BookResponse


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


# CREATE BOOK
@router.post("/", response_model=BookResponse)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db)
):
    # Check duplicate ISBN
    existing_book = (
        db.query(Book)
        .filter(Book.isbn == book.isbn)
        .first()
    )

    if existing_book:
        raise HTTPException(
            status_code=409,
            detail="Book with this ISBN already exists"
        )

    new_book = Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        category_id=book.category_id,
        total_copies=book.total_copies,
        available_copies=book.available_copies,
        published_year=book.published_year
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


# GET BOOKS - SEARCH + FILTER + PAGINATION
@router.get("/", response_model=list[BookResponse])
def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = None,
    category_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Book)

    # Search by title or author
    if search:
        query = query.filter(
            (Book.title.ilike(f"%{search}%")) |
            (Book.author.ilike(f"%{search}%"))
        )

    # Filter by category
    if category_id is not None:
        query = query.filter(
            Book.category_id == category_id
        )

    # Pagination
    return query.offset(skip).limit(limit).all()


# GET BOOK BY ID
@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = (
        db.query(Book)
        .filter(Book.book_id == book_id)
        .first()
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


# UPDATE BOOK
@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_data: BookCreate,
    db: Session = Depends(get_db)
):
    book = (
        db.query(Book)
        .filter(Book.book_id == book_id)
        .first()
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    # Check duplicate ISBN
    existing_book = (
        db.query(Book)
        .filter(
            Book.isbn == book_data.isbn,
            Book.book_id != book_id
        )
        .first()
    )

    if existing_book:
        raise HTTPException(
            status_code=409,
            detail="Book with this ISBN already exists"
        )

    book.title = book_data.title
    book.author = book_data.author
    book.isbn = book_data.isbn
    book.category_id = book_data.category_id
    book.total_copies = book_data.total_copies
    book.available_copies = book_data.available_copies
    book.published_year = book_data.published_year

    db.commit()
    db.refresh(book)

    return book


# DELETE BOOK
@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = (
        db.query(Book)
        .filter(Book.book_id == book_id)
        .first()
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    db.delete(book)
    db.commit()

    return {"message": "Book deleted successfully"}