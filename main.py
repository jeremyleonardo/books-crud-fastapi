from sqlalchemy import create_engine
from config import DATABASE_URI
from models import Base, Book
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from typing import Optional

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

def recreate_database():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

recreate_database()

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello"}

@app.get("/books/{id}")
async def find_book(id: int):
    s = Session()
    book = s.query(Book).filter(
       Book.id == id
    ).first()
    s.close()
    return {"book": book}

@app.get("/books")
async def get_books(limit: int = 10):
    if(limit > 100 | limit < 0):
        limit = 100
    s = Session()
    books = s.query(Book).limit(limit).all()
    s.close()
    return {"books": books}

@app.post("/books")
async def create_book(title: str, pages: int):
    s = Session()
    book = Book(
        title=title,
        pages=pages,
        created_at = date.today()
    )
    s.add(book)
    s.commit()
    s.close()
    return {
        "message": "success"
    }
