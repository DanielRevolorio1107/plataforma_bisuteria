from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Categoria, Producto, Inventario, Administrador
from app.schemas import ProductoCreate, ProductoResponse, ProductoUpdate
from app.security import obtener_administrador_actual
from app.models import Producto, Inventario

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


@router.get(
    "/",
    response_model=list[ProductoResponse]
)
def listar_productos(
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Producto)
        .where(Producto.activo == True)
        .order_by(Producto.id_producto)
    )

    return resultado.scalars().all()


@router.get(
    "/admin/todos",
    response_model=list[ProductoResponse]
)
def listar_productos_admin(
    db: Session = Depends(get_db),
    admin: Administrador = Depends(obtener_administrador_actual)
):
    resultado = db.execute(
        select(Producto).order_by(Producto.id_producto)
    )

    return resultado.scalars().all()


@router.post(
    "/",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db),
    admin: Administrador = Depends(obtener_administrador_actual)
):
    categoria = db.get(Categoria, producto.id_categoria)

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="La categoría indicada no existe"
        )

    codigo_existente = db.execute(
        select(Producto).where(
            Producto.codigo == producto.codigo
        )
    ).scalar_one_or_none()

    if codigo_existente:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un producto con ese código"
        )

    nuevo_producto = Producto(
        **producto.model_dump()
    )

    db.add(nuevo_producto)
    db.flush()

    nuevo_inventario = Inventario(
        id_producto=nuevo_producto.id_producto,
        stock_actual=0,
        stock_minimo=0
    )

    db.add(nuevo_inventario)
    db.commit()
    db.refresh(nuevo_producto)

    return nuevo_producto


@router.patch(
    "/{id_producto}/activar",
    response_model=ProductoResponse
)
def activar_producto(
    id_producto: int,
    db: Session = Depends(get_db),
    admin: Administrador = Depends(obtener_administrador_actual)
):
    producto = db.get(Producto, id_producto)

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="El producto no existe"
        )

    producto.activo = True

    db.commit()
    db.refresh(producto)

    return producto


@router.get(
    "/{id_producto}",
    response_model=ProductoResponse
)
def obtener_producto(
    id_producto: int,
    db: Session = Depends(get_db)
):
    producto = db.get(Producto, id_producto)

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="El producto no existe"
        )

    return producto


@router.patch(
    "/{id_producto}",
    response_model=ProductoResponse
)
def actualizar_producto(
    id_producto: int,
    datos: ProductoUpdate,
    db: Session = Depends(get_db),
    admin: Administrador = Depends(obtener_administrador_actual)
):
    producto = db.get(Producto, id_producto)

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="El producto no existe"
        )

    cambios = datos.model_dump(exclude_unset=True)

    if "id_categoria" in cambios:
        categoria = db.get(
            Categoria,
            cambios["id_categoria"]
        )

        if not categoria:
            raise HTTPException(
                status_code=404,
                detail="La categoría indicada no existe"
            )

    if (
        "precio" in cambios
        and cambios["precio"] is not None
        and cambios["precio"] < 0
    ):
        raise HTTPException(
            status_code=400,
            detail="El precio no puede ser negativo"
        )

    for campo, valor in cambios.items():
        setattr(producto, campo, valor)

    db.commit()
    db.refresh(producto)

    return producto


@router.delete(
    "/{id_producto}",
    response_model=ProductoResponse
)
def desactivar_producto(
    id_producto: int,
    db: Session = Depends(get_db),
    admin: Administrador = Depends(obtener_administrador_actual)
):
    producto = db.get(Producto, id_producto)

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="El producto no existe"
        )

    producto.activo = False

    db.commit()
    db.refresh(producto)

    return producto

@router.get("/{id_producto}/disponibilidad")
def obtener_disponibilidad(
    id_producto: int,
    db: Session = Depends(get_db)
):

    producto = db.get(
        Producto,
        id_producto
    )

    if not producto or not producto.activo:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    inventario = db.query(Inventario).filter(
        Inventario.id_producto == id_producto
    ).first()

    if not inventario:
        return {
            "id_producto": id_producto,
            "stock_disponible": 0
        }

    return {
        "id_producto": id_producto,
        "stock_disponible": inventario.stock_actual
    }