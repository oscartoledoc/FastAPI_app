from fastapi import APIRouter, HTTPException

router = APIRouter(prefix ="/products", 
                   tags = ["products"], 
                   responses = {404:{"message" : "No encontrado"}})    # Se crea el router | prefix: Para agregar un prefijo a la URL a todos los endpoints


products_list = ["Product 1", "Product 2", "Product 3", "Product 4", "Product 5"]


@router.get("/")
async def products(): # Key:value (JSON Structure)
    return products_list

@router.get("/{id}")
async def product(id: int):
    try:
        return products_list[id]
    except:
        raise HTTPException(status_code=404, detail="Product not found")