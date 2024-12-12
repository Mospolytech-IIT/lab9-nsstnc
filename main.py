import uvicorn

from models import *
from database import *
from db_init import db_init

from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from models import User, Post
from database import get_session, CRUDOperations

# Создание приложения FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Модели Pydantic для данных
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int


# Маршруты для работы с пользователями
@app.get("/users", response_class=HTMLResponse)
def list_users(request: Request):
    with get_session() as session:
        users = session.query(User).all()
    return templates.TemplateResponse("list_users.html", {"request": request, "users": users})


@app.post("/users")
def create_user(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    CRUDOperations.add_users([{"username": username, "email": email, "password": password}])
    return {"message": "User created successfully"}


@app.get("/users/{user_id}", response_class=HTMLResponse)
def edit_user(request: Request, user_id: int):
    with get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})


@app.post("/users/{user_id}")
def update_user(user_id: int, email: str = Form(...)):
    CRUDOperations.update_user_email(user_id, email)
    return {"message": "User updated successfully"}


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    CRUDOperations.delete_user_and_posts(user_id)
    return {"message": "User and their posts deleted successfully"}


# Маршруты для работы с постами
@app.get("/posts", response_class=HTMLResponse)
def list_posts(request: Request):
    with get_session() as session:
        posts = session.query(Post).all()
    return templates.TemplateResponse("list_posts.html", {"request": request, "posts": posts})


@app.post("/posts")
def create_post(title: str = Form(...), content: str = Form(...), user_id: int = Form(...)):
    CRUDOperations.add_posts([{"title": title, "content": content, "user_id": user_id}])
    return {"message": "Post created successfully"}


@app.get("/posts/{post_id}", response_class=HTMLResponse)
def edit_post(request: Request, post_id: int):
    with get_session() as session:
        post = session.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("edit_post.html", {"request": request, "post": post})


@app.post("/posts/{post_id}")
def update_post(post_id: int, content: str = Form(...)):
    CRUDOperations.update_post_content(post_id, content)
    return {"message": "Post updated successfully"}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    CRUDOperations.delete_post(post_id)
    return {"message": "Post deleted successfully"}


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    # db_init()
    uvicorn.run(app, host="localhost", port=8000)
