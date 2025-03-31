from fastapi import HTTPException, APIRouter, status
from pydantic import BaseModel
from typing import Union
from db.models.user import User # Importamos la clase User (Es importante para tener orden en el código)
from db.client import db_client # Importamos la conexión a la base de datos
from db.schemas.user import user_schema, users_schema # Importamos la función user_schema
from bson import ObjectId # Importamos ObjectId para convertir el id de MongoDB a string

router = APIRouter(prefix = "/userdb", 
                   tags = ["Usersdb"],
                   responses = {status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}}) # Se crea el router
#router_users = APIRouter(tags = ["Usersdb"])                  # Se crea el router solo para los usuarios


################ YA NO LA USO PORQUE LA TENGO EN MODELS ################
# User Class
# class User(BaseModel): # BaseModel allows us create a JSON structure
#     id: int
#     name: str
#     lastname: str
#     age: int

################ BUENA PRÁCTICA NO PONER ESTO EN ESTE FILE ################


# Traer todos los usuarios de la base de datos
@router.get("/", response_model=list[User])
async def users(): # Key:value (JSON Structure)
    return users_schema(db_client.users.find()) # Retorna todos los usuarios de la base de datos



# Calling through the URL (path parameter)
@router.get("/{id}")
async def user(id: str):
    return (search_user("_id" , ObjectId(id)))

# Calling through the URL (query parameter)
@router.get("/")
async def user(id: int):
    return (search_user("email" , ObjectId(id)))



@router.put("/", response_model=User)
async def update_user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)

    except:
        return {"error" : "No se ha actualizado el usuario"}

    return search_user("_id" , ObjectId(user.id))



@router.post("/" , response_model=User, status_code=status.HTTP_201_CREATED)   # status_code=201: Created, con esto se lanza el status code 201
async def create_user(user: User):  # Espera un parámetro de tipo JSON
    if type(search_user("email" , user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")  # Lanza un error si el usuario ya existe

    user_dict = dict(user) # Convierte el objeto user a un diccionario (JSON)
    del user_dict["id"] # Elimina el campo id del diccionario. Será generado por el propio MongoDB

    id = db_client.users.insert_one(user_dict).inserted_id # Inserta el usuario en la base de datos

    # Vamos a buscar el usuario que acabamos de insertar
    new_user = user_schema(db_client.users.find_one({"_id": id})) #"_id" es el campo que genera MongoDB automáticamente. CLAVE ÚNICA

    return User(**new_user) # Retorna el usuario creado tipo "User"





# Calling through the URL (query parameter)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id:str):

    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return{"Error":"No se ha eliminado el usuario"}


# Para validar si ya existe un usuario por email
def search_user(field: str, key): # key genérico, sin tipado
    try:
        user = db_client.users.find_one({field: key}) # Busca el usuario por email
        return User(**user_schema(user))
    except:
        return {"Error": "No se ha encontado el usuario"}
