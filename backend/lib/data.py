from typing import List, Optional
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from .modelos import Usuario, UsuarioWithId, Solicitudes, SolicitudCreate, DocumentoFirmado, DocumentoUpload, FirmaDocumento
from .mongodb import mongodb
from .gridfs_manager import gridfs

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

#Metodos para ingresar Documentos

async def upload_documento(file_data: bytes, documento_info: DocumentoUpload) -> str:
    """Subir un documento a GridFS"""
    try:
        # Preparar metadatos
        metadata = {
            'solicitud_id': documento_info.solicitud_id,
            'content_type': documento_info.content_type,
            'tipo': 'documento',
            'firmado': False,
            'estado': 'pendiente'
        }
        
        # Agregar metadatos adicionales si los hay
        if documento_info.metadata:
            metadata.update(documento_info.metadata)
        
        # Subir archivo usando GridFS
        file_id = await gridfs.upload_file(
            file_data=file_data,
            filename=documento_info.filename,
            metadata=metadata
        )
        
        # Actualizar la solicitud con el ID del documento
        await update_solicitud(documento_info.solicitud_id, {'documentoId': file_id})
        
        return file_id
        
    except Exception as error:
        print(f"Error uploading documento: {error}")
        raise error

async def get_documento_by_id(documento_id: str) -> Optional[DocumentoFirmado]:
    """Obtener un documento por ID"""
    try:
        file_data = await gridfs.download_file(documento_id)
        if file_data:
            return from_gridfs_documento(file_data)
        return None
    except Exception as error:
        print(f"Error fetching documento: {error}")
        return None

async def download_documento(documento_id: str) -> Optional[dict]:
    """Descargar un documento completo con sus datos"""
    try:
        return await gridfs.download_file(documento_id)
    except Exception as error:
        print(f"Error downloading documento: {error}")
        return None

async def get_documentos_by_solicitud(solicitud_id: str) -> List[DocumentoFirmado]:
    """Obtener todos los documentos de una solicitud"""
    try:
        filter_metadata = {'solicitud_id': solicitud_id}
        files = await gridfs.list_files(filter_metadata)
        
        return [from_gridfs_documento(file_data) for file_data in files]
    except Exception as error:
        print(f"Error fetching documentos by solicitud: {error}")
        return []

async def firmar_documento(firma_data: FirmaDocumento) -> bool:
    """Firmar un documento"""
    try:
        # Obtener metadatos actuales
        file_data = await gridfs.download_file(firma_data.documento_id)
        if not file_data:
            return False
        
        # Actualizar metadatos con información de firma
        new_metadata = file_data['metadata'].copy()
        new_metadata.update({
            'firmado': True,
            'firmado_por': firma_data.firmado_por,
            'fecha_firma': firma_data.fecha_firma,
            'estado': 'firmado'
        })
        
        # Agregar metadatos adicionales de firma si los hay
        if firma_data.metadata_firma:
            new_metadata.update(firma_data.metadata_firma)
        
        # Actualizar metadatos
        return await gridfs.update_file_metadata(
            firma_data.documento_id, 
            new_metadata
        )
        
    except Exception as error:
        print(f"Error firmando documento: {error}")
        return False

async def delete_documento(documento_id: str) -> bool:
    """Eliminar un documento"""
    try:
        return await gridfs.delete_file(documento_id)
    except Exception as error:
        print(f"Error deleting documento: {error}")
        return False

async def get_documentos_firmados() -> List[DocumentoFirmado]:
    """Obtener todos los documentos firmados"""
    try:
        filter_metadata = {'firmado': True}
        files = await gridfs.list_files(filter_metadata)
        
        return [from_gridfs_documento(file_data) for file_data in files]
    except Exception as error:
        print(f"Error fetching documentos firmados: {error}")
        return []

async def get_documentos_pendientes() -> List[DocumentoFirmado]:
    """Obtener todos los documentos pendientes de firma"""
    try:
        filter_metadata = {'firmado': False}
        files = await gridfs.list_files(filter_metadata)
        
        return [from_gridfs_documento(file_data) for file_data in files]
    except Exception as error:
        print(f"Error fetching documentos pendientes: {error}")
        return []