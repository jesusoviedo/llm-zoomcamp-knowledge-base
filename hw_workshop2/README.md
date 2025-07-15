## 📘 Homework Workshop 2 - Agentes

Este ejercicio práctico corresponde al Workshop 2 del [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp). El objetivo de este ejercicio es construir un sistema básico de agentes capaz de interactuar con funciones externas mediante el uso del **Model-Context Protocol (MCP)**. Usamos funciones simples relacionadas con datos del clima y exploramos cómo exponerlas como herramientas accesibles para un LLM. Además, montamos un servidor MCP con `FastMCP` y aprendemos a comunicarnos con él tanto desde scripts como desde una interfaz de chat. 

¿Qué aprenderás?
- Cómo definir funciones para ser usadas por agentes mediante `function calling`.
- Cómo levantar un servidor MCP con `FastMCP`.
- Cómo comunicarte con un servidor MCP a través de comandos JSON-RPC.
- Cómo integrar herramientas externas en un flujo conversacional.
- Cómo usar agentes para tomar decisiones y ejecutar funciones basadas en entradas del usuario.

🔗 [Ver enunciado original del Homework Workshop 2](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2025/0a-agents/homework.md)


### ⚙️ Preparación del entorno

1. Descargá los archivos necesarios (`pyproject.toml` y `uv.lock`)

```bash
wget https://raw.githubusercontent.com/jesusoviedo/llm-zoomcamp-knowledge-base/refs/heads/main/hw_workshop2/pyproject.toml
wget https://raw.githubusercontent.com/jesusoviedo/llm-zoomcamp-knowledge-base/refs/heads/main/hw_workshop2/uv.lock
```

2. Creá y activá el entorno virtual con `uv`:

```bash
uv venv --recreate
source .venv/bin/activate
```

3. Creá la carpeta donde guardarás los notebooks:

```bash
mkdir notebook
```

### 🧪 Uso de Jupyter Notebook

1. Iniciá el entorno de notebooks:

```bash
jupyter notebook &
```

### 📝 Desarrollo y solución
Descarga el archivo **[hw_workshop2_answers.ipynb](./notebook/hw_workshop2_answers.ipynb)** en la carpeta de notebooks para revisar los detalles de la solución de la tarea

### 🛠️ Comandos útiles

1. Para detener Jupyter Notebook:

```bash
pkill -f jupyter
```

2. Para salir del entorno virtual:

```bash
deactivate
```

---

> 📌 **Nota:** este repositorio complementa el curso **LLM Zoomcamp** de [DataTalks.Club](https://datatalks.club/), y contiene notas, lecturas, videos, ejemplos y recursos adicionales.  
> Para acceder al contenido oficial del curso, visita el [**repositorio principal en GitHub**](https://github.com/DataTalksClub/llm-zoomcamp).
