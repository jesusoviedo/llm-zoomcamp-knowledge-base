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




## 🛠️ Ejemplo práctico de Kùzu, Neo4j, Cognee y DLT

### Creación de un entorno de desarrollo

Para crear y gestionar el entorno de Python de este proyecto se utiliza `uv`, una herramienta moderna que combina la gestión de entornos virtuales y la resolución de dependencias de forma rápida y eficiente.

Este enfoque reemplaza el uso tradicional de herramientas como `venv`, `pip` y `virtualenv`, ofreciendo una experiencia más simple y ágil.

ℹ️ Para más detalles sobre cómo instalar y utilizar uv, consulta el archivo [`working-with-uv.md`](../docs/working-with-uv.md)

Una vez instalado `uv`, puedes crear el entorno virtual e instalar todas las dependencias necesarias con un solo comando:

```bash
uv venv && uv sync
```

Este comando creará un entorno virtual en el directorio del proyecto y sincronizará las librerías especificadas en el archivo `pyproject.toml`.

### Ejemplos de uso de grafos y sistemas cognitivos

A continuación, se presentan notebooks que exploran el uso de diferentes bases de datos de grafos y sistemas cognitivos aplicados a tareas de análisis y representación de conocimiento.


#### **1. Uso de Kùzu para consultas con grafos**

Si deseas ver cómo utilizar la base de datos de grafos **Kùzu** para realizar consultas sobre relaciones complejas, puedes consultar el archivo [`using_kuzu.ipynb`](./notebook/using_kuzu.ipynb).

Este notebook incluye ejemplos de:
- Instalación y configuración de Kùzu.
- Creación de nodos y relaciones.
- Ejecución de consultas en lenguaje Cypher.

#### **2. Uso de Neo4j para modelado de grafos**

Para aprender a trabajar con **Neo4j**, una base de datos de grafos ampliamente utilizada en producción, revisa el archivo [`using_neo4j.ipynb`](./notebook/using_neo4j.ipynb).

Este notebook incluye ejemplos de:
- Conexión a una instancia local de Neo4j.
- Inserción de datos con Cypher.
- Ejecución de consultas para analizar relaciones.

#### **3. Uso de Cognee como sistema cognitivo basado en grafos**

Si deseas explorar cómo **Cognee** utiliza memoria estructurada y grafos para potenciar la inteligencia artificial, puedes revisar el archivo [`using_cognee.ipynb`](./notebook/using_cognee.ipynb).

Este notebook incluye ejemplos de:
- Inicialización y configuración de Cognee.
- Inserción de conocimiento en el grafo cognitivo.
- Consultas y navegación por el grafo.
- Integración con embeddings y herramientas externas.

#### **4. Integración de DLT, Cognee y Kùzu con un dataset real**

Para ver una integración práctica entre **DLT**, **Cognee** y **Kùzu**, puedes consultar el archivo [`dlt_and_cognee_taxi_dataset.ipynb`](./notebook/dlt_and_cognee_taxi_dataset.ipynb).

Este notebook incluye ejemplos de:
- Extracción y transformación de datos con DLT.
- Ingesta del dataset de taxis en un grafo usando Kùzu.
- Enriquecimiento del conocimiento con Cognee.
- Análisis y consultas cognitivas sobre datos reales

#### **5. Análisis constitucional con Cognee**

Puedes consultar el archivo [`understanding_paraguays_constitution_with_cognee.ipynb`](./notebook/understanding_paraguays_constitution_with_cognee.ipynb), que muestra cómo utilizar **Cognee** para:

- Descargar y procesar el texto completo de la Constitución Nacional del Paraguay.
- Generar un grafo de conocimiento con entidades y relaciones extraídas del documento.
- Realizar búsquedas semánticas y consultas cognitivas sobre el contenido constitucional.
- Visualizar las conexiones clave entre conceptos jurídicos utilizando herramientas de grafo.

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
* [Neo4j - Example datasets](https://neo4j.com/docs/getting-started/appendix/example-data/)
* [Neo4j - Neo4j Tutorial: Using And Querying Graph Databases in Python](https://www.datacamp.com/tutorial/neo4j-tutorial)
* [De la Ingesta de Datos a la Inferencia Cognitiva: Una Arquitectura Moderna con dlt, RAG, Cognee y Bases de Datos Gráficas](https://medium.com/@j92riquelme/de-la-ingesta-de-datos-a-la-inferencia-cognitiva-una-arquitectura-moderna-con-dlt-rag-cognee-e18fdd6e94f8)
* [Dominando Cognee: Estructuración de Conocimiento con Pipelines, Ontologías y el SDK](https://medium.com/@j92riquelme/dominando-cognee-estructuracion-de-conocimiento-con-pipelines-ontologias-y-el-sdk-4ae15fdddb1b)
* [¿Puede una IA entender la Constitución del Paraguay? Mi experiencia con Cognee](https://medium.com/@j92riquelme/puede-una-ia-entender-la-constitucion-del-paraguay-mi-experiencia-con-dlt-y-cognee-6715f5708b83)


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
* [Neo4j Course for Beginners](https://www.youtube.com/watch?v=_IgbB24scLI)

---

> 📌 **Nota:** este repositorio complementa el curso **LLM Zoomcamp** de [DataTalks.Club](https://datatalks.club/), y contiene notas, lecturas, videos, ejemplos y recursos adicionales.  
> Para acceder al contenido oficial del curso, visita el [**repositorio principal en GitHub**](https://github.com/DataTalksClub/llm-zoomcamp).
