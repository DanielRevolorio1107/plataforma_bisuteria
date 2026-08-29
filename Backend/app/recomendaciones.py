def calcular_similitud_producto(
    producto_base,
    producto_candidato
) -> float:

    puntuacion = 0.0


    # Misma categoría
    if (
        producto_base.id_categoria ==
        producto_candidato.id_categoria
    ):
        puntuacion += 0.30


    # Mismo material
    if (
        producto_base.material and
        producto_candidato.material and
        producto_base.material.lower() ==
        producto_candidato.material.lower()
    ):
        puntuacion += 0.20


    # Mismo color
    if (
        producto_base.color and
        producto_candidato.color and
        producto_base.color.lower() ==
        producto_candidato.color.lower()
    ):
        puntuacion += 0.20


    # Mismo estilo
    if (
        producto_base.estilo and
        producto_candidato.estilo and
        producto_base.estilo.lower() ==
        producto_candidato.estilo.lower()
    ):
        puntuacion += 0.20


    # Precio parecido
    precio_base = float(
        producto_base.precio
    )

    precio_candidato = float(
        producto_candidato.precio
    )


    precio_mayor = max(
        precio_base,
        precio_candidato,
        1
    )


    diferencia = abs(
        precio_base - precio_candidato
    )


    similitud_precio = (
        1 - diferencia / precio_mayor
    )


    puntuacion += (
        max(similitud_precio, 0) * 0.10
    )


    return puntuacion


def recomendar_productos(
    producto_base,
    productos,
    limite: int = 4
):

    resultados = []


    for producto in productos:

        # No recomendar el mismo producto
        if (
            producto.id_producto ==
            producto_base.id_producto
        ):
            continue


        puntuacion = calcular_similitud_producto(
            producto_base,
            producto
        )


        resultados.append(
            (producto, puntuacion)
        )


    # Ordenar de mayor a menor puntuación
    resultados.sort(
        key=lambda resultado: resultado[1],
        reverse=True
    )


    # Solo dejar recomendaciones relevantes
    resultados_relevantes = [
        resultado
        for resultado in resultados
        if resultado[1] >= 0.35
    ]


    return resultados_relevantes[:limite]