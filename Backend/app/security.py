import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidTokenError
)
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Administrador


load_dotenv()


password_hash = PasswordHash.recommended()


SECRET_KEY = os.getenv("JWT_SECRET")

ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256"
)

EXPIRE_MINUTES = int(
    os.getenv(
        "JWT_EXPIRE_MINUTES",
        "60"
    )
)


if not SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET no está configurado "
        "en el archivo .env"
    )


security_scheme = HTTPBearer(
    auto_error=False
)


def generar_hash(
    password: str
) -> str:

    return password_hash.hash(
        password
    )


def verificar_password(
    password: str,
    password_guardado: str
) -> bool:

    return password_hash.verify(
        password,
        password_guardado
    )


def crear_token(
    id_administrador: int,
    usuario: str
) -> str:

    expiracion = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=EXPIRE_MINUTES
        )
    )


    datos = {
        "sub": str(id_administrador),
        "usuario": usuario,
        "exp": expiracion
    }


    return jwt.encode(
        datos,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def obtener_administrador_actual(
    credenciales:
        HTTPAuthorizationCredentials | None
        = Depends(security_scheme),

    db: Session = Depends(get_db)

) -> Administrador:

    if credenciales is None:
        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail="No se proporcionó un token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    token = credenciales.credentials


    try:

        datos = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[
                ALGORITHM
            ]
        )


        id_administrador = int(
            datos["sub"]
        )


        if id_administrador <= 0:
            raise ValueError


    except ExpiredSignatureError:

        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail="El token ha expirado",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    except (
        InvalidTokenError,
        KeyError,
        ValueError,
        TypeError
    ):

        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail="Token inválido",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    administrador = db.get(
        Administrador,
        id_administrador
    )


    if not administrador:
        raise HTTPException(
            status_code=(
                status.HTTP_401_UNAUTHORIZED
            ),
            detail=(
                "Administrador no encontrado"
            ),
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    if not administrador.activo:
        raise HTTPException(
            status_code=(
                status.HTTP_403_FORBIDDEN
            ),
            detail=(
                "Administrador desactivado"
            )
        )


    return administrador