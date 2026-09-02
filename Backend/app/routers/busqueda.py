from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Categoria, Producto
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

    resultado = db.execute(
        select(
            Producto,
            Categoria.nombre
        )
        .join(
            Categoria,
            Producto.id_categoria
            == Categoria.id_categoria
        )
        .where(
            Producto.activo.is_(True),
            Categoria.activo.is_(True)
        )
    ).all()

    productos = [
        fila[0]
        for fila in resultado
    ]

    categorias_por_producto = {
        fila[0].id_producto: fila[1]
        for fila in resultado
    }

    resultados = buscar_productos_semanticos(
        consulta=q,
        productos=productos,
        categorias_por_producto=(
            categorias_por_producto
        ),
        limite=limite
    )

    return [
        {
            "producto": producto,
            "similitud": float(similitud)
        }
        for producto, similitud in resultados
    ]