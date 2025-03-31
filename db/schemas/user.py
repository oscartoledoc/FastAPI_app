
def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),     # Convertimos el ObjectId de MongoDB a un string
        "username": user["username"],
        "email": user["email"]
    }

def users_schema(users) -> list:
    return [user_schema(user) for user in users]


    # id: str | None # None: Allows the field to be optional
    # username : str
    # email : str