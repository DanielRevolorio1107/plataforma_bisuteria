from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Modelo multilingüe que entiende español.
modelo = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


def crear_texto_producto(producto) -> str:
    """
    Une la información importante de un producto
    en un solo texto para poder compararlo.
    """

    campos = [
        producto.nombre,
        producto.descripcion,
        producto.material,
        producto.color,
        producto.estilo
    ]

    campos_validos = [
        str(campo)
        for campo in campos
        if campo
    ]

    return " ".join(campos_validos)


def buscar_productos_semanticos(
    consulta: str,
    productos: list,
    limite: int = 5
):
    """
    Compara la búsqueda del cliente con los productos
    y devuelve los productos más relacionados.
    """

    consulta = consulta.strip()

    if not consulta or not productos:
        return []


    textos_productos = [
        crear_texto_producto(producto)
        for producto in productos
    ]


    vectores_productos = modelo.encode(
        textos_productos
    )

    vector_consulta = modelo.encode(
        [consulta]
    )


    similitudes = cosine_similarity(
        vector_consulta,
        vectores_productos
    )[0]


    resultados = list(
        zip(productos, similitudes)
    )


    resultados.sort(
        key=lambda resultado: resultado[1],
        reverse=True
    )


    resultados_relevantes = [
        resultado
        for resultado in resultados
        if resultado[1] >= 0.35
    ]


    return resultados_relevantes[:limite]