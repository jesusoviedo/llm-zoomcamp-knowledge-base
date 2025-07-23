## 📘 Homework 3 - Evaluación de Búsqueda

Este ejercicio práctico corresponde a la quinta semana del [LLM Zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp).El objetivo es construir un sistema básico de preguntas y respuestas (Q&A) usando los documentos FAQ del curso LLM Zoomcamp, aplicando técnicas modernas de evaluación en búsqueda semántica. En este ejercicio práctico analizamos el rendimiento de búsquedas vectoriales con `minsearch` y `Qdrant`, midiendo métricas como `Hit Rate` y `MRR`. También comparamos respuestas generadas por un LLM con respuestas reales usando `cosine similarity` y `ROUGE`, evaluando así la calidad global del sistema.

🔗 [Ver enunciado original del Homework 3](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2025/03-evaluation/homework.md)

### ⚙️ Preparación del entorno

1. Descargá los archivos necesarios (`pyproject.toml` y `uv.lock`)

```bash
wget https://raw.githubusercontent.com/jesusoviedo/llm-zoomcamp-knowledge-base/refs/heads/main/homework3/pyproject.toml
wget https://raw.githubusercontent.com/jesusoviedo/llm-zoomcamp-knowledge-base/refs/heads/main/homework3/uv.lock
```

2. Creá y activá el entorno virtual con `uv`:

```bash
uv venv --recreate
source .venv/bin/activate
```

3. Creá la carpeta donde guardarás los notebooks y datos:

```bash
mkdir notebook
mkdir notebook/data
```

### 🧪 Uso de Jupyter Notebook

1. Iniciá el entorno de notebooks:

```bash
jupyter notebook &
```

### 📝 Desarrollo y solución
Descarga el archivo **[homework3_answers.ipynb](./notebook/homework3_answers.ipynb)** en la carpeta de notebooks para revisar los detalles de la solución de la tarea

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
