from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.routers import categorias, productos, inventario, pedidos, administradores, auth
from app.database import engine

app = FastAPI(
    title="API Plataforma de Bisutería",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
) 

app.include_router(categorias.router)

app.include_router(productos.router)

app.include_router(inventario.router)

app.include_router(pedidos.router)

app.include_router(administradores.router)

app.include_router(auth.router)

@app.get("/")
def inicio():
    return {
        "mensaje": "API de la plataforma de bisutería funcionando"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/database-test")
def database_test():
    with engine.connect() as conexion:
        resultado = conexion.execute(
            text("SELECT current_database(), current_user")
        ).fetchone()

    return {
        "base_datos": resultado[0],
        "usuario": resultado[1],
        "conexion": "correcta"
    }

