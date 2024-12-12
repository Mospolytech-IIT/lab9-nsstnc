from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from models import *

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


class CRUDOperations:

    @staticmethod
    def add_users(users):
        with get_session() as session:
            for user in users:
                session.add(User(**user))
            session.commit()

    @staticmethod
    def add_posts(posts):
        with get_session() as session:
            for post in posts:
                session.add(Post(**post))
            session.commit()

    @staticmethod
    def get_all_users():
        with get_session() as session:
            return session.query(User).all()

    @staticmethod
    def get_all_posts():
        with get_session() as session:
            return session.query(Post).all()

    @staticmethod
    def get_posts_by_user(user_id):
        with get_session() as session:
            return session.query(Post).filter(Post.user_id == user_id).all()

    @staticmethod
    def update_user_email(user_id, new_email):
        with get_session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                user.email = new_email
                session.commit()

    @staticmethod
    def update_post_content(post_id, new_content):
        with get_session() as session:
            post = session.query(Post).filter(Post.id == post_id).first()
            if post:
                post.content = new_content
                session.commit()

    @staticmethod
    def delete_post(post_id):
        with get_session() as session:
            post = session.query(Post).filter(Post.id == post_id).first()
            if post:
                session.delete(post)
                session.commit()

    @staticmethod
    def delete_user_and_posts(user_id):
        with get_session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                session.query(Post).filter(Post.user_id == user_id).delete()
                session.delete(user)
                session.commit()
