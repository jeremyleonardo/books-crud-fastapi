# Books API

A simple CRUD API created with FastAPI and SQLAlchemy for PostgreSQL

## Available APIs

It is recommended to test the available APIs from ``[GET] /docs``

- ``[GET] /`` - Root (Check API status)
- ``[POST] /books`` - Create Book
- ``[GET] /books/{id}`` - Find Book
- ``[GET] /books`` - Get Books
- ``[PUT] /books`` - Update Book
- ``[DELETE] /books`` - Delete Book

## Usage

using pipenv:
```
pipenv install
pipenv run uvicorn main:app
```