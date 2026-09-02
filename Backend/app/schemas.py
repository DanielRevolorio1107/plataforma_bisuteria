from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator
)


class CategoriaCreate(BaseModel):
    nombre: str = Field(
        min_length=1
    )
    descripcion: str | None = None

    @field_validator('nombre')
    @classmethod
    def validar_nombre(
        cls,
        valor: str
    ) -> str:

        valor = valor.strip()

        if not valor:
            raise ValueError(
                'El nombre de la categoría es obligatorio'
            )

        return valor

    @field_validator('descripcion')
    @classmethod
    def limpiar_descripcion(
        cls,
        valor: str | None
    ) -> str | None:

        if valor is None:
            return None

        valor = valor.strip()

        return valor or None


class CategoriaResponse(BaseModel):
    id_categoria: int
    nombre: str
    descripcion: str | None
    activo: bool
    fecha_creacion: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class CategoriaUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None

    @field_validator('nombre')
    @classmethod
    def validar_nombre(
        cls,
        valor: str | None
    ) -> str | None:

        if valor is None:
            return None

        valor = valor.strip()

        if not valor:
            raise ValueError(
                'El nombre de la categoría no puede estar vacío'
            )

        return valor

    @field_validator('descripcion')
    @classmethod
    def limpiar_descripcion(
        cls,
        valor: str | None
    ) -> str | None:

        if valor is None:
            return None

        valor = valor.strip()

        return valor or None


class ProductoCreate(BaseModel):
    id_categoria: int = Field(
        gt=0
    )

    codigo: str = Field(
        min_length=1
    )

    nombre: str = Field(
        min_length=1
    )

    descripcion: str | None = None
    material: str | None = None
    color: str | None = None
    estilo: str | None = None

    precio: Decimal = Field(
        ge=0
    )

    imagen_url: str | None = None

    @field_validator(
        'codigo',
        'nombre'
    )
    @classmethod
    def validar_texto_obligatorio(
        cls,
        valor: str
    ) -> str:

        valor = valor.strip()

        if not valor:
            raise ValueError(
                'Este campo no puede estar vacío'
            )

        return valor

    @field_validator(
        'descripcion',
        'material',
        'color',
        'estilo',
        'imagen_url'
    )
    @classmethod
    def limpiar_textos_opcionales(
        cls,
        valor: str | None
    ) -> str | None:

        if valor is None:
            return None

        valor = valor.strip()

        return valor or None


class ProductoUpdate(BaseModel):
    id_categoria: int | None = Field(
        default=None,
        gt=0
    )

    codigo: str | None = None
    nombre: str | None = None
    descripcion: str | None = None
    material: str | None = None
    color: str | None = None
    estilo: str | None = None

    precio: Decimal | None = Field(
        default=None,
        ge=0
    )

    imagen_url: str | None = None

    @field_validator(
        'codigo',
        'nombre'
    )
    @classmethod
    def validar_texto_obligatorio(
        cls,
        valor: str | None
    ) -> str | None:

        if valor is None:
            return None

        valor = valor.strip()

        if not valor:
            raise ValueError(
                'Este campo no puede estar vacío'
            )

        return valor

    @field_validator(
        'descripcion',
        'material',
        'color',
        'estilo',
        'imagen_url'
    )
    @classmethod
    def limpiar_textos_opcionales(
        cls,
        valor: str | None
    ) -> str | None:

        if valor is None:
            return None

        valor = valor.strip()

        return valor or None


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

    model_config = ConfigDict(
        from_attributes=True
    )


class InventarioUpdate(BaseModel):
    stock_actual: int = Field(
        ge=0
    )

    stock_minimo: int = Field(
        ge=0
    )


class InventarioResponse(BaseModel):
    id_inventario: int
    id_producto: int
    stock_actual: int
    stock_minimo: int
    fecha_actualizacion: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class DetallePedidoCreate(BaseModel):
    id_producto: int = Field(
        gt=0
    )

    cantidad: int = Field(
        gt=0
    )


class PedidoCreate(BaseModel):

    nombre_cliente: str

    telefono: str

    direccion_entrega: str

    observaciones: str | None = None

    productos: list[
        DetallePedidoCreate
    ] = Field(
        min_length=1
    )

    @field_validator('nombre_cliente')
    @classmethod
    def validar_nombre(
        cls,
        valor: str
    ) -> str:

        valor = valor.strip()

        if len(valor) < 2:
            raise ValueError(
                'El nombre debe contener al menos 2 caracteres'
            )

        caracteres_permitidos = {
            '-',
            "'"
        }

        if not all(
            caracter.isalpha()
            or caracter.isspace()
            or caracter in caracteres_permitidos
            for caracter in valor
        ):
            raise ValueError(
                'El nombre contiene caracteres no permitidos'
            )

        return valor

    @field_validator('telefono')
    @classmethod
    def validar_telefono(
        cls,
        valor: str
    ) -> str:

        valor = valor.strip()

        if (
            len(valor) != 8
            or not valor.isascii()
            or not valor.isdigit()
        ):
            raise ValueError(
                'El teléfono debe contener exactamente 8 números'
            )

        return valor

    @field_validator('direccion_entrega')
    @classmethod
    def validar_direccion(
        cls,
        valor: str
    ) -> str:

        valor = valor.strip()

        if len(valor) < 5:
            raise ValueError(
                'La dirección debe contener al menos 5 caracteres'
            )

        return valor

    @field_validator('observaciones')
    @classmethod
    def limpiar_observaciones(
        cls,
        valor: str | None
    ) -> str | None:

        if valor is None:
            return None

        valor = valor.strip()

        return valor or None


class PedidoResponse(BaseModel):
    id_pedido: int
    nombre_cliente: str
    telefono: str
    direccion_entrega: str
    observaciones: str | None
    estado: str
    total: Decimal
    fecha_pedido: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class DetallePedidoResponse(BaseModel):
    id_detalle: int
    id_producto: int
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )


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

    model_config = ConfigDict(
        from_attributes=True
    )


class PedidoEstadoUpdate(BaseModel):
    estado: Literal[
        'pendiente',
        'confirmado',
        'preparando',
        'enviado',
        'entregado',
        'cancelado'
    ]


class AdministradorCreate(BaseModel):
    nombre: str = Field(
        min_length=1
    )

    usuario: str = Field(
        min_length=1
    )

    password: str = Field(
        min_length=8
    )

    @field_validator(
        'nombre',
        'usuario'
    )
    @classmethod
    def validar_campos(
        cls,
        valor: str
    ) -> str:

        valor = valor.strip()

        if not valor:
            raise ValueError(
                'Este campo no puede estar vacío'
            )

        return valor


class AdministradorResponse(BaseModel):
    id_administrador: int
    nombre: str
    usuario: str
    activo: bool
    fecha_creacion: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class LoginRequest(BaseModel):
    usuario: str = Field(
        min_length=1
    )

    password: str = Field(
        min_length=1
    )

    @field_validator('usuario')
    @classmethod
    def limpiar_usuario(
        cls,
        valor: str
    ) -> str:

        valor = valor.strip()

        if not valor:
            raise ValueError(
                'El usuario es obligatorio'
            )

        return valor


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class BusquedaResultado(BaseModel):
    producto: ProductoResponse
    similitud: float


class RecomendacionResultado(BaseModel):
    producto: ProductoResponse
    puntuacion: float