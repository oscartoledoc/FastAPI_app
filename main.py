from typing import Union

from fastapi import FastAPI
from routers import users, products, basic_auth_users, jwt_auth_users,users_db # Importamos los routers
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Include the routers
app.include_router(users.router)    # Para incluir el router de users
app.include_router(products.router) # Para incluir el router de products
app.include_router(users.router_users) # Para incluir el router de users
app.include_router(users_db.router) # Para incluir el router de users_db

app.include_router(basic_auth_users.router) # Para incluir el router de basic_auth_users
app.include_router(jwt_auth_users.router) # Para incluir el router de jwt_auth_users

app.mount("/static", StaticFiles(directory="static"), name="static") # Para incluir archivos estaticos

@app.get("/")
async def read_root():
    return {"Hola": "Mundo Peru"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/apellidos")
async def mylastname():
    return {"apellido": "Gonzales"}



#Documentation with Swagger: http://localhost:8000/docs
#Documentation with ReDoc: http://localhost:8000/redoc