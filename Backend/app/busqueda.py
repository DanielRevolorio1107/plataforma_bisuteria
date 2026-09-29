import re
import unicodedata
from threading import Lock

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


modelo = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


UMBRAL_SIMILITUD = 0.35


cache_embeddings = {}

cache_lock = Lock()


def normalizar_texto(
    texto: str
) -> str:

    texto = texto.lower().strip()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

    return texto


def obtener_tokens(
    texto: str
) -> list[str]:

    texto = normalizar_texto(
        texto
    )

    tokens = re.findall(
        r"[a-z0-9]+",
        texto
    )

    palabras_vacias = {
        "de",
        "del",
        "la",
        "el",
        "los",
        "las",
        "un",
        "una",
        "unos",
        "unas",
        "para",
        "con",
        "y",
        "o",
        "en"
    }

    return [
        token
        for token in tokens
        if token not in palabras_vacias
    ]


def obtener_raiz_genero(
    token: str
) -> str:

    if (
        len(token) >= 6
        and token.endswith(
            ("os", "as")
        )
    ):
        return token[:-2]

    if (
        len(token) >= 6
        and token.endswith(
            ("o", "a")
        )
    ):
        return token[:-1]

    return token


def tokens_coinciden(
    token_consulta: str,
    token_valor: str
) -> bool:

    if token_consulta == token_valor:
        return True

    if (
        len(token_consulta) >= 4
        and len(token_valor) >= 4
    ):

        if (
            token_valor.startswith(
                token_consulta
            )
            or token_consulta.startswith(
                token_valor
            )
        ):
            return True

    raiz_consulta = obtener_raiz_genero(
        token_consulta
    )

    raiz_valor = obtener_raiz_genero(
        token_valor
    )

    if (
        raiz_consulta == raiz_valor
        and len(raiz_consulta) >= 4
    ):
        return True

    return False


def valor_aparece_en_consulta(
    consulta: str,
    valor: str | None
) -> bool:

    if not valor:
        return False

    tokens_consulta = obtener_tokens(
        consulta
    )

    tokens_valor = obtener_tokens(
        str(valor)
    )

    if (
        not tokens_consulta
        or not tokens_valor
    ):
        return False

    for token_consulta in tokens_consulta:

        for token_valor in tokens_valor:

            if tokens_coinciden(
                token_consulta,
                token_valor
            ):
                return True

    return False


def crear_texto_producto(
    producto,
    nombre_categoria: str | None = None
) -> str:

    campos = [
        producto.nombre,
        nombre_categoria,
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

    return " ".join(
        campos_validos
    )


def obtener_valores_unicos(
    productos: list,
    atributo: str
) -> list[str]:

    valores = {
        str(valor).strip()
        for producto in productos
        if (
            valor := getattr(
                producto,
                atributo,
                None
            )
        )
    }

    return list(valores)


def detectar_filtros(
    consulta: str,
    productos: list,
    categorias_por_producto: dict[int, str]
) -> dict[str, list[str]]:

    categorias = list(
        set(
            categorias_por_producto.values()
        )
    )

    colores = obtener_valores_unicos(
        productos,
        "color"
    )

    estilos = obtener_valores_unicos(
        productos,
        "estilo"
    )

    materiales = obtener_valores_unicos(
        productos,
        "material"
    )

    categorias_detectadas = [
        categoria
        for categoria in categorias
        if valor_aparece_en_consulta(
            consulta,
            categoria
        )
    ]

    colores_detectados = [
        color
        for color in colores
        if valor_aparece_en_consulta(
            consulta,
            color
        )
    ]

    estilos_detectados = [
        estilo
        for estilo in estilos
        if valor_aparece_en_consulta(
            consulta,
            estilo
        )
    ]

    materiales_detectados = [
        material
        for material in materiales
        if valor_aparece_en_consulta(
            consulta,
            material
        )
    ]

    return {
        "categorias":
            categorias_detectadas,

        "colores":
            colores_detectados,

        "estilos":
            estilos_detectados,

        "materiales":
            materiales_detectados
    }


def valor_esta_en_lista(
    valor: str | None,
    valores: list[str]
) -> bool:

    if not valor:
        return False

    valor_normalizado = normalizar_texto(
        str(valor)
    )

    return any(
        valor_normalizado
        == normalizar_texto(item)
        for item in valores
    )


def filtrar_productos(
    productos: list,
    categorias_por_producto: dict[int, str],
    filtros: dict[str, list[str]]
) -> list:

    productos_filtrados = []

    for producto in productos:

        categoria = (
            categorias_por_producto.get(
                producto.id_producto
            )
        )

        if (
            filtros["categorias"]
            and not valor_esta_en_lista(
                categoria,
                filtros["categorias"]
            )
        ):
            continue

        if (
            filtros["colores"]
            and not valor_esta_en_lista(
                producto.color,
                filtros["colores"]
            )
        ):
            continue

        if (
            filtros["estilos"]
            and not valor_esta_en_lista(
                producto.estilo,
                filtros["estilos"]
            )
        ):
            continue

        if (
            filtros["materiales"]
            and not valor_esta_en_lista(
                producto.material,
                filtros["materiales"]
            )
        ):
            continue

        productos_filtrados.append(
            producto
        )

    return productos_filtrados


def obtener_vectores_productos(
    productos: list,
    categorias_por_producto: dict[int, str]
):

    textos_productos = [
        crear_texto_producto(
            producto,
            categorias_por_producto.get(
                producto.id_producto
            )
        )
        for producto in productos
    ]

    with cache_lock:

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
    categorias_por_producto: dict[int, str],
    limite: int = 5
):

    consulta = consulta.strip()

    if not consulta or not productos:
        return []

    filtros = detectar_filtros(
        consulta,
        productos,
        categorias_por_producto
    )

    hay_filtros = any(
        filtros.values()
    )

    productos_candidatos = (
        filtrar_productos(
            productos,
            categorias_por_producto,
            filtros
        )
    )

    if not productos_candidatos:
        return []

    vectores_productos = (
        obtener_vectores_productos(
            productos_candidatos,
            categorias_por_producto
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
            productos_candidatos,
            similitudes
        )
    )

    resultados.sort(
        key=lambda resultado:
            resultado[1],
        reverse=True
    )

    if hay_filtros:

        return resultados[
            :limite
        ]

    resultados_relevantes = [
        resultado
        for resultado in resultados
        if resultado[1]
        >= UMBRAL_SIMILITUD
    ]

    return resultados_relevantes[
        :limite
    ]