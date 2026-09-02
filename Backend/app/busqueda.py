from threading import Lock

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


modelo = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


UMBRAL_SIMILITUD = 0.35


cache_embeddings = {}

cache_lock = Lock()


def crear_texto_producto(producto) -> str:

    campos = [
        producto.nombre,
        producto.descripcion,
        producto.material,
        producto.color,
        producto.estilo
    ]

    campos_validos = [
        str(campo).strip()
        for campo in campos
        if campo
    ]

    return " ".join(campos_validos)


def obtener_vectores_productos(
    productos: list
):

    textos_productos = [
        crear_texto_producto(producto)
        for producto in productos
    ]

    ids_actuales = {
        producto.id_producto
        for producto in productos
    }

    with cache_lock:

        ids_cache = list(
            cache_embeddings.keys()
        )

        for id_producto in ids_cache:

            if id_producto not in ids_actuales:
                del cache_embeddings[
                    id_producto
                ]

        productos_por_calcular = []
        textos_por_calcular = []

        for producto, texto in zip(
            productos,
            textos_productos
        ):

            guardado = cache_embeddings.get(
                producto.id_producto
            )

            if (
                guardado is None
                or guardado["texto"] != texto
            ):

                productos_por_calcular.append(
                    producto
                )

                textos_por_calcular.append(
                    texto
                )

        if textos_por_calcular:

            nuevos_vectores = modelo.encode(
                textos_por_calcular
            )

            for producto, texto, vector in zip(
                productos_por_calcular,
                textos_por_calcular,
                nuevos_vectores
            ):

                cache_embeddings[
                    producto.id_producto
                ] = {
                    "texto": texto,
                    "vector": vector
                }

        vectores_productos = [
            cache_embeddings[
                producto.id_producto
            ]["vector"]
            for producto in productos
        ]

    return vectores_productos


def buscar_productos_semanticos(
    consulta: str,
    productos: list,
    limite: int = 5
):

    consulta = consulta.strip()

    if not consulta or not productos:
        return []

    vectores_productos = (
        obtener_vectores_productos(
            productos
        )
    )

    vector_consulta = modelo.encode(
        [consulta]
    )

    similitudes = cosine_similarity(
        vector_consulta,
        vectores_productos
    )[0]

    resultados = list(
        zip(
            productos,
            similitudes
        )
    )

    resultados.sort(
        key=lambda resultado:
            resultado[1],
        reverse=True
    )

    resultados_relevantes = [
        resultado
        for resultado in resultados
        if resultado[1] >= UMBRAL_SIMILITUD
    ]

    return resultados_relevantes[
        :limite
    ]