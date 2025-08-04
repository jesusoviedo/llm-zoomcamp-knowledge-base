# Workshop 2 - De RAG a Agentes: Creando Asistentes de IA Inteligentes

Este documento recopila mis apuntes y recursos para la **Workshop 2** del curso LLM Zoomcamp.

## 📚 Recursos del Workshop

- **Video del Workshop - parte 1**: [Ver en YouTube](https://www.youtube.com/watch?v=GH3lrOsU3AU)
- **Video del Workshop - parte 2**: [Ver en YouTube](https://www.youtube.com/watch?v=yS_hwnJusDk)
- **Repositorio del Workshop**: [Ver en GigHub](https://github.com/alexeygrigorev/rag-agents-workshop)
- **Librería de chat open source para propósitos educativos**: [toyaikit](https://github.com/alexeygrigorev/toyaikit)

## 📝 Notas de la teoría

La inteligencia artificial está entrando en una nueva fase: los modelos ya no solo responden, ahora piensan, deciden y actúan. Esta transformación da lugar a los **agentes**, sistemas capaces de interactuar con su entorno, utilizar herramientas externas, adaptarse al contexto y perseguir objetivos de manera autónoma.

### 1. Agentes de IA: La Unidad de Autonomía

Un agente es la unidad fundamental de la IA autónoma. A diferencia de un modelo pasivo que solo responde a una entrada, un agente opera dentro de un ciclo de percepción-acción.

* **Ideas Centrales:**
    * Un agente **observa** su entorno (digital o físico), **toma decisiones** de forma independiente para alcanzar un objetivo y **ejecuta acciones** a través de herramientas.
    * Posee una **memoria** para registrar el historial de acciones pasadas, lo que le permite aprender y ajustar su estrategia. Se divide en:
        * **Memoria de Corto Plazo (Working Memory):** Contexto de la tarea actual.
        * **Memoria de Largo Plazo (Persistent Memory):** Conocimientos y experiencias pasadas, a menudo implementada con bases de datos vectoriales (ej. Qdrant).

* **Características Esenciales:**
    * **Autonomía:** Opera sin intervención humana directa.
    * **Proactividad:** Inicia acciones para alcanzar objetivos.
    * **Reactividad:** Responde a los cambios en su entorno.
    * **Ciclo de Operación (OODA):** Observar, Orientar, Decidir, Actuar.


### 2. Llamadas a Funciones (Tool Use): El Puente hacia el Mundo Real

Los agentes no actúan directamente; utilizan herramientas (`tools`). Las llamadas a funciones son el mecanismo seguro y estructurado que conecta el "cerebro" del agente (el LLM) con el mundo real (APIs, bases de datos, scripts).

* **Ideas Centrales:**
    * El LLM no ejecuta código. En su lugar, genera una solicitud estructurada (generalmente JSON) especificando qué herramienta usar y con qué parámetros.
    * El código del desarrollador recibe esta solicitud, ejecuta la función correspondiente de forma segura y devuelve el resultado al agente.
    * Este desacoplamiento es clave para la seguridad, el control y la fiabilidad del sistema.

* **Características Esenciales:**
    * **Extensibilidad:** Permite dotar al agente de cualquier capacidad accesible mediante código.
    * **Control:** El desarrollador mantiene el control total sobre la ejecución de las herramientas.
    * **Capacidad Múltiple:** Un agente puede tener acceso a un "cinturón de herramientas" y decidir cuál usar (o varias en paralelo) según la tarea.

### 3. Agentic RAG: De la Búsqueda Pasiva a la Investigación Activa

Agentic RAG transforma el patrón de Retrieval-Augmented Generation de un proceso lineal a una investigación dinámica y proactiva.

* **Ideas Centrales:**
    * **RAG Tradicional:** `Pregunta -> Búsqueda en Vector DB -> Respuesta`. Es un proceso de un solo paso y reactivo.
    * **Agentic RAG:** El agente actúa como un "investigador experto". Recibe una pregunta compleja y diseña un plan de varios pasos para resolverla.

* **Características Esenciales:**
    * **Refinamiento Iterativo:** Si la primera búsqueda es insuficiente, el agente refina la consulta, la descompone en sub-preguntas y vuelve a buscar.
    * **Autocorrección:** El agente puede evaluar la relevancia de la información recuperada. Si no es útil, puede decidir buscar en otra fuente de datos o usar una herramienta diferente.
    * **Orquestación de Múltiples Fuentes:** Puede consultar varias bases de datos vectoriales, bases de datos relacionales o APIs web dentro de la misma tarea.

### 4. Agentic Search: Navegación Inteligente en Datos Vivos

Es una aplicación especializada de un agente cuyo objetivo es responder preguntas complejas que requieren información actualizada y disponible en la web.

* **Ideas Centrales:**
    * Va más allá de una simple llamada a una API de búsqueda.
    * El agente planifica una estrategia de búsqueda, ejecuta consultas (ej. usando la API de Brave Search), analiza los resultados, y puede decidir "profundizar" y navegar por los enlaces para extraer información más detallada.

* **Características Esenciales:**
    * **Razonamiento Multi-paso:** Combina resultados de diferentes búsquedas para construir una respuesta coherente.
    * **Adaptabilidad:** Puede manejar la naturaleza ruidosa y no estructurada de los datos de la web.
    * **Síntesis:** No se limita a devolver enlaces, sino que sintetiza la información encontrada en una respuesta directa.

### 5. MCP (Model Context Protocol): El Estándar para un Ecosistema Conectado

MCP es la pieza que permite escalar las arquitecturas de agentes. Es un protocolo abierto que estandariza la comunicación entre los modelos de IA y sus herramientas.

* **Ideas Centrales:**
    * Resuelve el problema de la integración "N x M", donde cada uno de los N agentes necesita una integración a medida para cada una de las M herramientas.
    * La metáfora clave es el **"USB-C para la IA"**: un único estándar de conexión que garantiza la interoperabilidad.

* **Características Esenciales:**
    * **Arquitectura Cliente-Servidor:**
        * **Host/Cliente (el Agente):** Descubre y consume herramientas.
        * **Servidor (la Herramienta):** Expone sus capacidades siguiendo el protocolo MCP.
    * **Agnóstico al Modelo:** Funciona con cualquier modelo de IA.
    * **Interoperabilidad:** Un agente puede conectarse y usar cualquier herramienta que "hable" MCP sin necesidad de código personalizado, fomentando un ecosistema de herramientas reutilizables.

## 🛠️ Ejemplo práctico de Agentes

### Creación de un entorno de desarrollo

Para crear y gestionar el entorno de Python de este proyecto se utiliza `uv`, una herramienta moderna que combina la gestión de entornos virtuales y la resolución de dependencias de forma rápida y eficiente.

Este enfoque reemplaza el uso tradicional de herramientas como `venv`, `pip` y `virtualenv`, ofreciendo una experiencia más simple y ágil.

ℹ️ Para más detalles sobre cómo instalar y utilizar uv, consulta el archivo [`working-with-uv.md`](../docs/working-with-uv.md)

Una vez instalado `uv`, puedes crear el entorno virtual e instalar todas las dependencias necesarias con un solo comando:

```bash
uv venv && uv sync
```

Este comando creará un entorno virtual en el directorio del proyecto y sincronizará las librerías especificadas en el archivo `pyproject.toml`.

### Ejemplos prácticos de agentes y técnicas avanzadas con LLMs

#### **1. Uso de Agentic RAG para respuestas enriquecidas**

Si deseas explorar cómo un sistema **Agentic RAG** puede tomar decisiones autónomas sobre qué documentos recuperar y cómo usarlos para generar respuestas, puedes revisar el archivo [`agentic_rag.ipynb`](./notebook/agentic_rag.ipynb).

#### **2. Uso de Agentic Search para búsquedas controladas y adaptativas**

Para experimentar con **Agentic Search**, donde el LLM controla activamente el flujo de búsqueda (por ejemplo, decidir cuándo hacer más queries o afinar resultados), revisa el archivo [`agentic_search.ipynb`](./notebook/agentic_search.ipynb).

#### **3. Uso de Function Calling para integrar herramientas externas**

Puedes ver cómo utilizar **Function Calling** con modelos de OpenAI para que un asistente pueda invocar funciones cuando lo necesite en el archivo [`function_calling.ipynb`](./notebook/function_calling.ipynb).

#### **4. Uso de PydanticAI para validar estructuras de salida**

Para explorar cómo **PydanticAI** permite controlar y validar las salidas generadas por LLMs mediante modelos de datos, consulta el archivo [`using_pydanticai.ipynb`](./notebook/using_pydanticai.ipynb).

## 🔗 Lectura recomendada
Recomendado para profundizar en los conceptos clave y ampliar tu comprensión

* [La Revolución Agéntica: de modelos reactivos a ecosistemas de IA autónomos](https://medium.com/@j92riquelme/la-revolucion-agentica-6c055c8fe405)
* [ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners)
* [LLM Agents](https://www.promptingguide.ai/research/llm-agents)
* [Function Calling with LLMs](https://www.promptingguide.ai/applications/function_calling)
* [How LLMs Use Tools: A Step-by-Step Guide to Controlled AI Agents](https://medium.com/superdatascience/how-llms-use-tools-a-step-by-step-guide-to-controlled-ai-agents-dbc44ac4b785)
* [Get started with the Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction)
* [Model Context Protocol (MCP) an overview](https://www.philschmid.de/mcp-introduction?source=post_page-----7dee927e7223---------------------------------------#why-is-there-so-much-hype-did-mcp-win)
* [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
* [What is Agentic Search?](https://swirlaiconnect.com/blog/what-is-agentic-search)
* [What Is Agentic Search? Breaking Down the Concept and Definition](https://ninepeaks.io/what-is-agentic-search#:~:text=Agentic%20search%20systems%20work%20independently,process%2C%20and%20visualize%20operational%20data)
* [Agentic Search in Action: A Practical Guide to Building from Scratch](https://medium.com/google-cloud/agentic-search-in-action-a-practical-guide-to-building-from-scratch-e100422f27b2)
* [What is agentic RAG?](https://www.ibm.com/think/topics/agentic-rag#763338456)
* [What is Agentic RAG](https://weaviate.io/blog/what-is-agentic-rag)
* [An introduction to function calling and tool use](https://www.apideck.com/blog/llm-tool-use-and-function-calling)
* [tool-calling-guide](https://github.com/ALucek/tool-calling-guide)
* [mcp-for-beginners](https://github.com/microsoft/mcp-for-beginners)
* [Function calling](https://platform.openai.com/docs/guides/function-calling?api-mode=responses)
* [Brave Search API](https://brave.com/search/api/tools/)
* [Google Search API](https://serpapi.com/)
* [Dify](https://dify.ai)
* [PydanticAI](https://ai.pydantic.dev/)


## ▶️ Videos recomendados
Selección de videos para reforzar visualmente los temas abordados

* [What are AI Agents?](https://www.youtube.com/watch?v=F8NKVhkZZWI)
* [5 Types of AI Agents](https://www.youtube.com/watch?v=fXizBc03D7E)
* [IA + tu código: llamada a funciones](https://www.youtube.com/watch?v=NbAGbXr4DME)
* [What is Tool Calling?](https://www.youtube.com/watch?v=h8gMhXYAv1k)
* [What is Agentic RAG?](https://www.youtube.com/watch?v=0z9_MhcYvcY)
* [¿Qué es el RAG agentico?](https://www.youtube.com/watch?v=WcjAARvdL7I)
* [AI Agents in Action: How Research Agents Solve Complex Problems](https://www.youtube.com/watch?v=j_Q1cL6Cog4)
* [AI Search Agents Redefined: Agentic Research, MCP, & Tool Calling](https://www.youtube.com/watch?v=pUUzXimhUuA&t=1s)
* [What is MCP?](https://www.youtube.com/watch?v=eur8dUO9mvE)
* [MCP vs API](https://www.youtube.com/watch?v=7j1t3UZA1TY&t=78s)



## 📚 Cursos adicionales recomendados
Recursos complementarios para seguir aprendiendo y fortaleciendo tus habilidades.

* [Agentes de IA para principiantes](https://learn.microsoft.com/es-es/shows/ai-agents-for-beginners/)
* [Functions, Tools and Agents with LangChain](https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/)
* [Building Agentic RAG with LlamaIndex](https://www.deeplearning.ai/short-courses/building-agentic-rag-with-llamaindex/)
* [Generative AI for Software Development Skill Certificate](https://www.coursera.org/professional-certificates/generative-ai-for-software-development?utm_campaign=dlai-lp&utm_medium=institutions&utm_source=deeplearning-ai)
* [Generative AI for Everyone](https://www.coursera.org/learn/generative-ai-for-everyone?utm_campaign=genai4e-launch&utm_medium=institutions&utm_source=deeplearning-ai)

---

> 📌 **Nota:** este repositorio complementa el curso **LLM Zoomcamp** de [DataTalks.Club](https://datatalks.club/), y contiene notas, lecturas, videos, ejemplos y recursos adicionales.  
> Para acceder al contenido oficial del curso, visita el [**repositorio principal en GitHub**](https://github.com/DataTalksClub/llm-zoomcamp).
