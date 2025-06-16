## Homework 1

**[Enunciado Homework1](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/cohorts/2025/01-intro/homework.md#bonus-generating-the-answer-ungraded)**

### Descargar el archivo `pyproject.toml` y `uv.lock`

```bash
wget https://raw.githubusercontent.com/jesusoviedo/llm-zoomcamp-knowledge-base/refs/heads/main/homework1/pyproject.toml
wget https://raw.githubusercontent.com/jesusoviedo/llm-zoomcamp-knowledge-base/refs/heads/main/homework1/uv.lock
```

### Instalar las dependencias necesarias

```bash
uv venv --recreate
```

### Crear carpeta para notebooks

```bash
mkdir notebook
```

### Iniciar Jupyter

```bash
source .venv/bin/activate
```

```bash
jupyter notebook &
```

### Desarrollo de la tarea
Descarga el archivo **[homework1_answers.ipynb](./notebook/homework1_answers.ipynb)** en la carpeta de notebooks para revisar los detalles de la solución de la tarea

*Comando para detener todos los servicios de notebook:*

```bash
pkill -f jupyter
```

*Comando para salir del entorno:*

```bash
deactivate
```