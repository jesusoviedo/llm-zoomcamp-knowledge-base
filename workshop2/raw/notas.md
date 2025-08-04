### 🎥 **Build Agentic Assistants with OpenAI Function Calling: Part 1**

**Tema:** Creación de sistemas de Generación Aumentada por Recuperación (RAG) más inteligentes y flexibles utilizando un enfoque agéntico y la funcionalidad de "Function Calling" de OpenAI.

**1. Conceptos Fundamentales: RAG Básico**

* **¿Qué es RAG (Retrieval Augmented Generation)?**
    * Es un proceso para responder preguntas utilizando una base de conocimiento externa.
    * **Proceso de 3 pasos clave:**
        1. **Búsqueda (Retrieval):** Se busca información relevante en una base de datos (ej., FAQ) para encontrar el contexto adecuado.
        2. **Construcción del Prompt:** Se crea una instrucción para el modelo que incluye tanto la pregunta del usuario como el contexto encontrado.
            * **Observación:** Se recomienda usar etiquetas como `<context>` y `<question>` para estructurar el prompt.
        3. **Generación de Respuesta (Generation):** Se envía el prompt al modelo de lenguaje (LLM), que utiliza el contexto para formular una respuesta precisa.

* **Limitación Principal del RAG Básico:**
    * El sistema solo puede responder si la información está en su base de conocimiento. Si se le pregunta algo fuera de su contexto, no podrá responder con precisión.

**2. Evolución: El Enfoque del RAG Agéntico**

* **¿Qué es un RAG Agéntico?**
    * Es una versión más avanzada donde el sistema (el "agente") puede tomar decisiones sobre cómo responder.
    * **Decisión clave:** ¿Necesito buscar en la base de datos o puedo responder usando mi conocimiento general?

* **Flujo de trabajo del Agente:**
    1. El usuario hace una pregunta.
    2. El agente analiza la pregunta y decide:
        * **Si es una pregunta general:** Responde directamente.
        * **Si es una pregunta específica del contexto:** Activa la búsqueda en la base de conocimiento y luego responde con la información encontrada.

* **Búsqueda Agéntica (Agentic Search):**
    * El agente puede realizar múltiples búsquedas iterativas para explorar un tema a fondo.
    * Si la primera búsqueda no es suficiente, puede reformular la pregunta y volver a buscar.
    * **Ejemplo práctico:** Ante la pregunta "¿Cómo me va bien en el módulo uno?", el agente puede buscar primero "consejos para el módulo uno", luego hacer una búsqueda más específica sobre "consejos de estudio para Docker y Terraform".

**3. Implementación Avanzada: "Function Calling" (Uso de Herramientas)**

* **El Problema:** Crear prompts manuales para cada posible acción (buscar, responder, añadir datos) se vuelve complejo y difícil de mantener.

* **La Solución: "Function Calling"**
    * Es una funcionalidad de APIs como la de OpenAI que permite describirle al modelo las herramientas que tiene disponibles.
    * En vez de lógica compleja en el prompt, se le dice al modelo: "Tienes una herramienta para buscar en la FAQ llamada `search`".

    * **Proceso:**
        1. **Definición de Herramientas:** Se define cada función disponible (`search`, `add_entry`, etc.) con su nombre, descripción y parámetros requeridos.
        2. **Decisión del Modelo:** El modelo recibe la pregunta del usuario y decide si usar una herramienta y cuál.
        3. **Ejecución:** El código ejecuta la función que el modelo solicitó.
        4. **Retroalimentación:** El resultado se reenvía al modelo para formular la respuesta final.

* **Ventajas Clave:**
    * **Modularidad:** Es fácil añadir nuevas herramientas sin reescribir los prompts.
    * **Flexibilidad:** Se puede ajustar el comportamiento del agente modificando el prompt del sistema.
    * **Mantenimiento:** Se separa la lógica del agente de la definición de sus capacidades, haciendo el código más limpio.

**Observaciones y Conclusiones de la Clase**

* La elección entre un RAG simple o agéntico depende del caso de uso. Para una base de conocimiento cerrada, el RAG simple puede ser suficiente.
* El enfoque agéntico con "Function Calling" es muy poderoso para asistentes conversacionales complejos.
* Para entornos en producción, se deben considerar temas como persistencia de datos (ej. uso de Qdrant) y control de entradas inapropiadas (guardrails).

### 🎥 **Build Agentic Assistants with OpenAI Function Calling: Part 2**

**1. Introducción y Objetivos del Taller**

* **Continuación de la Parte 1:** Este taller es la segunda parte, enfocado en profundizar en el concepto de **Llamadas a Funciones (Function Calling)** de OpenAI.
* **Objetivo Principal:** Explicar en detalle la implementación de las llamadas a funciones, el bucle de ejecución y la refactorización del código a clases para una mejor organización.
* **Recurso Clave:** Se introduce la librería `toy AI kit`, que consolida el código de los talleres para que sea reutilizable y fácil de entender. Se puede instalar vía `pip`.

**2. Concepto Clave: ¿Qué es "Function Calling"?**

* **Definición:** Es la capacidad de un modelo de lenguaje (LLM) para decidir de forma autónoma si necesita invocar una función o herramienta externa para responder a una pregunta.
* **Problema que Resuelve:** Un LLM como ChatGPT no tiene conocimiento específico sobre temas privados o muy recientes (ej. las FAQs de un curso específico).
* **Solución:** Se le "enseña" al modelo qué herramientas tiene a su disposición.
    * **Implementación:** Se le proporciona al LLM una **descripción de la función** (qué hace, qué parámetros necesita) junto con la pregunta del usuario.
    * **Decisión del Modelo:** Basado en la pregunta, el LLM decide si debe usar la herramienta. Si lo hace, no responde directamente, sino que devuelve una instrucción para llamar a la función con los argumentos que considera necesarios.

**3. El Bucle de Ejecución del Agente**

* Este es el "cerebro" del asistente y funciona en dos niveles:
    * **Bucle Exterior (Interacción con el usuario):**
        1. Espera la pregunta del usuario (`input("User: ")`).
        2. Inicia el bucle interior para procesar la pregunta.
        3. Una vez que el bucle interior termina, muestra la respuesta final y espera la siguiente pregunta.
    * **Bucle Interior (Llamadas a funciones):**
        1. Recibe la pregunta y la envía al LLM.
        2. **Revisa la respuesta del LLM:**
            * Si el LLM pide llamar a una función (`function_call`), el código ejecuta esa función, recoge el resultado y vuelve a llamar al LLM con esa nueva información.
            * Este proceso se repite hasta que el LLM considera que tiene suficiente información.
        3. **Fin del Bucle:** Cuando el LLM responde con un mensaje de texto normal (sin pedir más funciones), el bucle interior termina y la respuesta se pasa al usuario.

* **Observación Importante:** Un LLM puede ser lo suficientemente avanzado como para explicar su razonamiento en texto y, en la misma respuesta, solicitar una llamada a función.

**4. Refactorización y Organización del Código (Buenas Prácticas)**

* El código inicial, aunque funcional, puede volverse desordenado. Se propone una estructura basada en clases para hacerlo más limpio, mantenible y escalable.

* **Clase `Tools`:**
    * **Responsabilidad:** Gestionar todas las herramientas disponibles.
    * Registra las funciones que el agente puede usar.
    * Genera automáticamente las descripciones que necesita la API de OpenAI a partir de los *docstrings* y *type hints* del código Python (usando la librería `inspect`).

* **Clase `IPythonChatInterface`:**
    * **Responsabilidad:** Manejar todo lo relacionado con la interfaz de usuario (mostrar texto, obtener input, formatear salidas).
    * Utiliza Markdown y HTML para que la conversación se vea más bonita y ordenada en un notebook, con secciones colapsables (`<details>`) para no saturar la pantalla.

* **Clase `ChatAssistant`:**
    * **Responsabilidad:** Es el orquestador principal. Contiene la lógica del bucle de ejecución y une la interfaz (`IPythonChatInterface`) con las herramientas (`Tools`).

**5. Conclusiones y Próximos Pasos**

* **Propósito Educativo:** El `toy AI kit` está diseñado para aprender los fundamentos. No es para sistemas en producción.
* **Alternativas para Producción:** Para proyectos reales, se recomiendan librerías más robustas como `Pydantic AI` o el `OpenAI Agent SDK`, aunque la lógica subyacente es muy similar a la vista en el taller.