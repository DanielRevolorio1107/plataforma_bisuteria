import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import (
    categorias,
    productos,
    inventario,
    pedidos,
    administradores,
    auth,
    busqueda,
    recomendaciones,
    uploads
)


load_dotenv()


app = FastAPI(
    title="API Plataforma de Bisutería",
    version="1.0.0"
)


BASE_DIR = Path(__file__).resolve().parent.parent

CARPETA_UPLOADS = BASE_DIR / "uploads"

CARPETA_UPLOADS.mkdir(
    parents=True,
    exist_ok=True
)


app.mount(
    "/media",
    StaticFiles(
        directory=str(CARPETA_UPLOADS)
    ),
    name="media"
)


FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:4200"
)


origenes_permitidos = [
    FRONTEND_URL
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes_permitidos,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(
    categorias.router
)

app.include_router(
    productos.router
)

app.include_router(
    inventario.router
)

app.include_router(
    pedidos.router
)

app.include_router(
    administradores.router
)

app.include_router(
    auth.router
)

app.include_router(
    busqueda.router
)

app.include_router(
    recomendaciones.router
)

app.include_router(
    uploads.router
)


@app.get("/")
def inicio():

    return {
        "mensaje":
            "API de la plataforma de bisutería funcionando"
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }