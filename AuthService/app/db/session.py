from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# Initialize the engine to manage the DB connections
engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# Initialize a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
