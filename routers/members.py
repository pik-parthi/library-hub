from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models
from database import get_db
from auth import require_admin

router = APIRouter(prefix="/members", tags=["Members"])


@router.get("/", response_model=List[schemas.MemberOut])
def list_members(db: Session = Depends(get_db), admin: models.User = Depends(require_admin)):
    return crud.get_members(db)


@router.get("/{member_id}", response_model=schemas.MemberOut)
def get_member(member_id: int, db: Session = Depends(get_db), admin: models.User = Depends(require_admin)):
    db_member = crud.get_member(db, member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member
