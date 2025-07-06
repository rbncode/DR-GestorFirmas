from typing import List, Optional
from bson import ObjectId
from bson.errors import InvalidId
from .modelos import Usuario, UsuarioWithId, Solicitudes, SolicitudCreate
from .mongodb import mongodb
SOLICITUDES_COLLECTION = 'Solicitudes'
USUARIOS_COLLECTION = 'Usuarios'

# Helper para convertir documento de MongoDB a tipo Solicitudes
def from_mongodb_solicitud(doc: dict) -> Solicitudes:
    return Solicitudes(
        id=str(doc['_id']),
        titulo=doc['titulo'],
        categoria=doc['categoria'],
        descripcion=doc['descripcion'],
        fecha=doc['fecha'],
        empleado=Usuario(**doc['empleado']),
        supervisor=Usuario(**doc['supervisor']),
        hr=Usuario(**doc['hr']),
        documentoId=doc['documentoId']
    )

def from_mongodb_usuario(doc: dict) -> UsuarioWithId:
    return UsuarioWithId(
        id=str(doc['_id']),
        nombre=doc['nombre'],
        correo=doc['correo'],
        rol=doc['rol'],
        contraseña=doc['contraseña']
    )

# Métodos para Solicitudes
async def get_solicitudes() -> List[Solicitudes]:
    """Obtener todas las solicitudes ordenadas por fecha descendente"""
    try:
        db = mongodb.get_database()
        collection = db[SOLICITUDES_COLLECTION]
        docs = list(collection.find({}).sort('fecha', -1))
        return [from_mongodb_solicitud(doc) for doc in docs]
    except Exception as error:
        print(f"Error fetching solicitudes: {error}")
        raise error

async def get_solicitud_by_id(id: str) -> Optional[Solicitudes]:
    """Obtener una solicitud por ID"""
    if not id:
        return None
    
    try:
        db = mongodb.get_database()
        collection = db[SOLICITUDES_COLLECTION]
        doc = collection.find_one({'_id': ObjectId(id)})
        
        if doc:
            return from_mongodb_solicitud(doc)
        return None
    except InvalidId:
        print(f"ID inválido: {id}")
        return None
    except Exception as error:
        print(f"Error fetching solicitud by ID: {error}")
        return None

async def add_solicitud(solicitud_data: SolicitudCreate) -> Solicitudes:
    """Agregar una nueva solicitud"""
    try:
        db = mongodb.get_database()
        collection = db[SOLICITUDES_COLLECTION]
        
        # Convertir a diccionario para insertar
        solicitud_dict = solicitud_data.dict()
        
        result = collection.insert_one(solicitud_dict)
        
        return Solicitudes(
            id=str(result.inserted_id),
            **solicitud_dict
        )
    except Exception as error:
        print(f"Error adding solicitud: {error}")
        raise error

async def delete_solicitud(id: str) -> bool:
    """Eliminar una solicitud por ID"""
    if not id:
        return False
    
    try:
        db = mongodb.get_database()
        collection = db[SOLICITUDES_COLLECTION]
        result = collection.delete_one({'_id': ObjectId(id)})
        return result.deleted_count == 1
    except InvalidId:
        print(f"ID inválido: {id}")
        return False
    except Exception as error:
        print(f"Error deleting solicitud: {error}")
        return False

# Métodos para Usuarios
async def get_usuarios() -> List[UsuarioWithId]:
    """Obtener todos los usuarios"""
    try:
        db = mongodb.get_database()
        collection = db[USUARIOS_COLLECTION]
        docs = list(collection.find({}))
        return [from_mongodb_usuario(doc) for doc in docs]
    except Exception as error:
        print(f"Error fetching usuarios: {error}")
        raise error

async def get_usuario_by_id(id: str) -> Optional[UsuarioWithId]:
    """Obtener un usuario por ID"""
    if not id:
        return None
    
    try:
        db = mongodb.get_database()
        collection = db[USUARIOS_COLLECTION]
        doc = collection.find_one({'_id': ObjectId(id)})
        
        if doc:
            return from_mongodb_usuario(doc)
        return None
    except InvalidId:
        print(f"ID inválido: {id}")
        return None
    except Exception as error:
        print(f"Error fetching usuario by ID: {error}")
        return None

async def add_usuario(usuario_data: Usuario) -> UsuarioWithId:
    """Agregar un nuevo usuario"""
    try:
        db = mongodb.get_database()
        collection = db[USUARIOS_COLLECTION]
        
        # Convertir a diccionario para insertar
        usuario_dict = usuario_data.dict()
        
        result = collection.insert_one(usuario_dict)
        
        return UsuarioWithId(
            id=str(result.inserted_id),
            **usuario_dict
        )
    except Exception as error:
        print(f"Error adding usuario: {error}")
        raise error

async def delete_usuario(id: str) -> bool:
    """Eliminar un usuario por ID"""
    if not id:
        return False
    
    try:
        db = mongodb.get_database()
        collection = db[USUARIOS_COLLECTION]
        result = collection.delete_one({'_id': ObjectId(id)})
        return result.deleted_count == 1
    except InvalidId:
        print(f"ID inválido: {id}")
        return False
    except Exception as error:
        print(f"Error deleting usuario: {error}")
        return False

# Métodos adicionales que podrían ser útiles
async def get_usuario_by_correo(correo: str) -> Optional[UsuarioWithId]:
    """Obtener un usuario por correo electrónico"""
    if not correo:
        return None
    
    try:
        db = mongodb.get_database()
        collection = db[USUARIOS_COLLECTION]
        doc = collection.find_one({'correo': correo})
        
        if doc:
            return from_mongodb_usuario(doc)
        return None
    except Exception as error:
        print(f"Error fetching usuario by correo: {error}")
        return None

async def update_solicitud(id: str, update_data: dict) -> bool:
    """Actualizar una solicitud"""
    if not id:
        return False
    
    try:
        db = mongodb.get_database()
        collection = db[SOLICITUDES_COLLECTION]
        result = collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': update_data}
        )
        return result.modified_count == 1
    except InvalidId:
        print(f"ID inválido: {id}")
        return False
    except Exception as error:
        print(f"Error updating solicitud: {error}")
        return False