from pydantic import BaseModel

class CategoryBase(BaseModel):
    category_name: str
    description: str | None = None

class CategoryCreate(CategoryBase):
    pass
class CategoryResponse(CategoryBase):
    category_id: int
class Config:
    from_attributes = True