from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Administrador
from app.schemas import AdministradorCreate, AdministradorResponse
from app.security import generar_hash, obtener_administrador_actual


router = APIRouter(
    prefix="/administradores",
    tags=["Administradores"]
)


@router.post(
    "/",
    response_model=AdministradorResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_administrador(
    datos: AdministradorCreate,
    db: Session = Depends(get_db),
    admin_actual: Administrador = Depends(
        obtener_administrador_actual
    )
):
    existente = db.execute(
        select(Administrador).where(
            Administrador.usuario == datos.usuario
        )
    ).scalar_one_or_none()

    if existente:
        raise HTTPException(
            status_code=409,
            detail="El nombre de usuario ya existe"
        )

    hash_password = generar_hash(datos.password)

    nuevo_administrador = Administrador(
        nombre=datos.nombre,
        usuario=datos.usuario,
        password_hash=hash_password
    )

    db.add(nuevo_administrador)
    db.commit()
    db.refresh(nuevo_administrador)

    return nuevo_administrador