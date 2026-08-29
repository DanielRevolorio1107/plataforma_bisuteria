
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: str | None = None


class CategoriaResponse(BaseModel):
    id_categoria: int
    nombre: str
    descripcion: str | None
    activo: bool
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductoCreate(BaseModel):
    id_categoria: int
    codigo: str
    nombre: str
    descripcion: str | None = None
    material: str | None = None
    color: str | None = None
    estilo: str | None = None
    precio: Decimal
    imagen_url: str | None = None

class ProductoUpdate(BaseModel):
    id_categoria: int | None = None
    codigo: str | None = None
    nombre: str | None = None
    descripcion: str | None = None
    material: str | None = None
    color: str | None = None
    estilo: str | None = None
    precio: Decimal | None = None
    imagen_url: str | None = None

class ProductoResponse(BaseModel):
    id_producto: int
    id_categoria: int
    codigo: str
    nombre: str
    descripcion: str | None
    material: str | None
    color: str | None
    estilo: str | None
    precio: Decimal
    imagen_url: str | None
    activo: bool
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)    

class InventarioUpdate(BaseModel):
    stock_actual: int
    stock_minimo: int


class InventarioResponse(BaseModel):
    id_inventario: int
    id_producto: int
    stock_actual: int
    stock_minimo: int
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)

class DetallePedidoCreate(BaseModel):
    id_producto: int
    cantidad: int = Field(gt=0)


class PedidoCreate(BaseModel):
    nombre_cliente: str
    telefono: str
    direccion_entrega: str
    observaciones: str | None = None
    productos: list[DetallePedidoCreate]


class PedidoResponse(BaseModel):
    id_pedido: int
    nombre_cliente: str
    telefono: str
    direccion_entrega: str
    observaciones: str | None
    estado: str
    total: Decimal
    fecha_pedido: datetime

    model_config = ConfigDict(from_attributes=True)

class DetallePedidoResponse(BaseModel):
    id_detalle: int
    id_producto: int
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal

    model_config = ConfigDict(from_attributes=True)

class PedidoDetalleResponse(BaseModel):
    id_pedido: int
    nombre_cliente: str
    telefono: str
    direccion_entrega: str
    observaciones: str | None
    estado: str
    total: Decimal
    fecha_pedido: datetime
    detalles: list[DetallePedidoResponse]

class PedidoEstadoUpdate(BaseModel):
    estado: str

class AdministradorCreate(BaseModel):
    nombre: str
    usuario: str
    password: str = Field(min_length=8)


class AdministradorResponse(BaseModel):
    id_administrador: int
    nombre: str
    usuario: str
    activo: bool
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    usuario: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class CategoriaUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None

class BusquedaResultado(BaseModel):
    producto: ProductoResponse
    similitud: float

class RecomendacionResultado(BaseModel):
    producto: ProductoResponse
    puntuacion: float