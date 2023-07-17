from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL is None:
    raise ValueError('DATABASE_URL environment variable not set')
else:
    print(f"Database url: {DATABASE_URL.split('@')[-1]}")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()