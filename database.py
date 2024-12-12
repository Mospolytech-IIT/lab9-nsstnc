from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///example.db"
engine = create_engine(DATABASE_URL, echo=True)

session_factory = sessionmaker(bind=engine)


def get_session():
    with session_factory() as session:
        yield session
        