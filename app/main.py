from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime, date
from typing import Optional
from app.settings import DATABASE_URL
from app.models import Base, Book


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
    
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "book": book
        })


@app.get("/books")
async def get_books(page_size: int = 10, page: int = 1):
    if(page_size > 100 or page_size < 0):
        page_size = 100

    page -= 1
    session = Session()
    books = session.query(Book).limit(page_size).offset(page*page_size).all()
    session.close()

    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "books": books
        })


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
    
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
        })


@app.put("/books")
async def update_book(id: int, title: str, pages: int):
    session = Session()
    book = session.query(Book).get(id)
    book.title = title
    book.pages = pages
    session.commit()
    session.close()
    
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
        })


@app.delete("/books")
async def delete_book(id: int):
    session = Session()
    book = session.query(Book).get(id)
    session.delete(book)
    session.commit()
    session.close()

    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
        })


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    json_resp = get_default_error_response()
    return json_resp


def get_default_error_response(status_code=500, message="Internal Server Error"):
    return JSONResponse(status_code=status_code, content={
        "status_code": status_code,
        "message": message
        })