from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Administrador
from app.schemas import LoginRequest, TokenResponse
from app.security import (
    generar_hash,
    verificar_password,
    crear_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


HASH_FALSO = generar_hash(
    "password_falso_para_validacion"
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    datos: LoginRequest,
    db: Session = Depends(get_db)
):

    administrador = db.execute(
        select(Administrador).where(
            Administrador.usuario
            == datos.usuario
        )
    ).scalar_one_or_none()


    if not administrador:

        verificar_password(
            datos.password,
            HASH_FALSO
        )

        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail=(
                "Usuario o contraseña incorrectos"
            ),
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    password_correcto = verificar_password(
        datos.password,
        administrador.password_hash
    )


    if (
        not password_correcto
        or not administrador.activo
    ):

        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail=(
                "Usuario o contraseña incorrectos"
            ),
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    token = crear_token(
        administrador.id_administrador,
        administrador.usuario
    )


    return {
        "access_token": token,
        "token_type": "bearer"
    }