from io import BytesIO
from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile
)

from PIL import (
    Image,
    UnidentifiedImageError
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


FORMATOS_PERMITIDOS = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "WEBP": ".webp"
}


@router.post("/producto")
async def subir_imagen_producto(
    archivo: UploadFile = File(...),
    administrador: Administrador = Depends(
        obtener_administrador_actual
    )
):

    contenido = await archivo.read()

    await archivo.close()


    if not contenido:

        raise HTTPException(
            status_code=400,
            detail="La imagen está vacía"
        )


    if len(contenido) > 5 * 1024 * 1024:

        raise HTTPException(
            status_code=400,
            detail="La imagen no puede superar los 5 MB"
        )


    try:

        imagen = Image.open(
            BytesIO(contenido)
        )

        formato = imagen.format

        imagen.verify()

    except (
        UnidentifiedImageError,
        OSError,
        SyntaxError
    ):

        raise HTTPException(
            status_code=400,
            detail="El archivo no es una imagen válida"
        )


    if formato not in FORMATOS_PERMITIDOS:

        raise HTTPException(
            status_code=400,
            detail="Solo se permiten imágenes JPG, PNG o WEBP"
        )


    extension = FORMATOS_PERMITIDOS[
        formato
    ]


    nombre_archivo = (
        f"{uuid4().hex}{extension}"
    )


    ruta = (
        CARPETA_PRODUCTOS /
        nombre_archivo
    )


    try:

        ruta.write_bytes(
            contenido
        )

    except OSError:

        raise HTTPException(
            status_code=500,
            detail="No se pudo guardar la imagen"
        )


    return {
        "imagen_url":
            "http://127.0.0.1:8000/"
            f"media/productos/{nombre_archivo}"
    }