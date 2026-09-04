# Online Library Management System (FastAPI)

A web-based Library Management System built with **FastAPI**, **SQLAlchemy**, and **Jinja2**.

## Features
- JWT-based authentication (Admin & Member roles)
- Book management (add/edit/delete/search) — admin only for write ops
- Member management
- Book issue & return with automatic fine calculation
- Dashboard with live stats
- Auto-generated API docs at `/docs` (Swagger UI)

## Setup Instructions

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```

4. **Open in browser**:
   - Web app: http://127.0.0.1:8000
   - API docs (Swagger UI): http://127.0.0.1:8000/docs

## First-time Usage

1. Go to `/docs` → `POST /auth/register` → create an **admin** user:
   ```json
   {
     "username": "admin",
     "email": "admin@library.com",
     "password": "admin123",
     "role": "admin",
     "name": "Library Admin",
     "roll_no": "ADMIN001",
     "department": "Administration",
     "contact": "9999999999"
   }
   ```
2. Go to `/` (web login page) and log in with the admin credentials.
3. Use `/docs` → `POST /books/` (with the JWT token, click "Authorize" button in Swagger UI using the token from login) to add books.
4. Register member users the same way with `"role": "member"`.
5. Use `POST /issue/` to issue a book to a member, and `POST /issue/return` to return it.

## Project Structure
```
library_management/
├── main.py               # App entry point
├── database.py            # DB connection (SQLAlchemy)
├── models.py               # ORM models (User, Book, Member, IssueRecord)
├── schemas.py               # Pydantic request/response schemas
├── auth.py                   # JWT auth & password hashing
├── crud.py                    # Database operations
├── routers/
│   ├── auth_router.py          # /auth/register, /auth/login
│   ├── books.py                 # /books CRUD
│   ├── members.py                # /members
│   ├── issue.py                   # /issue, /issue/return
│   └── pages.py                    # Jinja2 page routes
├── templates/                       # HTML pages (login, dashboard, books, issue)
├── static/style.css                  # Styling
└── requirements.txt
```

## Notes
- Default fine rate: ₹2/day for overdue books (edit `FINE_PER_DAY` in `crud.py`).
- Default borrowing period: 14 days (editable per-issue via `due_days` in the request).
- Change `SECRET_KEY` in `auth.py` before any real deployment.
- Database is SQLite (`library.db`) — created automatically on first run.
