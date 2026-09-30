from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


# CREATE CATEGORY
@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    existing_category = (
        db.query(Category)
        .filter(Category.category_name == category.category_name)
        .first()
    )

    if existing_category:
        raise HTTPException(
            status_code=409,
            detail="Category already exists"
        )

    new_category = Category(
        category_name=category.category_name,
        description=category.description
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


# GET ALL CATEGORIES
@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


# GET CATEGORY BY ID
@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = (
        db.query(Category)
        .filter(Category.category_id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category


# UPDATE CATEGORY
@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
):
    category = (
        db.query(Category)
        .filter(Category.category_id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    existing_category = (
        db.query(Category)
        .filter(
            Category.category_name == category_data.category_name,
            Category.category_id != category_id
        )
        .first()
    )

    if existing_category:
        raise HTTPException(
            status_code=409,
            detail="Category already exists"
        )

    category.category_name = category_data.category_name
    category.description = category_data.description

    db.commit()
    db.refresh(category)

    return category


# DELETE CATEGORY
@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = (
        db.query(Category)
        .filter(Category.category_id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    db.delete(category)
    db.commit()

    return {"message": "Category deleted successfully"}