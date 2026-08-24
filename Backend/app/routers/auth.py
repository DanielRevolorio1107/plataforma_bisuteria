from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Administrador
from app.schemas import LoginRequest, TokenResponse
from app.security import verificar_password, crear_token


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
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
            Administrador.usuario == datos.usuario
        )
    ).scalar_one_or_none()

    if not administrador:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    if not administrador.activo:
        raise HTTPException(
            status_code=403,
            detail="El administrador está desactivado"
        )

    password_correcto = verificar_password(
        datos.password,
        administrador.password_hash
    )

    if not password_correcto:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    token = crear_token(
        administrador.id_administrador,
        administrador.usuario
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }