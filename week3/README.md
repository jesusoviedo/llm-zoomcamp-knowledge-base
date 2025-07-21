# Semana 3 - LLM Zoomcamp

Este documento recopila mis apuntes y recursos para la **Semana 3** del curso LLM Zoomcamp.

## 📝 Notas de la teoría

### Importancia de la Evaluación

Es fundamental evaluar los resultados de búsqueda para optimizar cómo se almacenan y recuperan los datos en un sistema RAG (Retrieval-Augmented Generation). Sin una evaluación adecuada, es difícil saber si el sistema está devolviendo resultados útiles y relevantes. El rendimiento ideal siempre depende de los datos disponibles y los requisitos específicos del caso de uso.

El objetivo es medir de forma objetiva qué tan bueno es un sistema de búsqueda. En lugar de confiar en la intuición, usamos métricas para cuantificar el rendimiento. Esto nos permite comparar diferentes sistemas (como Elasticsearch o Qdrant vs. otro motor de búsqueda) o diferentes configuraciones del mismo sistema.


### Datos de Referencia (Ground Truth)

Para evaluar un sistema de recuperación, se necesita un conjunto de datos de referencia (también conocido como *ground truth* o *gold standard data*). Este conjunto contiene consultas junto con los documentos relevantes para cada una.

#### Necesidad de un "Ground Truth"
Es indispensable contar con este conjunto para evaluar de manera efectiva el rendimiento del sistema. Cada entrada debería vincular una pregunta con el documento que contiene la respuesta correcta.

#### Estructura del Conjunto de Datos
Idealmente, el conjunto contiene miles de preguntas, y para cada una se identifican los documentos relevantes. En algunos casos, como simplificación, se asume que existe **un solo documento relevante por pregunta**.

#### Métodos para Crear Ground Truth

- **Anotación Humana**: Especialistas etiquetan manualmente las preguntas con sus documentos relevantes. Es el método más preciso, aunque costoso y lento.
- **Observación del Usuario**: Se analiza el comportamiento real de los usuarios. Puede ser evaluado por humanos o por LLMs.
- **Generación Automática con LLM**: Usar un modelo como GPT-4 para generar preguntas y asociarlas automáticamente a documentos de referencia (por ejemplo, desde un conjunto de preguntas frecuentes).

#### Creación de un ID de Documento Único
Para asegurar trazabilidad, se genera un hash (MD5) con los campos del documento (curso, pregunta, texto), lo que garantiza que el ID cambie solo si el contenido cambia.

#### Ejemplo de Implementación
- Se carga un conjunto de documentos.
- Se asigna un ID único a cada uno.
- Se diseña un prompt detallado que instruye al LLM a actuar como un estudiante y generar cinco preguntas variadas por FAQ.
- El resultado es almacenado como un DataFrame y luego exportado a CSV.

#### Optimización de la Búsqueda

Varios parámetros de búsqueda pueden ajustarse para mejorar los resultados obtenidos. Algunos ejemplos incluyen:

- Tipo de búsqueda: densa, híbrida, BM25.
- Campos del documento que se consultan: título, cuerpo, metadatos, etc.
- Uso de boosting para priorizar campos como `question`.
- Filtros por categoría, curso o tipo de contenido.

La evaluación es la herramienta clave para identificar qué configuración produce el mejor rendimiento en función de las necesidades del usuario.

#### Métricas de Ranking Comunes

Para cuantificar la calidad de los resultados, se utilizan diversas métricas. Algunas de las más comunes incluyen:

- Precisión en k (P@k)
- Recall
- Mean Average Precision (MAP)
- Normalized Discounted Cumulative Gain (NDCG)
- Mean Reciprocal Rank (MRR)
- F1 Score
- Area Under the ROC curve (AUC-ROC)
- Mean Rank (MR)
- Hit Rate (HR) o Recall at K
- Expected Reciprocal Rank (ERR)

Cada una de estas métricas captura distintos aspectos del rendimiento del sistema, como la precisión, el orden de los resultados o la cobertura.


### Entendiendo las Métricas

Evaluar un sistema de recuperación o recomendación no solo implica observar si los resultados son buenos, sino también **cuán buenos**, **cuán rápidos** y **cuán completos** son. Para eso, se utilizan diversas métricas, cada una con su propia lógica y aplicaciones. A continuación, exploramos las más relevantes.

### **Precisión en k (P@k)**

Mide la proporción de documentos relevantes dentro de los primeros **k** resultados.

* **Fórmula:**  
  $P@k = \frac{\text{Número de documentos relevantes en los primeros k resultados}}{k}$

#### **Explicación Detallada**

Esta es la métrica más intuitiva. Imagina que buscas algo en Google y solo miras los primeros 10 resultados. La **Precisión en 10 (P@10)** te dice qué porcentaje de esos 10 enlaces fue realmente útil. No le importa si había más resultados buenos en la página 2; solo se enfoca en la calidad de la primera "vitrina" de resultados que ve el usuario.

#### **Casos de Uso Comunes**

- **Motores de búsqueda web (Google, Bing):** La mayoría de los usuarios no pasa de la primera página.
- **Búsqueda en e-commerce (Amazon):** Si buscas "zapatillas rojas", quieres ver zapatillas rojas inmediatamente.
- **Sistemas de recomendación (Netflix, Spotify):** Es crucial que las primeras recomendaciones sean atractivas.

### **Recall (Exhaustividad o Sensibilidad)**

Mide la proporción de documentos relevantes que el sistema logró encontrar de entre el **total** de documentos relevantes que existen.

* **Fórmula:**  
  $Recall = \frac{\text{Número de documentos relevantes recuperados}}{\text{Número total de documentos relevantes}}$

#### **Explicación Detallada**

El Recall se enfoca en la **cobertura**. No le importa si los resultados buenos están al principio o al final, solo quiere saber si el sistema fue capaz de encontrarlos todos. El objetivo es minimizar los "falsos negativos", es decir, no dejar fuera nada importante.

#### **Casos de Uso Comunes**

- **Búsquedas legales o de patentes:** Es crítico encontrar todos los documentos pertinentes.
- **Diagnóstico médico:** Se requiere considerar todas las posibilidades.
- **Detección de fraude o amenazas:** Es preferible detectar de más (falsos positivos) que pasar por alto algo grave.

### **Puntuación F1 (F1 Score)**

Es la media armónica de la Precisión y el Recall. Busca un equilibrio entre ambos.

* **Fórmula:**  
  $F1 = 2 \cdot \frac{Precision \cdot Recall}{Precision + Recall}$

#### **Explicación Detallada**

La puntuación F1 es el gran pacificador entre Precisión y Recall. Es imposible obtener un F1 alto si una de las dos métricas es muy baja. La media armónica penaliza los extremos, obligando al sistema a ser balanceado.

#### **Casos de Uso Comunes**

- **Clasificación de texto y análisis de sentimiento.**
- **Evaluación general de un sistema:** Proporciona una única cifra para resumir rendimiento.


### **Rango Recíproco Medio (Mean Reciprocal Rank - MRR)**

Evalúa la posición en el ranking del **primer** documento relevante encontrado.

* **Fórmula:**  
  $MRR = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{rank_i}$  
  - $|Q|$ es el número total de búsquedas.  
  - $rank_i$ es la posición del primer resultado correcto para la búsqueda $i$.

#### **Explicación Detallada**

¿El sistema encontró una buena respuesta rápido? Si la respuesta correcta aparece primero, el puntaje es 1. En la segunda posición, 1/2. En la tercera, 1/3, y así sucesivamente. El MRR promedia esta eficiencia a lo largo de muchas búsquedas.

#### **Casos de Uso Comunes**

- **Sistemas de preguntas y respuestas (FAQs).**
- **Chatbots de soporte.**
- **Autocompletado o resultados tipo "Voy a tener suerte".**

### **Ganancia Cumulativa Descontada Normalizada (NDCG)**

Mide la utilidad (o ganancia) de un documento según su posición en la lista de resultados.

* **Fórmula:**  
  $NDCG = \frac{DCG}{IDCG}$  
  - **DCG:** suma la relevancia de cada documento, pero “descuenta” su valor cuanto más abajo esté.  
  - **IDCG:** es el DCG ideal (orden perfecto).

#### **Explicación Detallada**

NDCG es una de las métricas más completas:
1. **Reconoce niveles de relevancia.**
2. **Penaliza posiciones bajas.**

El resultado normalizado varía entre 0 y 1, donde 1 representa un ranking perfecto.

#### **Casos de Uso Comunes**

- **Motores de búsqueda y sistemas de recomendación.**
- **Comparación de modelos en competiciones y benchmarks.**

### **Precisión Media Promedio (Mean Average Precision - MAP)**

Calcula la precisión promedio para cada búsqueda y luego promedia estos valores entre todas.

* **Fórmula:**  
  $MAP = \frac{1}{|Q|} \sum_{q \in Q} \text{Average Precision(q)}$

#### **Explicación Detallada**

El MAP recompensa que los documentos relevantes estén lo más arriba posible en los resultados. Aunque no diferencia grados de relevancia, mide bien el orden general de los aciertos.

#### **Casos de Uso Comunes**

- **Búsqueda de imágenes o documentos.**
- **Benchmarks académicos en recuperación de información.**

### **Tasa de Aciertos (Hit Rate - HR)**

Mide la proporción de búsquedas donde se recuperó **al menos un** documento relevante en el top **k**.

* **Fórmula:**  
  $HR@k = \frac{\text{Número de búsquedas con al menos un acierto en el top k}}{|Q|}$

#### **Explicación Detallada**

Es una métrica de “todo o nada”: ¿hubo al menos un resultado útil en el top **k**? No se preocupa por cuántos, solo por si hubo al menos uno.

#### **Casos de Uso Comunes**

- **Sistemas de recomendación.**
- **Validación de sistemas simples de recuperación.**


### **Rango Recíproco Esperado (Expected Reciprocal Rank - ERR)**

Evalúa la calidad del ranking considerando **la probabilidad de que un usuario encuentre una respuesta satisfactoria** en una posición determinada. A diferencia de MRR, tiene en cuenta múltiples niveles de relevancia y la probabilidad de que un usuario deje de buscar después de ver un resultado útil.

* **Fórmula (versión simplificada):**  
  $ERR = \sum_{r=1}^{n} \frac{1}{r} \cdot P(r)$  
  - $P(r)$ es la probabilidad de que el usuario se detenga en la posición $r$ (basada en la relevancia del documento en esa posición).

#### **Explicación Detallada**

ERR modela un comportamiento **más realista del usuario**: si encuentra un documento muy relevante en la primera posición, probablemente no siga mirando el resto. Pero si el documento es poco útil, seguirá bajando.

Esta métrica se basa en la idea de que la relevancia no es binaria (sí/no), sino que puede tener diferentes niveles (por ejemplo: irrelevante, relevante, muy relevante). ERR combina esto con una penalización por posición, similar a NDCG, pero con una interpretación probabilística.

#### **Casos de Uso Comunes**

- **Sistemas con múltiples grados de relevancia** como motores de búsqueda que clasifican resultados por utilidad.
- **Evaluaciones centradas en el usuario**, donde importa no solo qué tan relevante es un documento, sino también cuándo aparece en la lista.
- **Benchmarks avanzados**, como en competiciones de ranking (por ejemplo, TREC o LETOR).


## 🛠️ Ejemplo práctico: cómo medir el rendimiento de tu sistema RAG

### Creación de un entorno de desarrollo

Para crear y gestionar el entorno de Python de este proyecto se utiliza `uv`, una herramienta moderna que combina la gestión de entornos virtuales y la resolución de dependencias de forma rápida y eficiente.

Este enfoque reemplaza el uso tradicional de herramientas como `venv`, `pip` y `virtualenv`, ofreciendo una experiencia más simple y ágil.

ℹ️ Para más detalles sobre cómo instalar y utilizar uv, consulta el archivo [`working-with-uv.md`](../docs/working-with-uv.md)

Una vez instalado `uv`, puedes crear el entorno virtual e instalar todas las dependencias necesarias con un solo comando:

```bash
uv venv && uv sync
```

Este comando creará un entorno virtual en el directorio del proyecto y sincronizará las librerías especificadas en el archivo `pyproject.toml`.

### Evaluando la Recuperación de Información en Sistemas RAG

#### **1. Generación de datos de referencia (Ground Truth)**

Si deseas ver un ejemplo práctico de cómo generar datos de referencia para evaluar un sistema RAG, puedes consultar el archivo [`ground-truth-data.ipynb`](./notebook/ground-truth-data.ipynb).

Este notebook incluye ejemplos de:
- Generación de datos de referencia (ground truth) con ayuda de un LLM.
- Organización de las consultas y documentos relevantes.
- Preparación de los datos para su posterior evaluación.
- Opcionalmente, exportación a un formato binario para su uso en experimentos posteriores.

Este paso es fundamental para contar con un conjunto sólido de datos antes de realizar la indexación.

#### **2. Evaluación de respuestas generadas (Text Evaluation)**

Si deseas ver un ejemplo práctico de cómo evaluar respuestas generadas por un sistema RAG, puedes consultar el archivo [`evaluate-text.ipynb`](./notebook/evaluate-text.ipynb).

Este notebook incluye ejemplos de:
- Evaluación automática de respuestas usando métricas como MRR (Mean Reciprocal Rank).
- Comparación entre diferentes métodos para calcular la métrica.
- Revisión de casos con fallos y aciertos para entender el rendimiento del sistema.
- Preparación de los resultados para visualización o análisis posteriores.

Este paso es clave para medir la efectividad del sistema RAG a partir de los datos de referencia generados previamente.


## 🔗 Lectura recomendada
Recomendado para profundizar en los conceptos clave y ampliar tu comprensión
* [What is Qdrant?](https://qdrant.tech/documentation/overview/)


## ▶️ Videos recomendados
Selección de videos para reforzar visualmente los temas abordados
* [What is RAG? Building Better LLM Systems with Qdrant](https://www.youtube.com/watch?v=rtIyQPJUd_U)


## 📚 Cursos adicionales recomendados
Recursos complementarios para seguir aprendiendo y fortaleciendo tus habilidades.

* [Retrieval Optimization: From Tokenization to Vector Quantization](https://www.deeplearning.ai/short-courses/retrieval-optimization-from-tokenization-to-vector-quantization/?utm_campaign=qdrant-launch&utm_medium=qdrant&utm_source=partner-promo)

---

> 📌 **Nota:** este repositorio complementa el curso **LLM Zoomcamp** de [DataTalks.Club](https://datatalks.club/), y contiene notas, lecturas, videos, ejemplos y recursos adicionales.  
> Para acceder al contenido oficial del curso, visita el [**repositorio principal en GitHub**](https://github.com/DataTalksClub/llm-zoomcamp).
