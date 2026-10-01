import os
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from azure.identity import DefaultAzureCredential
from azure.storage.blob import (
    BlobServiceClient,
    ContentSettings
)
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


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)


CARPETA_PRODUCTOS = (
    BASE_DIR
    / "uploads"
    / "productos"
)

CARPETA_PRODUCTOS.mkdir(
    parents=True,
    exist_ok=True
)


STORAGE_ACCOUNT_URL = os.getenv(
    "STORAGE_ACCOUNT_URL"
)

STORAGE_CONTAINER = os.getenv(
    "STORAGE_CONTAINER",
    "productos"
)

AZURE_CLIENT_ID = os.getenv(
    "AZURE_CLIENT_ID"
)


FORMATOS_PERMITIDOS = {
    "JPEG": {
        "extension": ".jpg",
        "content_type": "image/jpeg"
    },
    "PNG": {
        "extension": ".png",
        "content_type": "image/png"
    },
    "WEBP": {
        "extension": ".webp",
        "content_type": "image/webp"
    }
}


def crear_blob_service_client():

    if not STORAGE_ACCOUNT_URL:

        return None


    credential = DefaultAzureCredential(
        managed_identity_client_id=AZURE_CLIENT_ID
    )


    return BlobServiceClient(
        account_url=STORAGE_ACCOUNT_URL,
        credential=credential
    )


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
            detail=(
                "La imagen no puede "
                "superar los 5 MB"
            )
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
            detail=(
                "El archivo no es "
                "una imagen válida"
            )
        )


    if formato not in FORMATOS_PERMITIDOS:

        raise HTTPException(
            status_code=400,
            detail=(
                "Solo se permiten imágenes "
                "JPG, PNG o WEBP"
            )
        )


    extension = FORMATOS_PERMITIDOS[
        formato
    ]["extension"]

    content_type = FORMATOS_PERMITIDOS[
        formato
    ]["content_type"]


    nombre_archivo = (
        f"{uuid4().hex}{extension}"
    )


    if STORAGE_ACCOUNT_URL:

        try:

            blob_service_client = (
                crear_blob_service_client()
            )

            blob_client = (
                blob_service_client
                .get_blob_client(
                    container=STORAGE_CONTAINER,
                    blob=nombre_archivo
                )
            )

            blob_client.upload_blob(
                contenido,
                overwrite=False,
                content_settings=ContentSettings(
                    content_type=content_type
                )
            )

            imagen_url = (
                f"{STORAGE_ACCOUNT_URL}/"
                f"{STORAGE_CONTAINER}/"
                f"{nombre_archivo}"
            )

        except Exception:

            raise HTTPException(
                status_code=500,
                detail=(
                    "No se pudo guardar "
                    "la imagen en Azure"
                )
            )

    else:

        ruta = (
            CARPETA_PRODUCTOS
            / nombre_archivo
        )

        try:

            ruta.write_bytes(
                contenido
            )

        except OSError:

            raise HTTPException(
                status_code=500,
                detail=(
                    "No se pudo guardar "
                    "la imagen"
                )
            )


        imagen_url = (
            "http://127.0.0.1:8000"
            f"/media/productos/"
            f"{nombre_archivo}"
        )


    return {
        "imagen_url": imagen_url
    }