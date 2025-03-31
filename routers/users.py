from fastapi import HTTPException
from pydantic import BaseModel
from typing import Union
from fastapi import APIRouter

router = APIRouter(prefix = "/user", tags = ["Users"], )    # Se crea el router
router_users = APIRouter(tags = ["Users"])                  # Se crea el router solo para los usuarios

# User Class
class User(BaseModel): # BaseModel allows us create a JSON structure
    id: int
    name: str
    lastname: str
    age: int

users_list = [User(id=1, name="Oscar", lastname="Gonzales", age=30),
              User(id=2, name="Juan", lastname="Perez", age=25),
              User(id=3, name="Maria", lastname="Lopez", age=35)]


@router_users.get("/users")
async def users(): # Key:value (JSON Structure)
    return users_list

# Calling through the URL (path parameter)
@router.get("/{id}")
async def user(id: int):
    return search_user(id)

# Calling through the URL (query parameter)
@router.get("/")
async def user(id: int):
    return search_user(id)


@router.put("/")
async def update_user(user: User):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"Error": "Error, no se ha actualizado"}

    return user


# Calling through the URL (query parameter)
@router.post("/" , response_model=User, status_code=201)   # status_code=201: Created, con esto se lanza el status code 201
async def create_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")  # Lanza un error si el usuario ya existe
    else:
        users_list.append(user)
        return user

# Calling through the URL (query parameter)
@router.delete("/{id}")
async def user(id:int):

    found = False

    for index, saved_user in enumerate(users_list): # Itera sobre la lista de usuarios y OBTIENE "index" y "saved_user"
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return{"Error":"No se ha eliminado el usuario"}


def search_user(id: int):
    users = filter (lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"message": "User not found"}