from fastapi import Body, FastAPI, HTTPException, UploadFile, File, Form
from lib.data import (
    get_usuarios, add_usuario, upload_documento, get_usuario_by_id, delete_usuario, get_usuario_by_correo,
    get_solicitudes, get_solicitud_by_id, add_solicitud, delete_solicitud, update_solicitud,
    get_documento_by_id, download_documento, get_documentos_by_solicitud,
    firmar_documento, delete_documento, get_documentos_firmados, get_documentos_pendientes
)
from lib.modelos import Usuario, Solicitudes, SolicitudCreate, DocumentoUpload, DocumentoFirmado, FirmaDocumento
from lib.mongodb import mongodb
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await mongodb.connect()

# -- ENDPOINTS USUARIOS

@app.get("/api/usuarios")
async def listar_usuarios():
    return await get_usuarios()

@app.get("/api/usuarios/{usuario_id}")
async def obtener_usuario(usuario_id: str):
    usuario = await get_usuario_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.get("/api/usuarios/correo/{correo}")
async def obtener_usuario_por_correo(correo: str):
    usuario = await get_usuario_by_correo(correo)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.post("/api/agregarUsuarios")
async def crear_usuario(usuario: Usuario):
    return await add_usuario(usuario)

@app.delete("/api/usuarios/{usuario_id}")
async def eliminar_usuario(usuario_id: str):
    ok = await delete_usuario(usuario_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no eliminado")
    return {"message": "Usuario eliminado"}

# -- ENDPOINTS SOLICITUDES

@app.get("/api/solicitudes")
async def listar_solicitudes():
    return await get_solicitudes()

@app.get("/api/solicitudes/{solicitud_id}")
async def obtener_solicitud(solicitud_id: str):
    solicitud = await get_solicitud_by_id(solicitud_id)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return solicitud

@app.post("/api/solicitudes")
async def crear_solicitud(solicitud: SolicitudCreate):
    return await add_solicitud(solicitud)

@app.delete("/api/solicitudes/{solicitud_id}")
async def eliminar_solicitud(solicitud_id: str):
    ok = await delete_solicitud(solicitud_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada o no eliminada")
    return {"message": "Solicitud eliminada"}

@app.put("/api/solicitudes/{solicitud_id}")
async def actualizar_solicitud(solicitud_id: str, update_data: dict = Body(...)):
    ok = await update_solicitud(solicitud_id, update_data)
    if not ok:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada o no actualizada")
    return {"message": "Solicitud actualizada"}

# -- ENDPOINTS DOCUMENTOS

@app.post("/api/agregarPDF")
async def test_upload_pdf(
    solicitud_id: str = Form(...),
    filename: str = Form(...),
    file: UploadFile = File(...)
):
    # Solo aceptar PDFs
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF.")
    file_data = await file.read()
    documento_info = DocumentoUpload(
        solicitud_id=solicitud_id,
        filename=filename,
        content_type=file.content_type
    )
    file_id = await upload_documento(file_data, documento_info)
    return {"file_id": file_id, "message": "Archivo PDF subido correctamente"}

@app.get("/api/documentos/{documento_id}")
async def obtener_documento(documento_id: str):
    doc = await get_documento_by_id(documento_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return doc

@app.get("/api/documentos/{documento_id}/descargar")
async def descargar_documento(documento_id: str):
    doc = await download_documento(documento_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return doc

@app.get("/api/solicitudes/{solicitud_id}/documentos")
async def documentos_por_solicitud(solicitud_id: str):
    return await get_documentos_by_solicitud(solicitud_id)

# -- ENDPOINTS FIRMAS

@app.post("/api/documentos/firmar")
async def firmar_un_documento(firma: FirmaDocumento):
    ok = await firmar_documento(firma)
    if not ok:
        raise HTTPException(status_code=400, detail="No se pudo firmar el documento")
    return {"message": "Documento firmado"}

@app.delete("/api/documentos/{documento_id}")
async def eliminar_documento(documento_id: str):
    ok = await delete_documento(documento_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Documento no encontrado o no eliminado")
    return {"message": "Documento eliminado"}

@app.get("/api/documentos/firmados")
async def listar_documentos_firmados():
    return await get_documentos_firmados()

@app.get("/api/documentos/pendientes")
async def listar_documentos_pendientes():
    return await get_documentos_pendientes()