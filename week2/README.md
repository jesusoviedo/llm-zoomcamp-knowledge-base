# Semana 2 - LLM Zoomcamp

Este documento recopila mis apuntes y recursos para la **Semana 2** del curso LLM Zoomcamp.

## 📝 Notas de la teoría

### Busqueda Vectorial

La búsqueda vectorial permite encontrar objetos similares transformándolos en vectores de alta dimensión y comparándolos en función de su cercanía en ese espacio. Qdrant es una base de datos open‑source escrita en Rust, diseñada para realizar esa búsqueda de manera rápida y escalable

**Vectores**

En aprendizaje automático, un vector es una representación numérica de un objeto complejo (texto, imagen, usuario, etc.) en un espacio multidimensional. Si imaginas cada dato como una canción, el vector sería la partitura que resume su melodía semántica.

**Métricas de similitud**

Comparar vectores es medir distancias:
- Similitud del coseno: compara la orientación de dos vectores (ángulo).
- Distancia Euclidiana: mide la distancia “directa” en el espacio.
- Producto escalar: correlaciona vectores en función de su producto escalar.

**Búsqueda semántica y disimilitud**

- Búsqueda de similitud semántica: encuentra vectores cercanos al vector de consulta, como buscar estrellas de la misma constelación.
- Búsqueda por disimilitud: selecciona vectores lejanos, útil para detección de anomalías.

**Búsqueda de diversidad**

Algunos casos requieren variedad. Una manera sería filtrar resultados muy cercanos entre sí (“vecinos ruidosos”), garantizando que los resultados sean semánticamente distintos entre sí.


**Recomendaciones basadas en vectores**
* Recomendaciones de características vectoriales: almacenamos vectores de usuarios y productos. Luego, al comparar vectores similares, sugerimos ítems que están cerca en ese espacio.

* Recomendaciones de distancia relativa: no se trata solo de encontrar los más similares, sino de medir "lo suficientemente cerca" respecto al promedio, usando filtros dinámicos y normalización dentro del espacio vectorial.

**Descubrimiento**

Encuentros inesperados son posibles gracias a la diversidad vectorial: descubrir relaciones no evidentes entre documentos, temas o productos.

### Qdrant: Motor de Búsqueda Vectorial Semántica

Qdrant (Quadrant) es un **motor de base de datos vectorial de alto rendimiento** diseñado para búsquedas semánticas, recuperación de información por similitud y aplicaciones de inteligencia artificial. Está optimizado para manejar **incrustaciones vectoriales** generadas por modelos de machine learning y proporciona una API eficiente para realizar búsquedas de vecinos más cercanos (k-NN) de manera precisa, rápida y escalable.

Qdrant permite almacenar vectores densos (embeddings) junto con **metadatos** estructurados, habilitando búsquedas híbridas: **vectoriales** (por similitud semántica) y **filtradas** (por condiciones estructuradas). Es ideal para aplicaciones como:

- RAG (Retrieval-Augmented Generation)
- Recomendadores
- Motores de búsqueda semántica
- Chatbots con contexto vectorial

#### **Características Principales**

- Soporte de vectores de alta dimensión:
- Búsqueda aproximada y exacta (HNSW, Brute Force)
- Filtros por metadatos estructurados
- Indexación incremental y tiempo real
- Optimizado para CPU y disponible con soporte para GPU
- Integración con FastEmbed y frameworks de ML/IA
- Soporta múltiples colecciones y namespaces.
- API REST y gRPC.
- Persistencia en disco o en memoria.

#### **Arquitectura**

![alt text](./img/image.png)

- Motor de búsqueda HNSW (Hierarchical Navigable Small World): estructura de grafo eficiente para búsquedas vectoriales aproximadas.
- Gestión de Payloads: cada vector puede tener metadatos adjuntos para filtrado semántico estructurado.
- Shard Manager: cuando se usa en clúster, balancea y distribuye datos entre nodos.

#### **Almacenamiento de Datos: Colecciones y Puntos**

Qdrant organiza los datos en **colecciones**, similares a las tablas en una base de datos relacional. Cada colección agrupa un conjunto de vectores y su información asociada.

![alt text](./img/image_2.png)

*Colección*

Una colección representa un espacio de búsqueda aislado con su propio índice, configuración y datos. Puedes tener múltiples colecciones, por ejemplo: `faq_articles`, `legal_docs` y `product_catalog`

Cada colección define:

- El tamaño de los vectores (dimensionalidad)
- La métrica de similitud (`Cosine`, `Euclidean`, `Dot`)
- Opcionalmente, si usa HNSW u otro tipo de indexado

*Punto*

Los datos dentro de una colección se almacenan como puntos (PointStruct). Cada punto es un objeto que representa un vector en el espacio semántico y contiene:
- `id`: identificador único del punto (entero o UUID)
- `vector`: array de floats (el embedding)
- `payload`: diccionario de metadatos JSON asociados al vector

Este diseño permite, realizar búsquedas vectoriales por similitud sobre `vector` y filtrar por metadatos estructurados contenidos en `payload`

Los `puntos` se pueden insertar individualmente o por lotes (`batch upsert`) usando la API o el cliente oficial (`qdrant-client` para Python).

*Indexación*

Una vez insertados, los puntos pueden ser indexados automáticamente por el motor HNSW (si está habilitado) o buscados mediante fuerza bruta (Brute Force) si no hay índice disponible. Los índices permiten acelerar la búsqueda de vectores similares sin recorrer todos los datos.

#### **Funcionalidades Clave**

- `search`: buscar por similitud vectorial.
- `recommend`: sugerencias basadas en vectores positivos y negativos.
- `scroll`: recuperación paginada.
- `filter`: búsquedas filtradas por metadatos (ej. categoría, fecha).
- `payload`: adjuntar información extra (JSON) a los vectores.
- `update/delete`: modificaciones en tiempo real.
- `collections`: múltiples espacios de trabajo aislados.
- `snapshots/backups`: gestión de respaldo y restauración.

#### **Seguridad**

- Autenticación basada en tokens (a partir de la versión 1.5).
- Control de acceso a endpoints vía configuración de API keys.
- Comunicaciones seguras mediante TLS (cuando se usa proxy o configuración externa).
- Integrable con firewalls, proxies y servicios de autenticación externos.

#### **Alta Disponibilidad y Redundancia**

- Modo Clúster (Enterprise o Community):
    - Distribución horizontal de shards en múltiples nodos.
    - Replicación de shards para tolerancia a fallos.
    - Rebalanceo automático ante cambios de topología.
- Backups y snapshots periódicos para recuperación de desastres.
- Qdrant Cloud ofrece despliegue gestionado con SLA, HA y escalado automático.

### 🛠️ Ejemplo práctico de Qdrant

**Creación de un entorno de desarrollo**

Para crear y gestionar el entorno de Python de este proyecto se utiliza `uv`, una herramienta moderna que combina la gestión de entornos virtuales y la resolución de dependencias de forma rápida y eficiente.

Este enfoque reemplaza el uso tradicional de herramientas como `venv`, `pip` y `virtualenv`, ofreciendo una experiencia más simple y ágil.

ℹ️ Para más detalles sobre cómo instalar y utilizar uv, consulta el archivo [`working-with-uv.md`](../docs/working-with-uv.md)

Una vez instalado `uv`, puedes crear el entorno virtual e instalar todas las dependencias necesarias con un solo comando:

```bash
uv venv && uv sync
```

Este comando creará un entorno virtual en el directorio del proyecto y sincronizará las librerías especificadas en el archivo `pyproject.toml`.

**Interactuando con Qdrant usando Python**

**1. Descargar la imagen de Qdrant desde Docker Hub**

```bash
docker pull qdrant/qdrant
```

**2. Ejecutar el servicio**

```bash
docker run -p 6333:6333 -p 6334:6334 \
    -v "$(pwd)/qdrant_storage:/qdrant/storage:z" \
    qdrant/qdrant
```

Con esta configuración predeterminada, todos los datos se almacenarán en el directorio  `./qdrant_storage`, el cual será accesible tanto para el contenedor como para el host.

Qdrant ahora estará disponible en:
- API REST: http://localhost:6333
- Interfaz web: http://localhost:6333/dashboard
- API gRPC: http://localhost:6334

**3. Flujo básico**

Si deseas ver un ejemplo práctico de cómo crear una colección, agregar elementos y realizar una consulta, puedes consultar el archivo [`0_quickstart`](./notebook/0_quickstart.ipynb).

Este notebook incluye ejemplos de:
- Creación de un cliente.
- Creación de una colección.
- Inserción de puntos/vectores en una colección.
- Recuperación de los puntos/vectores más cercanos.
- Aplicación de filtros en las búsquedas.



**4. Código Python que muestra cómo usar un LLM en conjunto con Qdrant**

Si querés ver un ejemplo práctico de cómo implementar RAG (Retrieval-Augmented Generation) utilizando OpenAI o Gemini y una base de conocimiento local, podés consultar el archivo [`llm_api_examples_gemini_openai`](./notebook/llm_api_examples_gemini_openai.ipynb)

Este notebook incluye ejemplos de cómo:
- Hacer una consulta simple a un modelo LLM (como GPT o Gemini).
- Conectar ese modelo a una fuente externa de datos (como un documento o colección de texto).
- Combinar recuperación de información y generación de texto para responder preguntas con base en conocimiento personalizado.

## 🔗 Lectura recomendada
Recomendado para profundizar en los conceptos clave y ampliar tu comprensión
* [What is Qdrant?](https://qdrant.tech/documentation/overview/)
* [How Does Vector Search Work in Qdrant?](https://qdrant.tech/documentation/overview/vector-search/)
* [How to Get Started with Qdrant Locally](https://qdrant.tech/documentation/quickstart/)
* [Qdrant Web UI](https://qdrant.tech/documentation/web-ui/)
* [How to Generate Text Embedings with FastEmbed](https://qdrant.tech/documentation/fastembed/fastembed-quickstart/)
* [Using FastEmbed with Qdrant for Vector Search](https://qdrant.tech/documentation/fastembed/fastembed-semantic-search/)
* [Qdrant - Concepts](https://qdrant.tech/documentation/concepts/)
* [Estrellas en el cielo semántico: búsqueda vectorial con Qdrant](https://medium.com/@j92riquelme/estrellas-en-el-cielo-semántico-búsqueda-vectorial-con-qdrant-89072b49f418)
* [An Introduction to Vector Databases](https://qdrant.tech/articles/what-is-a-vector-database/)
* [Build Your First Semantic Search Engine](https://qdrant.tech/documentation/beginner-tutorials/search-beginners/)
* [A Complete Guide to Filtering in Vector Search](https://qdrant.tech/articles/vector-search-filtering/)


## 🔗 Videos recomendados
Selección de videos para reforzar visualmente los temas abordados
* [What is RAG? Building Better LLM Systems with Qdrant](https://www.youtube.com/watch?v=rtIyQPJUd_U)
* [How Vector Search Algorithms Work: An Intro to Qdrant](https://www.youtube.com/watch?v=mXNrhyw4q84)
* [Exploring Qdrant concepts - Collections](https://www.youtube.com/watch?v=0sg7pJo0siU)
* [Qdrant Tutorial - Semantic Search for Beginners](https://www.youtube.com/watch?v=AASiqmtKo54)
* [Getting Started with Qdrant](https://youtu.be/LRcZ9pbGnno?si=0xPf3C9oGpR6BxRz)
* [Chatbot with RAG, using LangChain, OpenAI, and Groq](https://www.youtube.com/watch?v=O60-KuZZeQA)
* [Music Recommendation System with Qdrant Vector Search and Audio Embeddings](https://www.youtube.com/watch?v=id5ql-Abq4Y)


## Cursos adicionales recomendados
Recursos complementarios para seguir aprendiendo y fortaleciendo tus habilidades.

* [Retrieval Optimization: From Tokenization to Vector Quantization](https://www.deeplearning.ai/short-courses/retrieval-optimization-from-tokenization-to-vector-quantization/?utm_campaign=qdrant-launch&utm_medium=qdrant&utm_source=partner-promo)

---

> 📌 **Nota:** este repositorio complementa el curso **LLM Zoomcamp** de [DataTalks.Club](https://datatalks.club/), y contiene notas, lecturas, videos, ejemplos y recursos adicionales.  
> Para acceder al contenido oficial del curso, visita el [**repositorio principal en GitHub**](https://github.com/DataTalksClub/llm-zoomcamp).
