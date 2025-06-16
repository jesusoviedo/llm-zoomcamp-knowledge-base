## 📘 Homework 1 - Introducción a LLM y RAG

Este ejercicio práctico corresponde a la primera semana del [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp). El objetivo es construir un sistema básico de preguntas y respuestas (Q&A) usando documentos FAQ de cursos anteriores.

🔗 [Ver enunciado original del Homework 1](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2025/01-intro/homework.md#bonus-generating-the-answer-ungraded)

### ⚙️ Preparación del entorno

1. Descargá los archivos necesarios (`pyproject.toml` y `uv.lock`)

```bash
wget https://raw.githubusercontent.com/jesusoviedo/llm-zoomcamp-knowledge-base/refs/heads/main/homework1/pyproject.toml
wget https://raw.githubusercontent.com/jesusoviedo/llm-zoomcamp-knowledge-base/refs/heads/main/homework1/uv.lock
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

### Uso de Jupyter Notebook

1. Iniciá el entorno de notebooks:

```bash
jupyter notebook &
```

### Desarrollo y solución
Descarga el archivo **[homework1_answers.ipynb](./notebook/homework1_answers.ipynb)** en la carpeta de notebooks para revisar los detalles de la solución de la tarea

### Comandos útiles

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
