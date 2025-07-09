from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from lib.data import get_usuarios, add_usuario, upload_documento
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

@app.get("/api/usuarios")
async def listar_usuarios():
    return await get_usuarios()

@app.post("/api/agregarUsuarios")
async def crear_usuario(usuario: Usuario):
    return await add_usuario(usuario)

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