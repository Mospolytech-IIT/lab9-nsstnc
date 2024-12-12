from database import get_session
from models import *


def db_init():
    with get_session() as session:
        users = [User(username='Egor', email='email1', password='password'),
                User(username='Alex', email='email2', password='password')]

        for user in users:
            session.add(user)

        posts = [
            Post(title="Заголовок1", content="содержание", user_id=1),
            Post(title="Заголовок2", content="содержание", user_id=2)
        ]

        for post in posts:
            session.add(post)

        session.commit()
