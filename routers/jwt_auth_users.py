from typing import Union
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext # this is used to encrypt the password
from datetime import datetime, timedelta # to manage the time of the token

# The most algorithm used is HS256
# This is the algorithm used to encrypt the token
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 # 1 minute of authentication
SECRET = "7f24585e8fccbaa233f112ed215660c4579e8bd69e86bd830151cd586cce614b"

router = APIRouter()

# Instancia de autenticación
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

cryp = CryptContext(schemes=["bcrypt"])


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
        "password": "$2a$12$Q6UZk30VvRafpUv/SFjTTO2XWigM2d84rDPMw2YddOyNI0J.nGyGG"}, # This is a bad practice, the password should be encrypted (hashed)
        
    "mouredev2": {
        "username": "mouredev2",
        "fullname": "Miguel",
        "email": "oscar@gmail.com",
        "disabled": True,
        "password": "$2a$12$RLMfuVArOjHIueaIZKjm7uJ.kX7iIeY7mGPFKfRzlXA44C.wEtxvy"} # This is a bad practice, the password should be encrypted (hashed)
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


# Proceso de validación de token
async def auth_user(token : str = Depends(oauth2)):

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="Credenciales inválidas",
                              headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception
    
    return search_user(username)
    

# Criterio de dependencia
async def current_user(user : User = Depends(auth_user)):

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


    if not cryp.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    access_token = {"sub": user.username, 
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    # Ya validadas las credenciales, se genera el token
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}  # El token es para evitar validar muchas veces las credenciales

@router.get("/users/me")
async def me (user : User = Depends(current_user)):
    return user