from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Inventario, Administrador
from app.schemas import InventarioResponse, InventarioUpdate
from app.security import obtener_administrador_actual


router = APIRouter(
    prefix="/inventario",
    tags=["Inventario"]
)


@router.get(
    "/",
    response_model=list[InventarioResponse]
)
def listar_inventario(
    db: Session = Depends(get_db),
    administrador: Administrador = Depends(
        obtener_administrador_actual
    )
):
    resultado = db.execute(
        select(Inventario).order_by(
            Inventario.id_inventario
        )
    )

    return resultado.scalars().all()


@router.put(
    "/{id_producto}",
    response_model=InventarioResponse
)
def actualizar_inventario(
    id_producto: int,
    datos: InventarioUpdate,
    db: Session = Depends(get_db),
    administrador: Administrador = Depends(
        obtener_administrador_actual
    )
):
    inventario = db.execute(
        select(Inventario).where(
            Inventario.id_producto == id_producto
        )
    ).scalar_one_or_none()

    if not inventario:
        raise HTTPException(
            status_code=404,
            detail="No existe inventario para este producto"
        )

    if (
        datos.stock_actual < 0
        or datos.stock_minimo < 0
    ):
        raise HTTPException(
            status_code=400,
            detail="El stock no puede ser negativo"
        )

    inventario.stock_actual = datos.stock_actual
    inventario.stock_minimo = datos.stock_minimo

    db.commit()
    db.refresh(inventario)

    return inventario