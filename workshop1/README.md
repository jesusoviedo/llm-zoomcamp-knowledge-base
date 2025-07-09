# Workshop 1 - De REST al razonamiento con DLT y Cognee

Este documento recopila mis apuntes y recursos para la **Workshop 1** del curso LLM Zoomcamp.

## 📚 Recursos del Workshop

- **Video del Workshop**: [Ver en YouTube](https://www.youtube.com/watch?v=MNt_KK32gys)
- **Diapositivas utilizadas**: [Ver en Google Slides](https://docs.google.com/presentation/d/1oHQilxEVqGGW4S2ctNEE0wHY2LgcjYLaRUziAoinsis/edit?usp=sharing)
- **Notebook en Google Colab**: [Abrir en Colab](https://colab.research.google.com/drive/1vBA9OIGChcKjjg8r5hHduR0v3A5D6rmH?usp=sharing#scrollTo=ZU45VaNNG970)

## 📝 Notas de la teoría

### ¿Qué es dlt?

**dlt (data load tool)** es una biblioteca de Python de código abierto, declarativa y centrada en el desarrollador, diseñada para **simplificar y automatizar la creación de pipelines de datos**. Su filosofía se basa en la convención sobre configuración, permitiendo enfocarse en el *qué* y no en el *cómo*.

#### **Principales ventajas**

- Inferencia automática de esquemas y su evolución
- Carga incremental sin configuración adicional
- Mínima configuración y sin necesidad de backend
- Ejecutable en notebooks, scripts, AWS Lambda, Airflow y más
- Compatible con múltiples fuentes y destinos de datos


#### **Proceso dlt: ETL Automatizado**

1. Extract

- Conectores listos para usar (APIs REST, bases SQL, almacenamiento en la nube, estructuras Python)
- Gestión automática de paginación, autenticación y control de flujo

2. Transform and Normalize

- Limpieza y normalización automática de datos semi-estructurados (como JSON)
- Inferencia y evolución de esquemas sin intervención manual
- Generación automática de tablas secundarias y relaciones

3. Load

- Carga eficiente y en lote hacia destinos como:
  - DuckDB, BigQuery, Snowflake, Redshift, Databricks y más
- Optimizaciones para grandes volúmenes de datos


#### **¿Qué ocurre al ejecutar `pipeline.run()`?**

1. Gestión de Estado

- Registra ejecuciones anteriores, versiones de esquema, archivos procesados y progresos (ej. timestamps)
- Estado persistente almacenado en el destino, asegurando continuidad y tolerancia a fallos

2. Carga Incremental

- Solo se cargan los datos nuevos o modificados desde la última ejecución
- Reducción significativa en tiempo, costos y consumo de APIs

3. Escalabilidad y Paralelización

- Procesamiento por fragmentos (chunks) sin saturar la memoria
- Creación implícita de un DAG de extracción
- Ejecución en paralelo de tareas independientes

### ¿Qué es Retrieval-Augmented Generation (RAG)?

**RAG** es un enfoque que combina modelos de lenguaje (LLMs) con bases de conocimiento externas, permitiéndoles consultar datos dinámicamente en tiempo real.

#### **Objetivos de RAG**:

- **Reducir alucinaciones**: Respuestas basadas en hechos verificables.
- **Incluir conocimiento actualizado y específico del dominio**.
- **Aumentar la transparencia**: Capacidad de citar fuentes utilizadas.

#### **Flujo Offline: Preparación del Conocimiento**

Proceso previo a recibir preguntas de usuarios. Se construye una base de datos vectorial a partir de documentos crudos.

Etapas:
1. **Load** – Se usan *Document Loaders* para cargar documentos desde PDFs, webs, bases de datos, etc.
2. **Split** – Los documentos se dividen en *chunks* pequeños para ajustarse al contexto limitado del LLM.
3. **Embed** – Cada chunk se convierte en un vector usando modelos de embeddings (OpenAI, Cohere, etc.).
4. **Store** – Los vectores y su texto original se almacenan en bases vectoriales como Qdrant o ChromaDB.

#### **Flujo Online: Generación en Tiempo Real**

Se activa cuando un usuario realiza una pregunta. Se recupera información relevante y se genera una respuesta fundamentada.

Etapas:
1. **Retrieve** – La pregunta se vectoriza y se buscan los chunks más cercanos en la base vectorial.
2. **Augment** – Se crea un *prompt aumentado* que incluye la pregunta y los chunks recuperados.
3. **Generate** – El LLM responde usando este prompt enriquecido con contexto fáctico.

#### **Limitación: Compresión con Pérdidas**

El paso de *chunking* puede romper la coherencia entre conceptos relacionados distribuidos en distintas partes del documento.

Ejemplo de Problema:

- Un concepto clave (Término A) aparece en la página 1.
- Su aplicación (Ejemplo B) aparece en la página 10.
- RAG puede recuperar solo uno de los dos chunks, generando respuestas incompletas.

### ¿Qué es Cognee?

**Cognee** es un framework de código abierto para agentes de IA que va más allá de la búsqueda por similitud. Su objetivo es construir una **memoria semántica evolutiva**, modelando activamente las relaciones entre conceptos mediante grafos de conocimiento y pipelines de datos automatizados.

#### **Pipeline ECL: Extract, Cognify, Load**

Una nueva alternativa al clásico ETL y al flujo de RAG.

1. Extract

- Ingesta de múltiples fuentes (documentos, bases de datos, transcripciones).
- Utiliza frameworks como `dlt` para conectar más de 28 tipos de fuentes.

2. Cognify

- Paso clave del framework.
- Construye una representación dual:
  - **Grafo de conocimiento** (con nodos y relaciones)
  - **Índice vectorial** para búsqueda semántica
- Detecta entidades, relaciones y dependencias.
- Transforma documentos en mapas conceptuales interactivos.

3. Load

- Persistencia flexible en:
  - Bases de datos vectoriales (Qdrant, Weaviate, etc.)
  - Bases de datos gráficas (Neo4j, NetworkX, etc.)

#### **Ventajas Clave de Cognee**

- **Contexto relacional profundo**: Recupera subgrafos completos, no solo chunks aislados.
- **Razonamiento real**: Permite inferencias lógicas sobre la estructura del conocimiento.
- **Ontologías personalizadas**: Define esquemas semánticos específicos del dominio.
- **Control y privacidad**: Desplegable 100% on-premise.

#### **Casos de Uso**

1. **Asistentes de Programación**  
   - Navega y analiza dependencias en bases de código complejas.
2. **Chatbots Avanzados y Soporte Contextual**  
   - Construye perfiles de usuario dinámicos basados en historial y preferencias.
3. **Gestión del Conocimiento y Recursos Humanos**  
   - Extrae respuestas complejas desde grandes volúmenes de texto no estructurado.

#### **GraphRAG**

Cognee se alinea con la tendencia de GraphRAG.

### ¿Qué son las Bases de Datos Gráficas?

Son sistemas de almacenamiento diseñados específicamente para **modelar, persistir y consultar relaciones complejas**. A diferencia de las bases relacionales (tablas), las gráficas se estructuran como redes de entidades conectadas.

#### **Modelo de Grafo de Propiedades**

- **Nodos**: Representan entidades (Persona, Empresa, Función, etc.)
- **Relaciones**: Conectan nodos, con dirección y tipo (ej. `LLAMA_A`, `CONOCE`)
- **Propiedades**: Atributos en nodos o relaciones (ej. `nombre: "Alice"`, `desde: 2021`)

Las relaciones son elementos persistentes, no cálculos temporales como en los `JOINs` de SQL.

#### **Comparativa: Ventajas y Desventajas**

Ventajas

- **Alto rendimiento** en consultas de múltiples saltos (traversals)
- **Flexibilidad del esquema** sin migraciones complejas
- **Modelado intuitivo**, alineado con la lógica humana

Desventajas

- **No reemplazan** las bases tradicionales para consultas tabulares masivas
- **Falta de estandarización total** en lenguajes (aunque Cypher es popular)
- **Gestión compleja** en grafos muy densos o con "supernodos"

#### **Casos de Uso más allá de RAG**

1. **Detección de Fraude**  
   Modelan redes de transacciones, usuarios, IPs y dispositivos para identificar patrones complejos en tiempo real.
2. **Motores de Recomendación**  
   Basados en interacciones entre usuarios, productos y preferencias.
3. **Gestión de Redes de TI**  
   Analizan las dependencias entre servidores, routers y servicios para diagnóstico y resiliencia.
4. **Redes Sociales y Grafos de Conocimiento**  
   Usados para análisis de comunidades, propagación de información e inferencias semánticas.


#### **Relevancia para IA Cognitiva**

Las bases gráficas son fundamentales para frameworks como **Cognee**, ya que permiten:

- Representar relaciones explícitas entre conceptos
- Recuperar subgrafos como contexto relacional
- Aplicar razonamiento lógico sobre entidades conectadas

Las bases gráficas no solo almacenan datos, **modelan el conocimiento** en su forma más natural y navegable.

### ¿Qué es Kùzu?

Kùzu es una base de datos de grafos **open source**, embebida, de alto rendimiento, diseñada para tareas analíticas (OLAP). Su filosofía es similar a la de SQLite, pero en el mundo de los grafos: se ejecuta como una **biblioteca local**, sin servidores ni configuración adicional.

#### **Ventajas Clave**

- **Embebido**: se integra directamente como librería en tu aplicación Python (`pip install kuzu`)
- **Optimizado para OLAP**: motor columnar + ejecución vectorizada = consultas analíticas rápidas
- **Integración con ecosistema Python**: soporta Pandas, Polars, DuckDB, Parquet y Arrow
- **Modelo estructurado**: define tablas de nodos y relaciones con tipos, facilitando optimizaciones


### ¿Qué es Neo4j?

Neo4j es una base de datos gráfica **nativa, madura y empresarial**, orientada tanto a cargas de trabajo analíticas (OLAP) como transaccionales (OLTP). Se presenta como una **plataforma completa** para modelar, almacenar y consultar relaciones complejas en entornos de producción.

#### **Ventajas Clave**

- **Soporte para OLTP y OLAP**  
- **ACID-compliance** para aplicaciones críticas  
- **Escalabilidad empresarial** (clústeres, alta disponibilidad)  
- **Graph Data Science (GDS)**: algoritmos de grafos integrados  
- **Comunidad y soporte extensos** (GraphAcademy, documentación, partners)  




## 🛠️ Ejemplo práctico de Qdrant

### Creación de un entorno de desarrollo

Para crear y gestionar el entorno de Python de este proyecto se utiliza `uv`, una herramienta moderna que combina la gestión de entornos virtuales y la resolución de dependencias de forma rápida y eficiente.

Este enfoque reemplaza el uso tradicional de herramientas como `venv`, `pip` y `virtualenv`, ofreciendo una experiencia más simple y ágil.

ℹ️ Para más detalles sobre cómo instalar y utilizar uv, consulta el archivo [`working-with-uv.md`](../docs/working-with-uv.md)

Una vez instalado `uv`, puedes crear el entorno virtual e instalar todas las dependencias necesarias con un solo comando:

```bash
uv venv && uv sync
```

Este comando creará un entorno virtual en el directorio del proyecto y sincronizará las librerías especificadas en el archivo `pyproject.toml`.

### Interactuando con Qdrant usando Python

#### **1. Descargar la imagen de Qdrant desde Docker Hub**

```bash
docker pull qdrant/qdrant
```

#### **2. Ejecutar el servicio**

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

#### **3. Flujo básico**

Si deseas ver un ejemplo práctico de cómo crear una colección, agregar elementos y realizar una consulta, puedes consultar el archivo [`0_quickstart`](./notebook/0_quickstart.ipynb).

Este notebook incluye ejemplos de:
- Creación de un cliente.
- Creación de una colección.
- Inserción de puntos/vectores en una colección.
- Recuperación de los puntos/vectores más cercanos.
- Aplicación de filtros en las búsquedas.

#### **4. Generación de incrustaciones (embeddings) con FastEmbed**

Si deseas ver un ejemplo práctico de cómo generar incrustaciones de texto utilizando la librería `FastEmbed`, puedes consultar el archivo [`1_fastembed_embeddings`](./notebook/1_fastembed_embeddings.ipynb).

Este notebook incluye ejemplos de:
- Instalación y carga del modelo de incrustación (`BAAI/bge-small-en-v1.5`, entre otros).
- Transformación de textos en vectores numéricos (embeddings).
- Visualización de las incrustaciones generadas.
- Preparación de los vectores para su posterior indexación en una colección de Qdrant.

#### **5. Búsqueda semántica con Qdrant**

Si deseas ver un ejemplo práctico de cómo realizar una búsqueda semántica utilizando Qdrant, puedes consultar el archivo [`2_sematic_search.ipynb`](./notebook/2_sematic_search.ipynb).

Este notebook incluye ejemplos de:
- Creación de una colección en Qdrant para búsqueda semántica.
- Inserción de vectores densos generados previamente.
- Ejecución de búsquedas basadas en similitud semántica.
- Interpretación de los resultados obtenidos en consultas de lenguaje natural.

#### **6. Construcción de un sistema RAG con Qdrant**

Si deseas ver cómo construir un sistema RAG (Retrieval-Augmented Generation) básico, puedes consultar el archivo [`3_rag_and_qdrant.ipynb`](./notebook/3_rag_and_qdrant.ipynb).

Este notebook incluye ejemplos de:
- Indexación de documentos con metadatos relevantes.
- Implementación de un flujo de recuperación y generación con OpenAI.
- Uso de Qdrant como backend para la recuperación semántica.
- Generación de respuestas fundamentadas en los documentos cargados.

#### **7. Búsqueda híbrida: combinación de vectores densos y dispersos**

Si deseas ver cómo realizar una búsqueda híbrida combinando embeddings densos y vectores dispersos (como BM25), puedes consultar el archivo [`4_hybrid_search.ipynb`](./notebook/4_hybrid_search.ipynb).

Este notebook incluye ejemplos de:
- Configuración de una colección híbrida en Qdrant.
- Inserción de puntos con vectores densos y texto para vectorización dispersa.
- Ejecución de búsquedas híbridas con fusión de puntuaciones.
- Comparación entre resultados semánticos, léxicos e híbridos.

#### **8. Sistema RAG híbrido: recuperación y generación con Qdrant y OpenAI**
Si deseas ver un ejemplo práctico de cómo construir un sistema RAG (Retrieval-Augmented Generation) que combine búsqueda híbrida y generación de lenguaje, puedes consultar el archivo [`5_rag_and_qdrant-hybrid_search.ipynb`](./notebook/5_rag_and_qdrant-hybrid_search.ipynb).

Este notebook incluye ejemplos de:
- Preparación de una colección híbrida con Qdrant a partir de un dataset de películas.
- Ejecución de búsquedas híbridas usando fusión RRF con vectores densos y dispersos.
- Construcción dinámica de prompts con resultados recuperados.
- Generación de respuestas en lenguaje natural usando un modelo de OpenAI.

## 🔗 Lectura recomendada
Recomendado para profundizar en los conceptos clave y ampliar tu comprensión

* [dlt - Getting started](https://dlthub.com/docs/intro)
* [dlt - Sourcest](https://dlthub.com/docs/dlt-ecosystem/verified-sources/)
* [dlt - Destinations](https://dlthub.com/docs/dlt-ecosystem/destinations/)
* [dlt - Qdrant destination](https://dlthub.com/docs/dlt-ecosystem/destinations/qdrant)
* [dlt - Code examples](https://dlthub.com/docs/examples)
* [dlt - Using dlt](https://dlthub.com/docs/general-usage)

* [Cognee - Quickstart](https://docs.cognee.ai/quickstart)
* [Cognee - Hello cognee SDK](https://docs.cognee.ai/tutorials/hello-cognee)
* [Cognee - Core Concepts](https://docs.cognee.ai/core-concepts)
* [Cognee - How-to Guides](https://docs.cognee.ai/how-to-guides)
* [Cognee - Colab Notebooks](https://docs.cognee.ai/reference/colab-notebooks)
* [Cognee - Cognee UI](https://docs.cognee.ai/how-to-guides/cognee-ui)

* [Kuzu - Documentation](https://docs.kuzudb.com/)
* [Kuzu - Create your first graph](https://docs.kuzudb.com/get-started/)
* [Kuzu - Python Tutorial: Analyze a Social Network](https://docs.kuzudb.com/tutorials/python/)
* [Kuzu - Python API](https://docs.kuzudb.com/client-apis/python/)
* [Kuzu - Import data](https://docs.kuzudb.com/import/)

* [Cypher - Tutorial](https://docs.kuzudb.com/tutorials/cypher/)
* [Cypher - Manual](https://docs.kuzudb.com/cypher/)
* [Cypher - Run prepared Cypher statements](https://docs.kuzudb.com/get-started/prepared-statements/)
* [Cypher - What is Cypher](https://neo4j.com/docs/getting-started/cypher/)
* [Cypher - Cheat Sheet](https://neo4j.com/docs/cypher-cheat-sheet/5/all/)

* [Neo4j - What is Neo4j?](https://neo4j.com/docs/getting-started/whats-neo4j/)
* [Neo4j - What is a graph database](https://neo4j.com/docs/getting-started/graph-database/)
* [Neo4j - Graph database concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/)
* [Neo4j - Build applications with Neo4j and Python](https://neo4j.com/docs/python-manual/current/)
* [Neo4j - Neo4j Movies Application](https://github.com/neo4j-examples/movies-python-bolt)
* [Neo4j - The Neo4j Graph Data Science Library Manualxt](https://neo4j.com/docs/graph-data-science/current/)



## ▶️ Videos recomendados
Selección de videos para reforzar visualmente los temas abordados
* [What Is A Graph Database? Common features of graph DBMSs.](https://www.youtube.com/watch?v=BksVyv5864k)
* [Cognee GraphRAG + Visualization](https://www.youtube.com/watch?v=1bezuvLwJmw)
* [Host Your Own Local LLM with Ollama & cognee](https://www.youtube.com/watch?v=aZYRo-eXDzA)



## 📚 Cursos adicionales recomendados
Recursos complementarios para seguir aprendiendo y fortaleciendo tus habilidades.

* [Graph Data Modeling Fundamentals](https://graphacademy.neo4j.com/courses/modeling-fundamentals/?category=beginners)
* [Cypher Fundamentals](https://graphacademy.neo4j.com/courses/cypher-fundamentals/?category=beginners)
* [Neo4j Fundamentals](https://graphacademy.neo4j.com/courses/neo4j-fundamentals/?category=beginners)
* [Neo4j & GenerativeAI Fundamentals](https://graphacademy.neo4j.com/courses/genai-fundamentals/?category=development)
* [Using Neo4j with Python](https://graphacademy.neo4j.com/courses/drivers-python/?category=development)
* [Build a Neo4j-backed Chatbot using Python](https://graphacademy.neo4j.com/courses/llm-chatbot-python/?category=development)

---

> 📌 **Nota:** este repositorio complementa el curso **LLM Zoomcamp** de [DataTalks.Club](https://datatalks.club/), y contiene notas, lecturas, videos, ejemplos y recursos adicionales.  
> Para acceder al contenido oficial del curso, visita el [**repositorio principal en GitHub**](https://github.com/DataTalksClub/llm-zoomcamp).
