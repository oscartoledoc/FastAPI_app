from typing import Union
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# "Bearer" is used to authenticate HTTP requests with token gived.
# "Request form" is a form that is used to authenticate the user. This give the token.

router = APIRouter()

# Instancia de autenticación
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel): # BaseModel allows us create a JSON structure
    username: str
    fullname: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "mouredev": {
        "username": "mouredev",
        "fullname": "Miguel",
        "email": "oscar@gmail.com",
        "disabled": False,
        "password": "123456"}, # This is a bad practice, the password should be encrypted (hashed)
        
    "mouredev2": {
        "username": "mouredev2",
        "fullname": "Miguel",
        "email": "oscar@gmail.com",
        "disabled": True,
        "password": "654321"} # This is a bad practice, the password should be encrypted (hashed)
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

# Criterio de dependencia
async def current_user(token : str = Depends(oauth2)):
    user = search_user (token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Credenciales inválidas", 
                            headers={"WWW-Authenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Usuario Inactivo")

    return user


@router.post("/login")
async def login (form: OAuth2PasswordRequestForm = Depends()): # Depends ejecuta a "Request form" y este pasa los datos validados a "form"
    user_db = users_db.get(form.username)
    if not user_db: # Verifica si es NULO o FALSE
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario no encontrado")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    # Ya validadas las credenciales, se genera el token
    return {"access_token": user.username, "token_type": "bearer"}  # El token es para evitar validar muchas veces las credenciales


@router.get("/users/me")
async def me (user : User = Depends(current_user)):
    return user