from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Producto
from app.schemas import BusquedaResultado
from app.busqueda import buscar_productos_semanticos


router = APIRouter(
    prefix="/busqueda",
    tags=["Búsqueda inteligente"]
)


@router.get(
    "/",
    response_model=list[BusquedaResultado]
)
def buscar_productos(
    q: str = Query(
        ...,
        min_length=2,
        description="Texto que desea buscar el cliente"
    ),
    limite: int = Query(
        5,
        ge=1,
        le=20
    ),
    db: Session = Depends(get_db)
):

    productos = db.scalars(
        select(Producto).where(
            Producto.activo == True
        )
    ).all()


    resultados = buscar_productos_semanticos(
        consulta=q,
        productos=list(productos),
        limite=limite
    )


    return [
        {
            "producto": producto,
            "similitud": float(similitud)
        }
        for producto, similitud in resultados
    ]