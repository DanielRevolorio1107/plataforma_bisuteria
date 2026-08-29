from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Producto
from app.schemas import RecomendacionResultado
from app.recomendaciones import recomendar_productos


router = APIRouter(
    prefix="/recomendaciones",
    tags=["Recomendaciones"]
)


@router.get(
    "/{id_producto}",
    response_model=list[RecomendacionResultado]
)
def obtener_recomendaciones(
    id_producto: int,
    limite: int = 4,
    db: Session = Depends(get_db)
):

    producto_base = db.get(
        Producto,
        id_producto
    )


    if (
        not producto_base or
        not producto_base.activo
    ):
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )


    productos = db.scalars(
        select(Producto).where(
            Producto.activo == True
        )
    ).all()


    resultados = recomendar_productos(
        producto_base=producto_base,
        productos=list(productos),
        limite=limite
    )


    return [
        {
            "producto": producto,
            "puntuacion": float(puntuacion)
        }
        for producto, puntuacion in resultados
    ]