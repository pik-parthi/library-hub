from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


# ---------- USER / AUTH ----------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "member"
    name: str
    roll_no: str
    department: Optional[str] = None
    contact: Optional[str] = None


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- BOOK ----------
class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    category: str
    total_copies: int = 1


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    category: Optional[str] = None
    total_copies: Optional[int] = None


class BookOut(BookBase):
    id: int
    available_copies: int

    class Config:
        from_attributes = True


# ---------- MEMBER ----------
class MemberOut(BaseModel):
    id: int
    name: str
    roll_no: str
    department: Optional[str]
    contact: Optional[str]

    class Config:
        from_attributes = True


# ---------- ISSUE / RETURN ----------
class IssueCreate(BaseModel):
    book_id: int
    member_id: int
    due_days: int = 14  # default 14-day borrowing period


class IssueOut(BaseModel):
    id: int
    book_id: int
    member_id: int
    issue_date: date
    due_date: date
    return_date: Optional[date]
    fine: float

    class Config:
        from_attributes = True


class ReturnRequest(BaseModel):
    issue_id: int
