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
    empleado: Usuario
    supervisor: Usuario
    hr: Usuario
    documentoId: str