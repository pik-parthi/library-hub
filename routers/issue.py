from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import models
from database import get_db
from auth import require_admin, get_current_user

router = APIRouter(prefix="/issue", tags=["Issue & Return"])


@router.post("/", response_model=schemas.IssueOut)
def issue_book(request: schemas.IssueCreate, db: Session = Depends(get_db), admin: models.User = Depends(require_admin)):
    result = crud.issue_book(db, request)
    if not result:
        raise HTTPException(status_code=400, detail="Book not available for issue")
    return result


@router.post("/return", response_model=schemas.IssueOut)
def return_book(request: schemas.ReturnRequest, db: Session = Depends(get_db), admin: models.User = Depends(require_admin)):
    result = crud.return_book(db, request.issue_id)
    if not result:
        raise HTTPException(status_code=400, detail="Invalid issue record or already returned")
    return result


@router.get("/", response_model=List[schemas.IssueOut])
def list_issue_records(member_id: int = None, active_only: bool = False, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return crud.get_issue_records(db, member_id=member_id, active_only=active_only)
