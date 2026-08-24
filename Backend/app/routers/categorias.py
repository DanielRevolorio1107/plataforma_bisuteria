from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Categoria, Administrador
from app.schemas import (
    CategoriaCreate,
    CategoriaResponse,
    CategoriaUpdate
)
from app.security import obtener_administrador_actual


router = APIRouter(
    prefix="/categorias",
    tags=["Categorías"]
)


@router.get(
    "/",
    response_model=list[CategoriaResponse]
)
def listar_categorias(
    db: Session = Depends(get_db)
):
    resultado = db.execute(
        select(Categoria)
        .where(Categoria.activo == True)
        .order_by(Categoria.id_categoria)
    )

    return resultado.scalars().all()


@router.get(
    "/admin/todas",
    response_model=list[CategoriaResponse]
)
def listar_categorias_admin(
    db: Session = Depends(get_db),
    admin: Administrador = Depends(obtener_administrador_actual)
):
    resultado = db.execute(
        select(Categoria).order_by(Categoria.id_categoria)
    )

    return resultado.scalars().all()


@router.post(
    "/",
    response_model=CategoriaResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_categoria(
    categoria: CategoriaCreate,
    db: Session = Depends(get_db),
    admin: Administrador = Depends(obtener_administrador_actual)
):
    existente = db.execute(
        select(Categoria).where(
            Categoria.nombre == categoria.nombre
        )
    ).scalar_one_or_none()

    if existente:
        raise HTTPException(
            status_code=409,
            detail="Ya existe una categoría con ese nombre"
        )

    nueva_categoria = Categoria(
        nombre=categoria.nombre,
        descripcion=categoria.descripcion
    )

    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)

    return nueva_categoria


@router.patch(
    "/{id_categoria}/activar",
    response_model=CategoriaResponse
)
def activar_categoria(
    id_categoria: int,
    db: Session = Depends(get_db),
    admin: Administrador = Depends(obtener_administrador_actual)
):
    categoria = db.get(Categoria, id_categoria)

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="La categoría no existe"
        )

    categoria.activo = True

    db.commit()
    db.refresh(categoria)

    return categoria


@router.patch(
    "/{id_categoria}",
    response_model=CategoriaResponse
)
def actualizar_categoria(
    id_categoria: int,
    datos: CategoriaUpdate,
    db: Session = Depends(get_db),
    admin: Administrador = Depends(obtener_administrador_actual)
):
    categoria = db.get(Categoria, id_categoria)

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="La categoría no existe"
        )

    cambios = datos.model_dump(exclude_unset=True)

    if "nombre" in cambios:
        existente = db.execute(
            select(Categoria).where(
                Categoria.nombre == cambios["nombre"],
                Categoria.id_categoria != id_categoria
            )
        ).scalar_one_or_none()

        if existente:
            raise HTTPException(
                status_code=409,
                detail="Ya existe una categoría con ese nombre"
            )

    for campo, valor in cambios.items():
        setattr(categoria, campo, valor)

    db.commit()
    db.refresh(categoria)

    return categoria


@router.delete(
    "/{id_categoria}",
    response_model=CategoriaResponse
)
def desactivar_categoria(
    id_categoria: int,
    db: Session = Depends(get_db),
    admin: Administrador = Depends(obtener_administrador_actual)
):
    categoria = db.get(Categoria, id_categoria)

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="La categoría no existe"
        )

    categoria.activo = False

    db.commit()
    db.refresh(categoria)

    return categoria