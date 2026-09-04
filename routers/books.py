from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models
from database import get_db
from auth import get_current_user, require_admin

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=schemas.BookOut)
def add_book(book: schemas.BookCreate, db: Session = Depends(get_db), admin: models.User = Depends(require_admin)):
    return crud.create_book(db, book)


@router.get("/", response_model=List[schemas.BookOut])
def list_books(search: Optional[str] = None, db: Session = Depends(get_db)):
    # Public: anyone can browse/search the catalogue
    return crud.get_books(db, search=search)


@router.get("/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.put("/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, updates: schemas.BookUpdate, db: Session = Depends(get_db), admin: models.User = Depends(require_admin)):
    db_book = crud.update_book(db, book_id, updates)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), admin: models.User = Depends(require_admin)):
    db_book = crud.delete_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted successfully"}
