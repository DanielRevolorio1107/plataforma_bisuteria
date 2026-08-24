from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func
)
from sqlalchemy import (
    Boolean,
    Computed,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func
)

class Categoria(Base):
    __tablename__ = "categorias"

    id_categoria: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    descripcion: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
    DateTime,
    nullable=False,
    server_default=func.now()
    )

class Producto(Base):
    __tablename__ = "productos"

    id_producto: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_categoria: Mapped[int] = mapped_column(
        ForeignKey("categorias.id_categoria"),
        nullable=False
    )

    codigo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    descripcion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    material: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    color: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    estilo: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    precio: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    imagen_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )
class Inventario(Base):
    __tablename__ = "inventario"

    id_inventario: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_producto: Mapped[int] = mapped_column(
        ForeignKey("productos.id_producto", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    stock_actual: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    stock_minimo: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )   
class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre_cliente: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    telefono: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    direccion_entrega: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    observaciones: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    estado: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="pendiente"
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=0
    )

    fecha_pedido: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )


class DetallePedido(Base):
    __tablename__ = "detalle_pedido"

    id_detalle: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    id_pedido: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id_pedido", ondelete="CASCADE"),
        nullable=False
    )

    id_producto: Mapped[int] = mapped_column(
        ForeignKey("productos.id_producto"),
        nullable=False
    )

    cantidad: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    precio_unitario: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        Computed("cantidad * precio_unitario")
    )

class Administrador(Base):
    __tablename__ = "administradores"

    id_administrador: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    usuario: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )