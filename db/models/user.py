# Esto sería nuestra entidad, MODELOS o PLANTILLAS con las que voy a trabajar en mi API
from pydantic import BaseModel
from typing import Optional

class User(BaseModel): # BaseModel allows us create a JSON structure
    id: Optional[str] = None # None: Allows the field to be optional #Diferente al video, aquí se pone Optional
    username : str
    email : str
