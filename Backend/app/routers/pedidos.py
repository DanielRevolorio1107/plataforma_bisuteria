from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Administrador
from app.database import get_db
from app.models import (
    Pedido,
    DetallePedido,
    Producto,
    Inventario
)
from app.schemas import (
    PedidoCreate,
    PedidoResponse,
    PedidoDetalleResponse,
    DetallePedidoResponse,
    PedidoEstadoUpdate
)

from app.models import Administrador
from app.security import obtener_administrador_actual

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
    if not pedido.productos:
        raise HTTPException(
            status_code=400,
            detail="El pedido debe contener al menos un producto"
        )

    try:
        nuevo_pedido = Pedido(
            nombre_cliente=pedido.nombre_cliente,
            telefono=pedido.telefono,
            direccion_entrega=pedido.direccion_entrega,
            observaciones=pedido.observaciones,
            estado="pendiente",
            total=Decimal("0.00")
        )

        db.add(nuevo_pedido)
        db.flush()

        total_pedido = Decimal("0.00")

        for item in pedido.productos:

            # Buscar el producto
            producto = db.get(
                Producto,
                item.id_producto
            )

            if not producto:
                raise HTTPException(
                    status_code=404,
                    detail=f"El producto {item.id_producto} no existe"
                )

            if not producto.activo:
                raise HTTPException(
                    status_code=400,
                    detail=f"El producto {producto.nombre} no está disponible"
                )

            # Buscar su inventario
            inventario = db.execute(
                select(Inventario).where(
                    Inventario.id_producto == item.id_producto
                )
            ).scalar_one_or_none()

            if not inventario:
                raise HTTPException(
                    status_code=400,
                    detail=f"El producto {producto.nombre} no tiene inventario"
                )

            # Validar existencias
            if inventario.stock_actual < item.cantidad:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Stock insuficiente para {producto.nombre}. "
                        f"Disponible: {inventario.stock_actual}"
                    )
                )

            # Guardar el precio actual del producto
            precio = producto.precio

            detalle = DetallePedido(
                id_pedido=nuevo_pedido.id_pedido,
                id_producto=producto.id_producto,
                cantidad=item.cantidad,
                precio_unitario=precio
            )

            db.add(detalle)

            # Descontar existencias
            inventario.stock_actual -= item.cantidad

            # Calcular el total
            total_pedido += precio * item.cantidad

        # Guardar el total final
        nuevo_pedido.total = total_pedido

        # Confirmar toda la operación
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
            detail="Ocurrió un error al registrar el pedido"
        )

@router.get("/")
def listar_pedidos(
    db: Session = Depends(get_db),
    administrador: Administrador = Depends(
        obtener_administrador_actual
    )
):
    resultado = db.execute(
        select(Pedido).order_by(
            Pedido.fecha_pedido.desc()
        )
    )

    return resultado.scalars().all()

@router.get("/{id_pedido}")
def obtener_pedido(
    id_pedido: int,
    db: Session = Depends(get_db),
    administrador: Administrador = Depends(
        obtener_administrador_actual
    )
):
    pedido = db.get(Pedido, id_pedido)

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="El pedido no existe"
        )

    resultado = db.execute(
        select(DetallePedido).where(
            DetallePedido.id_pedido == id_pedido
        )
    )

    detalles = resultado.scalars().all()

    return {
        "id_pedido": pedido.id_pedido,
        "nombre_cliente": pedido.nombre_cliente,
        "telefono": pedido.telefono,
        "direccion_entrega": pedido.direccion_entrega,
        "observaciones": pedido.observaciones,
        "estado": pedido.estado,
        "total": pedido.total,
        "fecha_pedido": pedido.fecha_pedido,
        "detalles": detalles
    }

@router.patch(
    "/{id_pedido}/estado",
    response_model=PedidoResponse
)
def actualizar_estado_pedido(
    id_pedido: int,
    datos: PedidoEstadoUpdate,
    db: Session = Depends(get_db),
    administrador: Administrador = Depends(obtener_administrador_actual)
):
    estados_validos = {
        "pendiente",
        "confirmado",
        "preparando",
        "enviado",
        "entregado",
        "cancelado"
    }

    if datos.estado not in estados_validos:
        raise HTTPException(
            status_code=400,
            detail="Estado de pedido no válido"
        )

    pedido = db.get(Pedido, id_pedido)

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="El pedido no existe"
        )

    pedido.estado = datos.estado

    db.commit()
    db.refresh(pedido)

    return pedido