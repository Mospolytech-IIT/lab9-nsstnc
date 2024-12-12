from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


DATABASE_URL = "sqlite:///example.db"
engine = create_engine(DATABASE_URL, echo=True)

session_factory = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
