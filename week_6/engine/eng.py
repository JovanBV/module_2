from sqlalchemy import create_engine

DB_URI = 'postgresql://postgres:jovan@localhost:5432/postgres'
engine = create_engine(DB_URI, echo=False)