import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import engine, Base
from routers import auth_router, books, members, issue, pages

# Create all database tables (run once at startup)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Online Library Management System",
    description="A FastAPI-based backend for managing books, members, issue/return, and fines.",
    version="1.0.0",
)

# Static files (CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# API routers
app.include_router(auth_router.router)
app.include_router(books.router)
app.include_router(members.router)
app.include_router(issue.router)

# Frontend page routes (Jinja2)
app.include_router(pages.router)


# Allows running directly (e.g. via VS Code "Run/Debug" button on this file).
# For development, prefer: uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
