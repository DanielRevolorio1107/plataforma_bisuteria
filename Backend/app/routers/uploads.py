from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile
)

from app.models import Administrador
from app.security import obtener_administrador_actual


router = APIRouter(
    prefix="/uploads",
    tags=["Imágenes"]
)


CARPETA_PRODUCTOS = Path(
    "uploads/productos"
)

CARPETA_PRODUCTOS.mkdir(
    parents=True,
    exist_ok=True
)


TIPOS_PERMITIDOS = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp"
}


@router.post("/producto")
async def subir_imagen_producto(
    archivo: UploadFile = File(...),
    administrador: Administrador = Depends(
        obtener_administrador_actual
    )
):

    if archivo.content_type not in TIPOS_PERMITIDOS:

        raise HTTPException(
            status_code=400,
            detail="Solo se permiten imágenes JPG, PNG o WEBP"
        )


    contenido = await archivo.read()


    # Máximo 5 MB
    if len(contenido) > 5 * 1024 * 1024:

        raise HTTPException(
            status_code=400,
            detail="La imagen no puede superar los 5 MB"
        )


    extension = TIPOS_PERMITIDOS[
        archivo.content_type
    ]


    nombre_archivo = (
        f"{uuid4().hex}{extension}"
    )


    ruta = (
        CARPETA_PRODUCTOS /
        nombre_archivo
    )


    ruta.write_bytes(
        contenido
    )


    return {
        "imagen_url":
            "http://127.0.0.1:8000/"
            f"media/productos/{nombre_archivo}"
    }