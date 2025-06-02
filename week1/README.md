# Semana 1 - LLM Zoomcamp

Este documento recopila mis apuntes y recursos para la **Semana 1** del curso LLM Zoomcamp.

## 📝 Notas de la teoría

### Definición de LLM 

Un LLM (Large Language Model) es un modelo de lenguaje basado en redes neuronales profundas, entrenado para predecir el siguiente token (una palabra, parte de una palabra o símbolo) en una secuencia de texto. A partir de grandes volúmenes de datos textuales, aprende patrones sintácticos, semánticos y contextuales, lo que le permite generar respuestas coherentes, relevantes y con apariencia humana.

Los LLM más avanzados están compuestos por miles de millones o incluso billones de parámetros. Estos parámetros —los pesos de la red neuronal— representan el conocimiento adquirido durante el entrenamiento.

El rendimiento de un LLM depende en gran medida de tres factores:
* La cantidad y diversidad del corpus de entrenamiento
* La escala del modelo (número de parámetros)
* Y su arquitectura, siendo el Transformer la base de los modelos modernos.

**¿Cómo predice tokens un LLM?**
1. Se introduce un prompt o secuencia inicial de texto.
2. El modelo calcula la probabilidad de cada posible token que podría continuar la secuencia.
3. Se selecciona el token más probable (o uno entre los más probables, usando técnicas como muestreo o top-k).
4. El token elegido se agrega al texto y el proceso se repite hasta completar la respuesta.

### Definición de RAG

### Crear entorno

Para crear y gestionar el entorno de Python de este proyecto se utiliza `uv`, una herramienta moderna que combina gestión de entornos virtuales y resolución de dependencias de forma rápida y eficiente.

Este enfoque reemplaza el uso tradicional de herramientas como `venv`, `pip` y `virtualenv`, ofreciendo una experiencia más simple y veloz.

ℹ️ Para más detalles sobre cómo instalar y utilizar uv, consulta el archivo [`working-with-uv.md`](../docs/working-with-uv.md)

Una vez instalado `uv`, puedes crear el entorno virtual e instalar todas las dependencias necesarias con un solo comando:

```bash
uv venv && uv sync
```

Esto creará un entorno virtual en el directorio del proyecto y sincronizará las librerías especificadas en el archivo `pyproject.toml`.

### Usando la API de OpenAI





## 💻 Ejemplos de código

```python
# Ejemplo: cargar un modelo GPT simple
```

## 🔗 Lectura recomendada
Recomendado para profundizar en los conceptos clave y ampliar tu comprensión
* [Del prompt a la respuesta: el poder de los Large Language Models](https://medium.com/@j92riquelme/del-prompt-a-la-respuesta-el-poder-de-los-large-language-models-b4a28663fed9)
* [¿Qué son los modelos de lenguaje de grandes (LLM)?](https://azure.microsoft.com/es-es/resources/cloud-computing-dictionary/what-are-large-language-models-llms)
* [Introduction to Large Language Models](https://developers.google.com/machine-learning/resources/intro-llms)

## 🔗 Videos recomendados
Selección de videos para reforzar visualmente los temas abordados
* [Introducción a la IA generativa](https://www.youtube.com/watch?v=tNBvUvsScAA&t=1s)
* [Introducción a los modelos de lenguaje grandes](https://www.youtube.com/watch?v=Vi0ODh3ncxw&t=3s)
* [Introduction to Responsible AI](https://www.youtube.com/watch?v=JbluXe6QpxM&t=4s)


## Cursos adicionales recomendados
Recursos complementarios para seguir aprendiendo y fortaleciendo tus habilidades.

* [Introduction to Generative AI Learning Path](https://www.cloudskillsboost.google/paths/118)


---

> 📌 **Nota:** este repositorio complementa el curso **LLM Zoomcamp** de [DataTalks.Club](https://datatalks.club/), y contiene notas, lecturas, videos, ejemplos y recursos adicionales.  
> Para acceder al contenido oficial del curso, visita el [**repositorio principal en GitHub**](https://github.com/DataTalksClub/llm-zoomcamp).
