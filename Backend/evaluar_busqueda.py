from sqlalchemy import select

from app.database import SessionLocal
from app.models import Categoria, Producto
from app.busqueda import buscar_productos_semanticos


CONSULTAS = [
    "aretes plateados",
    "anillo rosa",
    "pulsera minimalista",
    "collar casual",
    "aretes para uso diario",
    "accesorio dorado para evento",
    "joya rosa para uso diario",
    "algo minimalista y plateado",
    "collar de acero",
    "regalo elegante dorado"
]


def ejecutar_evaluacion():

    db = SessionLocal()

    try:

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


        print()
        print(
            f"Productos activos evaluados: "
            f"{len(productos)}"
        )


        for numero, consulta in enumerate(
            CONSULTAS,
            start=1
        ):

            print()
            print("=" * 65)

            print(
                f"{numero}. Búsqueda: {consulta}"
            )

            print("=" * 65)


            resultados = buscar_productos_semanticos(
                consulta=consulta,
                productos=productos,
                categorias_por_producto=(
                    categorias_por_producto
                ),
                limite=5
            )


            if not resultados:

                print(
                    "No se encontraron resultados."
                )

                continue


            for posicion, (
                producto,
                puntuacion
            ) in enumerate(
                resultados,
                start=1
            ):

                categoria = (
                    categorias_por_producto.get(
                        producto.id_producto,
                        "Sin categoría"
                    )
                )


                print(
                    f"{posicion}. "
                    f"{producto.nombre}"
                )

                print(
                    f"   Categoría: {categoria}"
                )

                print(
                    f"   Material: {producto.material}"
                )

                print(
                    f"   Color: {producto.color}"
                )

                print(
                    f"   Estilo: {producto.estilo}"
                )

                print(
                    f"   Puntuación: "
                    f"{puntuacion:.2%}"
                )

                print()


    finally:

        db.close()


if __name__ == "__main__":
    ejecutar_evaluacion()