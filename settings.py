from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgres+psycopg2://postgres:password@localhost:5432/books_database") 