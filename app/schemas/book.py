from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    category_id: int
    total_copies: int
    available_copies: int
    published_year: int | None = None

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    book_id: int
    
class Config:
    from_attributes = True
