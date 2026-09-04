from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import crud
from database import get_db

router = APIRouter(tags=["Pages"])
templates = Jinja2Templates(directory="templates")
templates.env.cache = None  # Workaround: disable Jinja2's internal cache (bug on Python 3.14)


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "login.html", {})


@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    stats = crud.get_dashboard_stats(db)
    return templates.TemplateResponse(request, "dashboard.html", {"stats": stats})


@router.get("/books-page")
def books_page(request: Request, db: Session = Depends(get_db)):
    books = crud.get_books(db)
    return templates.TemplateResponse(request, "books.html", {"books": books})


@router.get("/issue-page")
def issue_page(request: Request):
    return templates.TemplateResponse(request, "issue.html", {})
