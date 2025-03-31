from pymongo import MongoClient

# Base de datos local
# db_client = MongoClient().local

# Base de datos en la nube (REMOTA)
db_client = MongoClient("mongodb+srv://oscar:oscar@cluster0.ewoaneg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").oscar
