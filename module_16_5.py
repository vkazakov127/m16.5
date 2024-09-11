# -*- coding: utf-8 -*-
# module_16_5.py
from fastapi import FastAPI, Path, status, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import List, Annotated
import logging

app = FastAPI()
templates = Jinja2Templates(directory='.venv/templates_users')
# Настройка логирования
logging.basicConfig(level=logging.INFO, filemode='w', filename='fast.log',
                    format='%(asctime)s | %(levelname)s | %(message)s')

users = []
users_dict = {user['id']: user for user in users}


class User(BaseModel):
    user_id: int = None
    username: str = None
    age: int = None


@app.get("/")
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id}")
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    # Вычисление индекса в списке
    # Сначала сделаем из списка 'users' свой словарь. {'id':index}
    dict1 = {dict_i.user_id: users.index(dict_i) for dict_i in users}
    lst_index = dict1.get(user_id)
    if lst_index is None:
        return HTMLResponse(content="User not found", status_code=404)
    return templates.TemplateResponse("users.html", {"request": request, "user": users[lst_index]})


@app.post('/user/{username}/{age}')
async def add_user(username: Annotated[str, Path(min_length=1, max_length=20,
                                                 description='Enter user name', example='UrbanUser')],
                   age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]) -> User:
    # Вычисление атрибута "id" для нового объекта "User"
    if len(users) == 0:
        new_user_id = 1
    else:
        # new_user_id = max(users, key=lambda m: m["user_id"])["user_id"] + 1
        # Сначала сделаем из списка 'users' свой словарь. {'id':index}
        dict1 = {dict_i.user_id: users.index(dict_i) for dict_i in users}
        new_user_id = max(dict1) + 1
    # Новый объект "User"
    new_user = User(user_id=new_user_id, username=username, age=age)
    # Добавляем в список "users" объект "new_user"
    users.append(new_user)
    return new_user


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(request: Request,
        user_id: Annotated[int, Path(ge=1, le=150, description='Enter user ID', example=1)],
        username: Annotated[str, Path(min_length=1, max_length=20,
                                      description='Enter user name', example='UrbanProfi')],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=28)]) -> HTMLResponse:
    # Получаем объект "User" из списка "users"
    # Сначала сделаем из списка 'users' свой словарь. {'id':index}
    user_dict = {dict_i.user_id: users.index(dict_i) for dict_i in users}
    users_list_index = user_dict[user_id]  # Поиск по ключу в словаре 'user_dict'
    if users_list_index is None:
        return HTMLResponse(content="User not found", status_code=404)
    user_for_update = users[users_list_index]
    # Изменяем объект "User"
    user_for_update.username = username
    user_for_update.age = age
    return templates.TemplateResponse("users.html", {"request": request, "user": users[users_list_index]})


@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(ge=1, le=150, description='Enter user ID', example=2)]) -> str:
    # Сначала сделаем из списка 'users' свой словарь. {'id':index}
    user_dict = {dict_i.user_id: users.index(dict_i) for dict_i in users}
    users_list_index = user_dict.get(user_id)  # Поиск по ключу в словаре 'user_dict'
    if users_list_index is None:
        return f"User ID={user_id} is not found"
    # Для красоты запомним
    deleted_user_name = users[users_list_index].username
    deleted_user_age = users[users_list_index].age
    # Удаляем из списка
    users.pop(users_list_index)
    return (f"User ID={user_id} is deleted: "
            f"username={deleted_user_name}, "
            f"age={deleted_user_age}")
