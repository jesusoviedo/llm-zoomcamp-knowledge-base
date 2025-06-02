# Uso de `uv` en Proyectos Python
`uv` es una herramienta rápida y moderna para gestionar entornos virtuales y dependencias en proyectos Python. Esta guía cubre cómo instalar `uv`, iniciar un proyecto, agregar/eliminar dependencias, y compartir tu entorno con otras personas.

> ⚙️ Para más detalles, consulta la [documentación oficial de uv](https://docs.astral.sh/uv/).

## Instalación de `uv`
### Usando pip
```bash
pip install uv
```

### En sistemas Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Inicializar un Proyecto con `uv`
### Si no existe una carpeta de proyecto:
```bash
uv init hello-world
cd hello-world
```

Esto crea un entorno virtual `.venv`, un archivo `pyproject.toml` y un `uv.lock`.

### Si ya existe una carpeta con archivos:
```bash
mkdir hello-world
cd hello-world
uv init
```

Esto detecta dependencias existentes y genera los archivos necesarios.

## Agregar y Eliminar Dependencias
### Agregar
```bash
uv add requests
uv add pandas matplotlib
```

### Eliminar
```bash
uv remove matplotlib
```

## Agregar Dependencias Opcionales y Grupos de Dependencias

Puedes organizar tus dependencias en grupos opcionales (por ejemplo: "dev", "docs") para tener un entorno más flexible.

### Agregar un grupo de desarrollo:
```bash
uv add --group dev black pre-commit
```

Esto agregará `black` y `pre-commit` al grupo de desarrollo. Luego podrás instalar solo ese grupo si lo deseas:

```bash
uv sync --group dev
```

### Agregar una dependencia como opcional:
```bash
uv add --optional rich
```

### Instalar todos los grupos:
```bash
uv sync --all
```

## Actualizar Dependencias
```bash
uv upgrade
```

Para actualizar paquetes específicos:
```bash
uv upgrade pandas
```

## Ejecutar scripts Python
Una vez que tu entorno virtual esté configurado, puedes ejecutar tus scripts de Python desde la terminal activando el entorno:

```bash
source .venv/bin/activate  # En Linux/macOS
# o
.venv\Scripts\activate     # En Windows
```

Luego, puedes correr tus scripts de la forma habitual:

```bash
python script.py
```

Alternativamente, puedes ejecutar scripts sin activar manualmente el entorno si usas el comando uv venv run:

```bash
uv run python script.py
```

## Compartir el Proyecto
Agrega los siguientes archivos al control de versiones (`git`):
```bash
git add pyproject.toml uv.lock
```

Otros usuarios solo necesitan ejecutar:
```bash
uv venv && uv sync
```

Esto crea el entorno virtual e instala exactamente las versiones bloqueadas en `uv.lock`.

## Herramientas adicionales incluidas en `uv`
* `uv pip`: Un reemplazo más rápido para `pip`, se usa internamente en `uv add/remove`.
* `uv venv`: Administra entornos virtuales (crear, eliminar).
* `uv sync`: Instala dependencias según `uv.lock`, asegurando entornos reproducibles.
* `uv run`: Ejecuta comandos dentro del entorno virtual.
* `uv upgrade`: Actualiza dependencias.

## Créditos

Basado en la [documentación oficial de uv](https://docs.astral.sh/uv/) y el [tutorial de DataCamp](https://www.datacamp.com/es/tutorial/python-uv).