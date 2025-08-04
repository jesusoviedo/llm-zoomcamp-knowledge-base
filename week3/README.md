# Semana 3 - LLM Zoomcamp

Este documento recopila mis apuntes y recursos para la **Semana 3** del curso LLM Zoomcamp.

## 📝 Notas de la teoría

### Importancia de la Evaluación

Es fundamental evaluar los resultados de búsqueda para optimizar cómo se almacenan y recuperan los datos en un sistema RAG (Retrieval-Augmented Generation). Sin una evaluación adecuada, es difícil saber si el sistema está devolviendo resultados útiles y relevantes. El rendimiento ideal siempre depende de los datos disponibles y los requisitos específicos del caso de uso.

El objetivo es medir de forma objetiva qué tan bueno es un sistema de búsqueda. En lugar de confiar en la intuición, usamos métricas para cuantificar el rendimiento. Esto nos permite comparar diferentes sistemas (como Elasticsearch o Qdrant vs. otro motor de búsqueda) o diferentes configuraciones del mismo sistema.


### Datos de Referencia (Ground Truth)

Para evaluar un sistema de recuperación, se necesita un conjunto de datos de referencia (también conocido como *ground truth* o *gold standard data*). Este conjunto contiene consultas junto con los documentos relevantes para cada una.

#### **Necesidad de un "Ground Truth"**
Es indispensable contar con este conjunto para evaluar de manera efectiva el rendimiento del sistema. Cada entrada debería vincular una pregunta con el documento que contiene la respuesta correcta.

#### **Estructura del Conjunto de Datos**
Idealmente, el conjunto contiene miles de preguntas, y para cada una se identifican los documentos relevantes. En algunos casos, como simplificación, se asume que existe **un solo documento relevante por pregunta**.

#### **Métodos para Crear Ground Truth**

- **Anotación Humana**: Especialistas etiquetan manualmente las preguntas con sus documentos relevantes. Es el método más preciso, aunque costoso y lento.
- **Observación del Usuario**: Se analiza el comportamiento real de los usuarios. Puede ser evaluado por humanos o por LLMs.
- **Generación Automática con LLM**: Usar un modelo como GPT-4 para generar preguntas y asociarlas automáticamente a documentos de referencia (por ejemplo, desde un conjunto de preguntas frecuentes).

#### **Creación de un ID de Documento Único**
Para asegurar trazabilidad, se genera un hash (MD5) con los campos del documento (curso, pregunta, texto), lo que garantiza que el ID cambie solo si el contenido cambia.

#### **Ejemplo de Implementación**
- Se carga un conjunto de documentos.
- Se asigna un ID único a cada uno.
- Se diseña un prompt detallado que instruye al LLM a actuar como un estudiante y generar cinco preguntas variadas por FAQ.
- El resultado es almacenado como un DataFrame y luego exportado a CSV.

#### **Optimización de la Búsqueda**

Varios parámetros de búsqueda pueden ajustarse para mejorar los resultados obtenidos. Algunos ejemplos incluyen:

- Tipo de búsqueda: densa, híbrida, BM25.
- Campos del documento que se consultan: título, cuerpo, metadatos, etc.
- Uso de boosting para priorizar campos como `question`.
- Filtros por categoría, curso o tipo de contenido.

La evaluación es la herramienta clave para identificar qué configuración produce el mejor rendimiento en función de las necesidades del usuario.

#### **Métricas de Ranking Comunes**

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

### Evaluación y Monitoreo

Aunque los sistemas RAG utilizan modelos de lenguaje como parte del proceso, los LLMs también pueden usarse **de manera independiente** en tareas como generación de texto, clasificación o razonamiento. Por eso, es importante entender cómo evaluarlos y monitorearlos en distintos contextos.

#### **Evaluación de LLMs: ¿Qué se mide y cómo?**

- **Calidad del contenido generado**  
  Se busca responder: ¿es útil, coherente, relevante y veraz lo que produce el modelo? Algunas formas comunes de evaluar esto son:

  - **Human Evaluation**  
    Personas humanas califican las respuestas del modelo en dimensiones como claridad, utilidad, precisión factual o tono.

  - **Automatic Metrics**  
    Herramientas que cuantifican la calidad de las respuestas:
    - `BLEU`, `ROUGE`, `METEOR`: comparan respuestas generadas con referencias.
    - `BERTScore`: mide similitud semántica entre textos.
    - **Similitud Embedding (coseno)**: se representa el texto en vectores y se mide su cercanía matemática.

  - **LLM-as-a-Judge**  
    Otro LLM actúa como evaluador. Se le da una instrucción del tipo:
    "Dada esta pregunta y esta respuesta generada, ¿qué tan útil y correcta es la respuesta?"

  - **Pruebas A/B**  
    Se comparan dos versiones del modelo (por ejemplo, una con un nuevo prompt o ajuste de hiperparámetros) con usuarios reales. A cada grupo se le muestra una versión diferente, y se recopilan métricas como satisfacción, tasa de clics o preferencia explícita entre respuestas.


- **Evaluación de comportamiento no deseado**  
  Los LLMs también se evalúan para detectar errores como:
  - **Alucinaciones**: respuestas que suenan correctas pero son falsas.
  - **Bias o toxicidad**: lenguaje ofensivo o sesgado.
  - **Seguridad**: si el modelo responde a preguntas dañinas o peligrosas.

#### **Monitoreo de LLMs en Producción**

Una vez que el LLM está en uso (en apps, asistentes, bots, etc.), el monitoreo continuo es clave para mantener su calidad y seguridad.

- **Métricas técnicas**  
  - Latencia de respuesta  
  - Tasa de error o caídas del sistema  
  - Costo por consulta (tokens, tiempo de cómputo)

- **Métricas de uso y comportamiento**  
  - Número de usuarios activos  
  - Tasa de éxito en tareas (ejemplo: generación correcta de reportes, respuestas útiles)  
  - Detección de respuestas problemáticas o alucinaciones en tiempo real

- **Retroalimentación del usuario**  
  - Pulgar arriba/abajo  
  - Comentarios abiertos  
  - NPS (Net Promoter Score) sobre la experiencia con el modelo

#### **Importancia de la Evaluación y el Monitoreo Combinados**

Un buen LLM no solo debe pasar pruebas antes de salir a producción, sino también demostrar que **mantiene su rendimiento bajo condiciones reales** y con usuarios diversos. La combinación de evaluación sistemática y monitoreo activo permite:

- Detectar degradaciones en la calidad.
- Responder rápidamente a incidentes de seguridad.
- Identificar oportunidades para mejorar el modelo o ajustar prompts.

Evaluar y monitorear LLMs es un proceso continuo, que combina **pruebas offline** (en entornos controlados antes del despliegue, como benchmarks o datasets con ground truth), **pruebas online** (con usuarios reales y métricas en tiempo real), **recolección de datos de uso** y **herramientas automáticas** (como evaluadores automáticos o LLM-as-a-Judge), para garantizar calidad, seguridad y valor para el usuario final.

#### **Evaluación Offline de Sistemas RAG**

La **evaluación offline** en sistemas de Recuperación Aumentada por Generación (RAG) es esencial para validar la **calidad** de las respuestas **antes del despliegue en producción**. Este proceso permite comparar modelos, ajustar configuraciones y optimizar el balance entre **precisión, velocidad y costo**.

**Componentes de un sistema RAG**

Un sistema RAG consta de tres componentes clave:

1. **Búsqueda (Retrieval):**  
   Recupera documentos relevantes utilizando búsquedas semánticas en bases vectoriales como **Qdrant**, **Elasticsearch** o **FAISS**.

2. **Construcción del prompt:**  
   Ensambla la consulta del usuario con los documentos recuperados, generando una entrada coherente para el modelo.

3. **Generación con LLM:**  
   El modelo de lenguaje procesa el prompt y genera una respuesta final basada en el contexto aportado.

**Proceso de evaluación**

La evaluación offline simula interacciones antes de poner el sistema frente a usuarios reales. Utiliza **datasets de referencia** para medir el desempeño con métricas cuantitativas. A continuación se explica un proceso paso a paso:

1. **Indexación de datos:**  
   Los documentos son convertidos en vectores con modelos como `multi-qa-MiniLM-L6-cos-v1`.

2. **Generación de preguntas sintéticas (opcional):**  
   A partir de las respuestas ideales (ground truth), un LLM genera una pregunta coherente.

3. **Obtención de respuesta generada:**  
   Se evalúa cómo responde el modelo cuando recibe esa pregunta.

4. **Comparación entre respuestas (A vs A’):**  
   Se mide cuán parecida es la respuesta generada (A') a la ideal (A), usando métricas como:

   - **Similitud del coseno:**  
     Evalúa la cercanía semántica entre vectores de texto.  
     - `1.0`: muy similares  
     - `0.0`: completamente diferentes

   - **Otras métricas complementarias:**  
     - `Exact Match`  
     - `F1 Score`  
     - `BLEU`, `ROUGE` (útiles cuando no se trabaja con embeddings)

**Comparativa de modelos**

La elección del modelo LLM no debe hacerse de forma arbitraria. Existen múltiples opciones disponibles, y cada una presenta ventajas y desventajas en términos de **costo**, **tiempo de procesamiento** y **calidad de resultados**. Evaluar estos factores permite seleccionar el modelo más adecuado según el contexto y los objetivos del sistema RAG.

**Caso Práctico: Comparación de Modelos LLM de OpenAI**

Se compararon tres modelos populares para ver cuál ofrece mejor relación **calidad / costo / tiempo**:

| Modelo         | Similitud promedio | Costo aprox. por lote | Tiempo de procesamiento |
|----------------|--------------------|------------------------|--------------------------|
| **GPT-4o Mini** | 0.683              | $0.10                  | 6.5 minutos (con multithreading) |
| **GPT-4**       | 0.679              | $10.00                 | 3 horas                  |
| **GPT-3.5 Turbo**| 0.657              | $0.79                  | 6.5 minutos              |

**Observaciones claves:**

- Las puntuaciones de calidad son **muy similares**.
- **GPT-4o Mini** destaca por ser **más rápido y económico**, aunque con restricciones de **rate limit**.
- Con técnicas como `ThreadPoolExecutor` se puede acelerar el proceso sin comprometer calidad.

**Visualización y Métricas**

Se recomienda visualizar los resultados con herramientas como:

- `sns.histplot()` para histogramas de similitud
- `sns.kdeplot()` para estimaciones de densidad
- `sns.ecdfplot()` para distribución acumulada

**Herramientas útiles**

- **RAGAS**: Evalúa múltiples dimensiones (fidelidad, relevancia, recuerdo)
- **LangChain Evaluation**: Framework flexible para comparar cadenas y prompts
- **Pandas**: Gestión estructurada de resultados
- **tqdm**: Visualización del progreso
- **PromptLayer** y **Evidently**: Para trazabilidad y análisis en producción

La evaluación offline no solo permite elegir el mejor modelo, sino también tomar decisiones informadas que optimicen el rendimiento general del sistema RAG.

> **Evaluar no es un paso único, es un proceso continuo.**

#### **LLM como Juez en la Evaluación Offline y Online**

Cuando no se dispone de una respuesta ideal (ground truth), o se busca un enfoque más cualitativo, puede emplearse la técnica **LLM-as-a-Judge**, donde otro modelo LLM evalúa las respuestas generadas.

**Escenario 1: Evaluación Offline (con ground truth)**

- **Contexto:** Evaluación previa al despliegue, en entorno controlado.
- **Datos disponibles para el LLM juez:**
  - Pregunta del usuario.
  - Respuesta generada por el sistema.
  - Respuesta ideal (ground truth).
- **Tarea del juez:** Clasificar la respuesta generada como `RELEVANTE`, `PARCIALMENTE RELEVANTE` o `NO RELEVANTE`, explicando su razonamiento.

**Escenario 2: Evaluación Online (sin ground truth)**

- **Contexto:** Evaluación en producción, con datos en tiempo real.
- **Datos disponibles para el LLM juez:**
  - Pregunta del usuario.
  - Respuesta generada por el sistema.
- **Tarea del juez:** Evaluar si la respuesta es coherente y útil, sin referencia directa. Ideal para monitoreo continuo o testing en vivo.

**Ventaja:** Esta técnica permite realizar evaluaciones más subjetivas o de criterio experto, incluso cuando no se dispone de respuestas ideales.

**Diseño de Prompts para el Juez LLM**

Para asegurar una evaluación consistente y útil, el LLM juez necesita instrucciones claras. Se recomienda usar prompts como:

- **Prompt para Evaluación Offline:**  
  `"Analiza la respuesta generada en relación con la respuesta original. Clasifícala como RELEVANTE, PARCIALMENTE RELEVANTE o NO RELEVANTE. Justifica tu elección."`

- **Prompt para Evaluación Online:**  
  `"Evalúa si la respuesta proporcionada es relevante para la pregunta. Clasifícala como RELEVANTE, PARCIALMENTE RELEVANTE o NO RELEVANTE. Justifica tu decisión."`

**Consejo técnico:** Estructura las respuestas del juez en formato **JSON** para facilitar su procesamiento automático.

**Lecciones Clave y Consideraciones Técnicas**

- **Las respuestas incorrectas son oro:** Las clasificaciones como "NO RELEVANTE" ayudan a detectar fallos críticos en el sistema RAG (por ejemplo, recuperación errónea o prompts mal construidos).
- **Identificación de cuellos de botella:** El análisis cualitativo permite detectar si el problema radica en la búsqueda, construcción del prompt o generación del LLM.
- **Monitoreo continuo:** En entornos productivos, el LLM juez permite mantener control de calidad sin intervención humana directa.

### Entendiendo las Métricas

Evaluar un sistema de recuperación o recomendación no solo implica observar si los resultados son buenos, sino también **cuán buenos**, **cuán rápidos** y **cuán completos** son. Para eso, se utilizan diversas métricas, cada una con su propia lógica y aplicaciones. A continuación, exploramos las más relevantes.

#### Precisión en k (P@k)

Mide la proporción de documentos relevantes dentro de los primeros **k** resultados.

* **Fórmula:**  
  $P@k = \frac{\text{Número de documentos relevantes en los primeros k resultados}}{k}$

**Explicación Detallada**

Esta es la métrica más intuitiva. Imagina que buscas algo en Google y solo miras los primeros 10 resultados. La **Precisión en 10 (P@10)** te dice qué porcentaje de esos 10 enlaces fue realmente útil. No le importa si había más resultados buenos en la página 2; solo se enfoca en la calidad de la primera "vitrina" de resultados que ve el usuario.

**Casos de Uso Comunes**

- **Motores de búsqueda web (Google, Bing):** La mayoría de los usuarios no pasa de la primera página.
- **Búsqueda en e-commerce (Amazon):** Si buscas "zapatillas rojas", quieres ver zapatillas rojas inmediatamente.
- **Sistemas de recomendación (Netflix, Spotify):** Es crucial que las primeras recomendaciones sean atractivas.

#### Recall (Exhaustividad o Sensibilidad)

Mide la proporción de documentos relevantes que el sistema logró encontrar de entre el **total** de documentos relevantes que existen.

* **Fórmula:**  
  $Recall = \frac{\text{Número de documentos relevantes recuperados}}{\text{Número total de documentos relevantes}}$

**Explicación Detallada**

El Recall se enfoca en la **cobertura**. No le importa si los resultados buenos están al principio o al final, solo quiere saber si el sistema fue capaz de encontrarlos todos. El objetivo es minimizar los "falsos negativos", es decir, no dejar fuera nada importante.

**Casos de Uso Comunes**

- **Búsquedas legales o de patentes:** Es crítico encontrar todos los documentos pertinentes.
- **Diagnóstico médico:** Se requiere considerar todas las posibilidades.
- **Detección de fraude o amenazas:** Es preferible detectar de más (falsos positivos) que pasar por alto algo grave.

#### Puntuación F1 (F1 Score)

Es la media armónica de la Precisión y el Recall. Busca un equilibrio entre ambos.

* **Fórmula:**  
  $F1 = 2 \cdot \frac{Precision \cdot Recall}{Precision + Recall}$

**Explicación Detallada**

La puntuación F1 es el gran pacificador entre Precisión y Recall. Es imposible obtener un F1 alto si una de las dos métricas es muy baja. La media armónica penaliza los extremos, obligando al sistema a ser balanceado.

**Casos de Uso Comunes**

- **Clasificación de texto y análisis de sentimiento.**
- **Evaluación general de un sistema:** Proporciona una única cifra para resumir rendimiento.


#### Rango Recíproco Medio (Mean Reciprocal Rank - MRR)

Evalúa la posición en el ranking del **primer** documento relevante encontrado.

* **Fórmula:**  
  $MRR = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{rank_i}$  
  - $|Q|$ es el número total de búsquedas.  
  - $rank_i$ es la posición del primer resultado correcto para la búsqueda $i$.

**Explicación Detallada**

¿El sistema encontró una buena respuesta rápido? Si la respuesta correcta aparece primero, el puntaje es 1. En la segunda posición, 1/2. En la tercera, 1/3, y así sucesivamente. El MRR promedia esta eficiencia a lo largo de muchas búsquedas.

**Casos de Uso Comunes**

- **Sistemas de preguntas y respuestas (FAQs).**
- **Chatbots de soporte.**
- **Autocompletado o resultados tipo "Voy a tener suerte".**

#### Ganancia Cumulativa Descontada Normalizada (NDCG)

Mide la utilidad (o ganancia) de un documento según su posición en la lista de resultados.

* **Fórmula:**  
  $NDCG = \frac{DCG}{IDCG}$  
  - **DCG:** suma la relevancia de cada documento, pero “descuenta” su valor cuanto más abajo esté.  
  - **IDCG:** es el DCG ideal (orden perfecto).

**Explicación Detallada**

NDCG es una de las métricas más completas:
1. **Reconoce niveles de relevancia.**
2. **Penaliza posiciones bajas.**

El resultado normalizado varía entre 0 y 1, donde 1 representa un ranking perfecto.

**Casos de Uso Comunes**

- **Motores de búsqueda y sistemas de recomendación.**
- **Comparación de modelos en competiciones y benchmarks.**

#### Precisión Media Promedio (Mean Average Precision - MAP)

Calcula la precisión promedio para cada búsqueda y luego promedia estos valores entre todas.

* **Fórmula:**  
  $MAP = \frac{1}{|Q|} \sum_{q \in Q} \text{Average Precision(q)}$

**Explicación Detallada**

El MAP recompensa que los documentos relevantes estén lo más arriba posible en los resultados. Aunque no diferencia grados de relevancia, mide bien el orden general de los aciertos.

**Casos de Uso Comunes**

- **Búsqueda de imágenes o documentos.**
- **Benchmarks académicos en recuperación de información.**

#### Tasa de Aciertos (Hit Rate - HR)

Mide la proporción de búsquedas donde se recuperó **al menos un** documento relevante en el top **k**.

* **Fórmula:**  
  $HR@k = \frac{\text{Número de búsquedas con al menos un acierto en el top k}}{|Q|}$

**Explicación Detallada**

Es una métrica de “todo o nada”: ¿hubo al menos un resultado útil en el top **k**? No se preocupa por cuántos, solo por si hubo al menos uno.

**Casos de Uso Comunes**

- **Sistemas de recomendación.**
- **Validación de sistemas simples de recuperación.**


#### Rango Recíproco Esperado (Expected Reciprocal Rank - ERR)

Evalúa la calidad del ranking considerando **la probabilidad de que un usuario encuentre una respuesta satisfactoria** en una posición determinada. A diferencia de MRR, tiene en cuenta múltiples niveles de relevancia y la probabilidad de que un usuario deje de buscar después de ver un resultado útil.

* **Fórmula (versión simplificada):**  
  $ERR = \sum_{r=1}^{n} \frac{1}{r} \cdot P(r)$  
  - $P(r)$ es la probabilidad de que el usuario se detenga en la posición $r$ (basada en la relevancia del documento en esa posición).

**Explicación Detallada**

ERR modela un comportamiento **más realista del usuario**: si encuentra un documento muy relevante en la primera posición, probablemente no siga mirando el resto. Pero si el documento es poco útil, seguirá bajando.

Esta métrica se basa en la idea de que la relevancia no es binaria (sí/no), sino que puede tener diferentes niveles (por ejemplo: irrelevante, relevante, muy relevante). ERR combina esto con una penalización por posición, similar a NDCG, pero con una interpretación probabilística.

**Casos de Uso Comunes**

- **Sistemas con múltiples grados de relevancia** como motores de búsqueda que clasifican resultados por utilidad.
- **Evaluaciones centradas en el usuario**, donde importa no solo qué tan relevante es un documento, sino también cuándo aparece en la lista.
- **Benchmarks avanzados**, como en competiciones de ranking (por ejemplo, TREC o LETOR).

---

Cuando se quiere evaluar automáticamente la calidad de textos generados por un modelo, es común comparar esos textos con respuestas de referencia utilizando métricas específicas. A continuación, se explican algunas de las más utilizadas.

#### BLEU (Bilingual Evaluation Understudy)

Evalúa la calidad de un texto generado comparando **n-gramas coincidentes** (secuencias de palabras) con una o más referencias.

* **Idea clave:** Si el modelo usa muchas frases similares a las de la referencia, la calidad es alta.
* **Penalización por longitud:** BLEU incluye una penalización si el texto generado es mucho más corto que la referencia.

**Fórmula (simplificada):**  
`BLEU = BP × exp(∑ wₙ × log(pₙ))`  
- `BP`: *brevity penalty*  
- `pₙ`: precisión de n-gramas de orden `n`  
- `wₙ`: peso asignado a cada orden (por ejemplo, 0.25 si se usan 4-gramas)

**Casos de Uso Comunes**  
- Traducción automática  
- Generación de texto donde se espera que el output se acerque mucho a una referencia  

#### ROUGE (Recall-Oriented Understudy for Gisting Evaluation)

Mide la **superposición de n-gramas o frases** entre la salida del modelo y una o varias referencias.

* **Variantes comunes:**
  - `ROUGE-1`: superposición de palabras individuales
  - `ROUGE-2`: superposición de bigramas (pares de palabras)
  - `ROUGE-L`: longitud de la subsecuencia común más larga (*Longest Common Subsequence*)

**Enfoque en recall:** A diferencia de BLEU (que prioriza precisión), ROUGE está orientado a capturar cuánta información relevante se ha recuperado.

**Casos de Uso Comunes**  
- Evaluación de resúmenes automáticos  
- Tareas donde es más importante **capturar lo esencial** del contenido  

#### METEOR (Metric for Evaluation of Translation with Explicit ORdering)

Mejora algunas limitaciones de BLEU y ROUGE utilizando:
- Coincidencias por sinónimos y variantes morfológicas
- Penalizaciones por orden incorrecto
- Evaluación a nivel de frase

**Ventajas:**  
- Mayor correlación con evaluaciones humanas  
- Soporta flexibilidad lingüística  

**Casos de Uso Comunes**  
- Traducción automática  
- Generación de lenguaje natural en contextos sensibles a la semántica  

#### BERTScore

Evalúa la **similitud semántica** entre el texto generado y la referencia utilizando **representaciones vectoriales obtenidas con BERT** (o modelos similares).

* **Cómo funciona:**
  - Convierte cada palabra en un vector (*embedding*)
  - Compara los vectores del texto generado con los de la referencia
  - Usa métricas de similitud como el coseno

**Ventajas:**  
- Capta mejor el *significado*, no solo la coincidencia superficial de palabras  
- Funciona bien en tareas donde el lenguaje puede ser diverso pero el mensaje debe mantenerse  

**Casos de Uso Comunes**  
- Resumen automático  
- Parafraseo  
- Generación abierta de texto donde puede haber muchas respuestas correctas  

Estas métricas ofrecen una primera aproximación rápida y cuantitativa a la calidad del texto generado. Sin embargo, en muchos casos **es necesario complementarlas con evaluaciones humanas o LLM-as-a-Judge** para obtener una visión completa.



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

* [Evaluating RAG Architectures on Benchmark Tasks](https://langchain-ai.github.io/langchain-benchmarks/notebooks/retrieval/comparing_techniques.html)
* [Best Practices for LLM Evaluation of RAG Applications](https://www.databricks.com/blog/LLM-auto-eval-best-practices-RAG)
* [Awesome RAG Evaluation](https://github.com/YHPeter/Awesome-RAG-Evaluation?tab=readme-ov-file)
* [An Overview on RAG Evaluation](https://weaviate.io/blog/rag-evaluation)
* [La guía definitiva para evaluar los componentes del sistema RAG: lo que necesitas saber](https://myscale.com/blog/es/ultimate-guide-to-evaluate-rag-system/)
* [Evaluadores de generación aumentada por recuperación (RAG)](https://learn.microsoft.com/es-es/azure/ai-foundry/concepts/evaluation-evaluators/rag-evaluators)
* [Let's talk about LLM evaluation](https://huggingface.co/blog/clefourrier/llm-evaluation)
* [RAG Evaluation](https://huggingface.co/learn/cookbook/en/rag_evaluation)
* [RAG Evaluation: Don’t let customers tell you first](https://www.pinecone.io/learn/series/vector-databases-in-production-for-busy-engineers/rag-evaluation/)
* [LLM Evaluation Metrics: The Ultimate LLM Evaluation Guide](https://www.confident-ai.com/blog/llm-evaluation-metrics-everything-you-need-for-llm-evaluation#:~:text=1,is%20able%20to%20call%20the)
* [Evaluating model performance](https://platform.openai.com/docs/guides/evals)
* [Evaluación de LLMs: Principales benchmarks y cómo entenderlos](https://www.nerds.ai/blog/evaluacion-de-llms-principales-benchmarks-y-como-entenderlos)
* [Ragas core Concepts](https://docs.ragas.io/en/stable/concepts/)
* [SentenceTransformers Documentation](https://sbert.net/)
* [SentenceTransformers Quickstart](https://sbert.net/docs/quickstart.html)
* [SentenceTransformers Pretrained Models](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html)
* [LLM evaluation: a beginner's guide](https://www.evidentlyai.com/llm-guide/llm-evaluation)
* [La Arquitectura de la Confianza: Una Guía para la Evaluación de Sistemas de IA, LLM y RAG](https://medium.com/@j92riquelme/la-arquitectura-de-la-confianza-una-guia-para-la-evaluacion-de-sistemas-de-ia-be5be4aed808)


## ▶️ Videos recomendados
Selección de videos para reforzar visualmente los temas abordados

* [LLM evaluation for builders - Course announcement](https://www.youtube.com/watch?v=jQgI8tTkWQU&list=PL9omX6impEuNTr0KGLChHwhvN-q3ZF12d)
* [Welcome to the LLM evaluation course](https://www.youtube.com/watch?v=rHs0sP7b5fM&list=PL9omX6impEuMgDFCK_NleIB0sMzKs2boI)


## 📚 Cursos adicionales recomendados
Recursos complementarios para seguir aprendiendo y fortaleciendo tus habilidades.

* [Ragas tutorials](https://docs.ragas.io/en/stable/getstarted/)
* [LLM apps: Evaluation](https://wandb.ai/site/courses/evals/?utm_source=chatgpt.com)
* [Building and Evaluating Advanced RAG Applications](https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/?utm_source=chatgpt.com)
* [Evaluación de modelos de lenguaje con Azure Databricks](https://learn.microsoft.com/es-es/training/modules/evaluate-language-models-azure-databricks/?utm_source=chatgpt.com)

---

> 📌 **Nota:** este repositorio complementa el curso **LLM Zoomcamp** de [DataTalks.Club](https://datatalks.club/), y contiene notas, lecturas, videos, ejemplos y recursos adicionales.  
> Para acceder al contenido oficial del curso, visita el [**repositorio principal en GitHub**](https://github.com/DataTalksClub/llm-zoomcamp).
