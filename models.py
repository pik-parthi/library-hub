from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="member")  # "admin" or "member"

    member = relationship("Member", back_populates="user", uselist=False)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    isbn = Column(String, unique=True, index=True)
    category = Column(String, index=True)
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)

    issue_records = relationship("IssueRecord", back_populates="book")


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    name = Column(String, nullable=False)
    roll_no = Column(String, unique=True, index=True)
    department = Column(String)
    contact = Column(String)

    user = relationship("User", back_populates="member")
    issue_records = relationship("IssueRecord", back_populates="member")


class IssueRecord(Base):
    __tablename__ = "issue_records"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    fine = Column(Float, default=0.0)

    book = relationship("Book", back_populates="issue_records")
    member = relationship("Member", back_populates="issue_records")
