from decimal import Decimal

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db

from app.models import (
    Administrador,
    Categoria,
    Pedido,
    DetallePedido,
    Producto,
    Inventario
)

from app.schemas import (
    PedidoCreate,
    PedidoResponse,
    PedidoDetalleResponse,
    PedidoEstadoUpdate
)

from app.security import (
    obtener_administrador_actual
)


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


@router.post(
    "/",
    response_model=PedidoResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_pedido(
    pedido: PedidoCreate,
    db: Session = Depends(get_db)
):

    ids_productos = [
        item.id_producto
        for item in pedido.productos
    ]

    if (
        len(ids_productos)
        != len(set(ids_productos))
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Un mismo producto no puede "
                "aparecer más de una vez en el pedido"
            )
        )

    productos_ordenados = sorted(
        pedido.productos,
        key=lambda item: item.id_producto
    )

    try:

        nuevo_pedido = Pedido(
            nombre_cliente=pedido.nombre_cliente,
            telefono=pedido.telefono,
            direccion_entrega=(
                pedido.direccion_entrega
            ),
            observaciones=pedido.observaciones,
            estado="pendiente",
            total=Decimal("0.00")
        )

        db.add(nuevo_pedido)
        db.flush()

        total_pedido = Decimal("0.00")

        for item in productos_ordenados:

            producto = db.get(
                Producto,
                item.id_producto
            )

            if not producto:
                raise HTTPException(
                    status_code=404,
                    detail=(
                        f"El producto "
                        f"{item.id_producto} "
                        "no existe"
                    )
                )

            if not producto.activo:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"El producto "
                        f"{producto.nombre} "
                        "no está disponible"
                    )
                )

            categoria = db.get(
                Categoria,
                producto.id_categoria
            )

            if (
                not categoria
                or not categoria.activo
            ):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"El producto "
                        f"{producto.nombre} "
                        "no está disponible"
                    )
                )

            inventario = db.execute(
                select(Inventario)
                .where(
                    Inventario.id_producto
                    == item.id_producto
                )
                .with_for_update()
            ).scalar_one_or_none()

            if not inventario:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"El producto "
                        f"{producto.nombre} "
                        "no tiene inventario"
                    )
                )

            if (
                inventario.stock_actual
                < item.cantidad
            ):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Stock insuficiente para "
                        f"{producto.nombre}. "
                        "Disponible: "
                        f"{inventario.stock_actual}"
                    )
                )

            precio = producto.precio

            detalle = DetallePedido(
                id_pedido=(
                    nuevo_pedido.id_pedido
                ),
                id_producto=(
                    producto.id_producto
                ),
                cantidad=item.cantidad,
                precio_unitario=precio
            )

            db.add(detalle)

            inventario.stock_actual -= (
                item.cantidad
            )

            total_pedido += (
                precio * item.cantidad
            )

        nuevo_pedido.total = total_pedido

        db.commit()
        db.refresh(nuevo_pedido)

        return nuevo_pedido

    except HTTPException:

        db.rollback()
        raise

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=(
                "Ocurrió un error al "
                "registrar el pedido"
            )
        )


@router.get(
    "/",
    response_model=list[PedidoResponse]
)
def listar_pedidos(
    db: Session = Depends(get_db),
    administrador: Administrador = Depends(
        obtener_administrador_actual
    )
):

    resultado = db.execute(
        select(Pedido)
        .order_by(
            Pedido.fecha_pedido.desc()
        )
    )

    return resultado.scalars().all()


@router.get(
    "/{id_pedido}",
    response_model=PedidoDetalleResponse
)
def obtener_pedido(
    id_pedido: int,
    db: Session = Depends(get_db),
    administrador: Administrador = Depends(
        obtener_administrador_actual
    )
):

    pedido = db.get(
        Pedido,
        id_pedido
    )

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="El pedido no existe"
        )

    resultado = db.execute(
        select(DetallePedido).where(
            DetallePedido.id_pedido
            == id_pedido
        )
    )

    detalles = (
        resultado.scalars().all()
    )

    return {
        "id_pedido":
            pedido.id_pedido,

        "nombre_cliente":
            pedido.nombre_cliente,

        "telefono":
            pedido.telefono,

        "direccion_entrega":
            pedido.direccion_entrega,

        "observaciones":
            pedido.observaciones,

        "estado":
            pedido.estado,

        "total":
            pedido.total,

        "fecha_pedido":
            pedido.fecha_pedido,

        "detalles":
            detalles
    }


@router.patch(
    "/{id_pedido}/estado",
    response_model=PedidoResponse
)
def actualizar_estado_pedido(
    id_pedido: int,
    datos: PedidoEstadoUpdate,
    db: Session = Depends(get_db),
    administrador: Administrador = Depends(
        obtener_administrador_actual
    )
):

    transiciones_permitidas = {

        "pendiente": {
            "confirmado",
            "cancelado"
        },

        "confirmado": {
            "preparando",
            "cancelado"
        },

        "preparando": {
            "enviado",
            "cancelado"
        },

        "enviado": {
            "entregado"
        },

        "entregado": set(),

        "cancelado": set()
    }

    pedido = db.get(
        Pedido,
        id_pedido
    )

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="El pedido no existe"
        )

    estado_anterior = pedido.estado
    estado_nuevo = datos.estado

    if estado_anterior == estado_nuevo:
        return pedido

    if (
        estado_anterior
        not in transiciones_permitidas
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "El pedido tiene un estado "
                "no reconocido"
            )
        )

    if (
        estado_nuevo
        not in transiciones_permitidas[
            estado_anterior
        ]
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "No se puede cambiar "
                f"el pedido de "
                f"{estado_anterior} "
                f"a {estado_nuevo}"
            )
        )

    try:

        if estado_nuevo == "cancelado":

            resultado = db.execute(
                select(DetallePedido)
                .where(
                    DetallePedido.id_pedido
                    == id_pedido
                )
                .order_by(
                    DetallePedido.id_producto
                )
            )

            detalles = (
                resultado.scalars().all()
            )

            for detalle in detalles:

                inventario = db.execute(
                    select(Inventario)
                    .where(
                        Inventario.id_producto
                        == detalle.id_producto
                    )
                    .with_for_update()
                ).scalar_one_or_none()

                if not inventario:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            "No se pudo devolver "
                            "el inventario del "
                            "producto "
                            f"{detalle.id_producto}"
                        )
                    )

                inventario.stock_actual += (
                    detalle.cantidad
                )

        pedido.estado = estado_nuevo

        db.commit()
        db.refresh(pedido)

        return pedido

    except HTTPException:

        db.rollback()
        raise

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=(
                "Ocurrió un error al "
                "actualizar el pedido"
            )
        )