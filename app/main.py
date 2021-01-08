from sqlalchemy import create_engine
from app.settings import DATABASE_URL
from app.models import Base, Book
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from typing import Optional


# DISCLAIMER:
# This is a very simple CRUD API
# Not intended for production


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def recreate_database():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

recreate_database()

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Sample books API is online"}


@app.get("/books/{id}")
async def find_book(id: int):
    session = Session()
    book = session.query(Book).filter(
       Book.id == id
    ).first()
    session.close()
    return {"book": book}


@app.get("/books")
async def get_books(page_size: int = 10, page: int = 1):
    if(page_size > 100 or page_size < 0):
        page_size = 100

    page -= 1
    session = Session()
    books = session.query(Book).limit(page_size).offset(page*page_size).all()
    session.close()
    return {"books": books}


@app.post("/books")
async def create_book(title: str, pages: int):
    session = Session()
    book = Book(
        title=title,
        pages=pages,
        created_at = date.today()
    )
    session.add(book)
    session.commit()
    session.close()
    return {
        "message": "success"
    }


@app.put("/books")
async def update_book(id: int, title: str, pages: int):
    session = Session()
    book = session.query(Book).get(id)
    book.title = title
    book.pages = pages
    session.commit()
    session.close()
    return {
        "message": "success"
    }


@app.delete("/books")
async def delete_book(id: int):
    session = Session()
    book = session.query(Book).get(id)
    session.delete(book)
    session.commit()
    session.close()
    return {
        "message": "success"
    }
