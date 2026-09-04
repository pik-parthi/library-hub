from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_

import models
import schemas
from auth import hash_password

FINE_PER_DAY = 2.0  # currency units per day overdue


# ---------- USER ----------
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_member = models.Member(
        user_id=db_user.id,
        name=user.name,
        roll_no=user.roll_no,
        department=user.department,
        contact=user.contact,
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)

    return db_user


# ---------- BOOK ----------
def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        category=book.category,
        total_copies=book.total_copies,
        available_copies=book.total_copies,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, search: str = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Book)
    if search:
        like = f"%{search}%"
        query = query.filter(
            or_(models.Book.title.ilike(like), models.Book.author.ilike(like), models.Book.category.ilike(like))
        )
    return query.offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(db: Session, book_id: int, updates: schemas.BookUpdate):
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_book, field, value)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book


# ---------- MEMBER ----------
def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Member).offset(skip).limit(limit).all()


def get_member(db: Session, member_id: int):
    return db.query(models.Member).filter(models.Member.id == member_id).first()


# ---------- ISSUE / RETURN ----------
def issue_book(db: Session, issue: schemas.IssueCreate):
    db_book = get_book(db, issue.book_id)
    if not db_book or db_book.available_copies < 1:
        return None  # caller should raise HTTPException

    today = date.today()
    db_issue = models.IssueRecord(
        book_id=issue.book_id,
        member_id=issue.member_id,
        issue_date=today,
        due_date=today + timedelta(days=issue.due_days),
        return_date=None,
        fine=0.0,
    )
    db_book.available_copies -= 1
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


def return_book(db: Session, issue_id: int):
    db_issue = db.query(models.IssueRecord).filter(models.IssueRecord.id == issue_id).first()
    if not db_issue or db_issue.return_date is not None:
        return None

    today = date.today()
    db_issue.return_date = today

    if today > db_issue.due_date:
        overdue_days = (today - db_issue.due_date).days
        db_issue.fine = overdue_days * FINE_PER_DAY

    db_book = get_book(db, db_issue.book_id)
    if db_book:
        db_book.available_copies += 1

    db.commit()
    db.refresh(db_issue)
    return db_issue


def get_issue_records(db: Session, member_id: int = None, active_only: bool = False):
    query = db.query(models.IssueRecord)
    if member_id:
        query = query.filter(models.IssueRecord.member_id == member_id)
    if active_only:
        query = query.filter(models.IssueRecord.return_date.is_(None))
    return query.all()


# ---------- DASHBOARD STATS ----------
def get_dashboard_stats(db: Session):
    total_books = db.query(models.Book).count()
    total_members = db.query(models.Member).count()
    issued_now = db.query(models.IssueRecord).filter(models.IssueRecord.return_date.is_(None)).count()
    return {
        "total_books": total_books,
        "total_members": total_members,
        "books_issued": issued_now,
    }
