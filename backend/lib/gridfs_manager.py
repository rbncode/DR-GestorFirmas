import gridfs as mongo_gridfs
import io
from typing import Optional, List, Dict, Any
from bson import ObjectId
from bson.errors import InvalidId
from .mongodb import mongodb

class GridFSManager:
    def __init__(self):
        self.fs = None
    
    def initialize(self):
        """Inicializar GridFS con la base de datos"""
        if mongodb.db is None:
            raise Exception("MongoDB no está conectado")
        self.fs = mongo_gridfs.GridFS(mongodb.db)
    
    async def upload_file(self, file_data: bytes, filename: str, metadata: Dict[str, Any] = None) -> str:
        """
        Subir un archivo a GridFS
        
        Args:
            file_data: Datos del archivo en bytes
            filename: Nombre del archivo
            metadata: Metadatos adicionales (opcional)
            
        Returns:
            str: ID del archivo subido
        """
        try:
            if self.fs is None:
                self.initialize()
            
            # Metadatos por defecto
            file_metadata = {
                'tipo': 'documento',
                'estado': 'activo',
                'firmado': False
            }
            
            # Agregar metadatos personalizados
            if metadata:
                file_metadata.update(metadata)
            
            # Subir archivo
            file_id = self.fs.put(
                file_data,
                filename=filename,
                metadata=file_metadata
            )
            
            return str(file_id)
            
        except Exception as e:
            print(f"Error subiendo archivo: {e}")
            raise e
    
    async def download_file(self, file_id: str) -> Optional[Dict[str, Any]]:
        """
        Descargar un archivo de GridFS
        
        Args:
            file_id: ID del archivo
            
        Returns:
            Dict con datos del archivo y metadatos
        """
        try:
            if self.fs is None:
                self.initialize()
            
            # Obtener archivo por ID
            file_doc = self.fs.get(ObjectId(file_id))
            
            return {
                'id': str(file_doc._id),
                'filename': file_doc.filename,
                'data': file_doc.read(),
                'metadata': file_doc.metadata,
                'upload_date': file_doc.upload_date,
                'length': file_doc.length,
                'content_type': file_doc.metadata.get('content_type', 'application/octet-stream')
            }
            
        except InvalidId:
            print(f"ID inválido: {file_id}")
            return None
        except gridfs.NoFile:
            print(f"Archivo no encontrado: {file_id}")
            return None
        except Exception as e:
            print(f"Error descargando archivo: {e}")
            return None
    
    async def download_file_by_name(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Descargar un archivo por nombre
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            Dict con datos del archivo y metadatos
        """
        try:
            if self.fs is None:
                self.initialize()
            
            # Obtener la última versión del archivo
            file_doc = self.fs.get_last_version(filename)
            
            return {
                'id': str(file_doc._id),
                'filename': file_doc.filename,
                'data': file_doc.read(),
                'metadata': file_doc.metadata,
                'upload_date': file_doc.upload_date,
                'length': file_doc.length,
                'content_type': file_doc.metadata.get('content_type', 'application/octet-stream')
            }
            
        except gridfs.NoFile:
            print(f"Archivo no encontrado: {filename}")
            return None
        except Exception as e:
            print(f"Error descargando archivo: {e}")
            return None
    
    async def list_files(self, filter_metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Listar archivos en GridFS
        
        Args:
            filter_metadata: Filtros para metadatos
            
        Returns:
            Lista de archivos con metadatos
        """
        try:
            if self.fs is None:
                self.initialize()
            
            # Construir filtro
            query = {}
            if filter_metadata:
                for key, value in filter_metadata.items():
                    query[f'metadata.{key}'] = value
            
            # Buscar archivos
            files = self.fs.find(query)
            
            result = []
            for file_doc in files:
                result.append({
                    'id': str(file_doc._id),
                    'filename': file_doc.filename,
                    'metadata': file_doc.metadata,
                    'upload_date': file_doc.upload_date,
                    'length': file_doc.length,
                    'content_type': file_doc.metadata.get('content_type', 'application/octet-stream')
                })
            
            return result
            
        except Exception as e:
            print(f"Error listando archivos: {e}")
            return []
    
    async def delete_file(self, file_id: str) -> bool:
        """
        Eliminar un archivo de GridFS
        
        Args:
            file_id: ID del archivo
            
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            if self.fs is None:
                self.initialize()
            
            self.fs.delete(ObjectId(file_id))
            return True
            
        except InvalidId:
            print(f"ID inválido: {file_id}")
            return False
        except gridfs.NoFile:
            print(f"Archivo no encontrado: {file_id}")
            return False
        except Exception as e:
            print(f"Error eliminando archivo: {e}")
            return False
    
    async def update_file_metadata(self, file_id: str, new_metadata: Dict[str, Any]) -> bool:
        """
        Actualizar metadatos de un archivo
        
        Args:
            file_id: ID del archivo
            new_metadata: Nuevos metadatos
            
        Returns:
            bool: True si se actualizó correctamente
        """
        try:
            if self.fs is None:
                self.initialize()
            
            # GridFS no permite actualizar metadatos directamente
            # Necesitamos actualizar en la colección fs.files
            db = mongodb.get_database()
            files_collection = db['fs.files']
            
            result = files_collection.update_one(
                {'_id': ObjectId(file_id)},
                {'$set': {'metadata': new_metadata}}
            )
            
            return result.modified_count == 1
            
        except InvalidId:
            print(f"ID inválido: {file_id}")
            return False
        except Exception as e:
            print(f"Error actualizando metadatos: {e}")
            return False
    
    async def file_exists(self, file_id: str) -> bool:
        """
        Verificar si un archivo existe
        
        Args:
            file_id: ID del archivo
            
        Returns:
            bool: True si existe
        """
        try:
            if self.fs is None:
                self.initialize()
            
            return self.fs.exists(ObjectId(file_id))
            
        except InvalidId:
            return False
        except Exception as e:
            print(f"Error verificando existencia del archivo: {e}")
            return False

# Instancia global del gestor de archivos
gridfs = GridFSManager()