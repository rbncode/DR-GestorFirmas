import os
from typing import List, Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from bson import ObjectId
from bson.errors import InvalidId
from .modelos import Usuario, UsuarioWithId, Solicitudes, SolicitudCreate

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
    
    async def connect(self):
        # Obtener la URI desde variables de entorno
        mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        db_name = os.getenv('MONGO_DB', 'FirmaSimple')
        
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        
        # Verificar conexión
        try:
            self.client.admin.command('ping')
            print("Conexión exitosa a MongoDB")
        except Exception as e:
            print(f"Error conectando a MongoDB: {e}")
            raise
    
    def get_database(self):
        return self.db

# Instancia global de la base de datos
mongodb = MongoDB()