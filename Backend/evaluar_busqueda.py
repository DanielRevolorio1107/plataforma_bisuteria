from sqlalchemy import select

from app.database import SessionLocal
from app.models import Categoria, Producto
from app.busqueda import buscar_productos_semanticos


CONSULTAS = [
    "anillo elegante",
    "pulsera dorada",
    "collar plateado",
    "accesorio para regalo",
    "bisutería elegante",
    "pulsera casual",
    "collar dorado",
    "anillo plateado",
    "accesorio elegante",
    "joyería para ocasión especial"
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


        for numero, consulta in enumerate(
            CONSULTAS,
            start=1
        ):

            print()
            print("=" * 60)

            print(
                f"{numero}. Búsqueda: {consulta}"
            )

            print("=" * 60)


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
                similitud
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
                    f"   Material: "
                    f"{producto.material}"
                )

                print(
                    f"   Color: "
                    f"{producto.color}"
                )

                print(
                    f"   Estilo: "
                    f"{producto.estilo}"
                )

                print(
                    f"   Similitud: "
                    f"{similitud:.2%}"
                )

                print()


    finally:

        db.close()


if __name__ == "__main__":
    ejecutar_evaluacion()