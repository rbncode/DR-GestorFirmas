from pydantic import BaseModel, ConfigDict
import datetime
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId

class RolUsuario(str, Enum):
    EMPLEADO = "empleado"
    SUPERVISOR = "supervisor"
    HR = "hr"

class Estado(str, Enum):
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"
    PENDIENTE = "pendiente"

class Usuario(BaseModel):
    nombre: str
    correo: str
    rol: RolUsuario
    contraseña: str

class UsuarioSolicitud(BaseModel):
    nombre: str
    correo: str
    rol: RolUsuario

class UsuarioWithId(Usuario):
    id: str

class Solicitudes(BaseModel):
    id: str
    titulo: str
    categoria: str
    descripcion: str
    fecha: str  # ISO string
    empleado: Usuario
    supervisor: Usuario
    hr: Usuario
    documentoId: str  # Referencia al documento PDF

class SolicitudCreate(BaseModel):
    titulo: str
    categoria: str
    descripcion: str
    fecha: str
    empleado: UsuarioSolicitud
    supervisor: UsuarioSolicitud
    hr: UsuarioSolicitud
    documentoId: str

class DocumentoFirmado(BaseModel):
    id: str
    solicitud_id: str
    filename: str
    content_type: str
    upload_date: datetime.datetime
    length: int
    firmado: bool = False
    firmado_por: Optional[Usuario] = None
    fecha_firma: Optional[datetime.datetime] = None
    metadata: Optional[dict] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

class DocumentoUpload(BaseModel):
    solicitud_id: str
    filename: str
    content_type: str
    metadata: Optional[dict] = None

class FirmaDocumento(BaseModel):
    documento_id: str
    firmado_por: str
    fecha_firma: datetime.datetime
    metadata_firma: Optional[dict] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)