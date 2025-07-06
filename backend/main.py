from fastapi import FastAPI, HTTPException
from lib.data import get_usuarios, add_usuario
from lib.modelos import Usuario
from lib.mongodb import mongodb
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O especifica tu origen, ej: ["http://localhost:19006"]
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