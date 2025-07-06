## 📘 Homework Workshop 1 - De REST al razonamiento con DLT y Cognee

Este ejercicio práctico corresponde al Workshop 1 del [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp). El objetivo es construir un sistema básico de preguntas y respuestas (Q&A) utilizando documentos de tipo FAQ del curso **Machine Learning Zoomcamp**, empleando la librería `dlt` junto con `Qdrant`. En lugar de generar embeddings manualmente y cargarlos en una base de vectores, en este ejercicio exploraremos cómo crear un **pipeline automatizado de ingesta** de datos que:

- Descarga y transforma los documentos FAQ desde un recurso remoto.
- Aplica automáticamente un modelo de embeddings para representar los textos.
- Inserta los datos enriquecidos en una colección de Qdrant

Todo esto se realiza con un enfoque moderno basado en `dlt` y su soporte para `Qdrant`, facilitando tanto la creación del pipeline como el control del proceso de transformación.

🔗 [Ver enunciado original del Homework Workshop 1](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2025/workshops/dlt.md)

### ⚙️ Preparación del entorno

1. Descargá los archivos necesarios (`pyproject.toml` y `uv.lock`)

```bash
wget https://raw.githubusercontent.com/jesusoviedo/llm-zoomcamp-knowledge-base/refs/heads/main/hw_workshop1/pyproject.toml
wget https://raw.githubusercontent.com/jesusoviedo/llm-zoomcamp-knowledge-base/refs/heads/main/hw_workshop1/uv.lock
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
Descarga el archivo **[hw_workshop1_answers.ipynb](./notebook/hw_workshop1_answers.ipynb)** en la carpeta de notebooks para revisar los detalles de la solución de la tarea

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
