---
name: notebook-integration
description: >
  Integración con Jupyter notebooks: ejecución, creación y exportación de celdas.
  Trigger: Cuando trabajás con Jupyter, .ipynb, notebooks, o necesitás ejecutar código en celdas.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "2.0"
  model_tier: T2-fast
---

# Skill: notebook-integration

## Para qué sirve

Trabajar con notebooks Jupyter de forma programática: crearlos desde código, modificarlos, ejecutarlos sin abrir el navegador, y exportarlos a otros formatos. Los notebooks .ipynb son archivos JSON — podés leerlos, escribirlos y manipularlos como cualquier otro formato estructurado.

## Trigger (cuándo cargar esta skill)

- Necesitás crear un notebook automáticamente desde código
- Querés ejecutar notebooks en batch (por ejemplo, uno por cliente)
- Tenés que exportar notebooks a script Python o HTML
- Querés modificar celdas de un notebook existente sin abrirlo

## Workflow paso a paso

1. **Identificá qué necesitás**: ¿crear, modificar, ejecutar, o exportar?
2. **Usá `nbformat` para crear/modificar**: es la biblioteca oficial de Jupyter para manipular .ipynb
3. **Usá `nbconvert` para ejecutar/exportar**: corre desde terminal y también desde Python con `subprocess`
4. **Para ejecución parametrizada**: usá `papermill` — te deja pasar parámetros al notebook como si fuera una función
5. **Para producción**: convertí notebooks a scripts con `nbconvert --to script` antes de mandarlos a un pipeline

## Patrones esenciales

### 1. Leer y explorar notebooks

Los notebooks son JSON. Con `nbformat` los abrís y ves qué tienen adentro: tipo de celda, código, outputs, metadata.

```python
import nbformat

# Leer notebook
with open('analisis.ipynb', 'r') as f:
    nb = nbformat.read(f, as_version=4)

# Explorar celdas
for i, cell in enumerate(nb.cells):
    tipo = cell.cell_type       # 'code' o 'markdown'
    source = cell.source[:80]   # primeras líneas
    outputs = len(cell.outputs) if cell.cell_type == 'code' else '-'
    print(f"#{i} [{tipo}] {source}... | outputs: {outputs}")
```

### 2. Crear notebook desde código

Ideal para generar reportes automatizados: creás un notebook con markdown y código, lo ejecutás, y obtenés un análisis completo.

```python
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell

nb = new_notebook()
nb.metadata['kernelspec'] = {
    'display_name': 'Python 3',
    'language': 'python',
    'name': 'python3'
}

nb.cells = [
    new_markdown_cell("# Reporte Automático\n\nGenerado el 2024-01-15"),
    new_code_cell("import pandas as pd\nimport matplotlib.pyplot as plt"),
    new_code_cell("df = pd.read_csv('datos.csv')\ndf.head()"),
    new_code_cell("df.describe()"),
    new_code_cell("df.plot(kind='bar', y='monto')\nplt.savefig('reporte.png')"),
]

with open('reporte.ipynb', 'w') as f:
    nbformat.write(nb, f)
```

### 3. Ejecutar notebooks desde terminal

`nbconvert --execute` corre el notebook de principio a fin y guarda los outputs. Si una celda falla, podés elegir si continúa o para.

```bash
# Ejecutar y guardar con outputs
jupyter nbconvert --to notebook --execute analisis.ipynb --output ejecutado.ipynb

# Continuar aunque haya errores
jupyter nbconvert --to notebook --execute analisis.ipynb --allow-errors --output ejecutado.ipynb

# Ejecutar desde Python
import subprocess
subprocess.run([
    'jupyter', 'nbconvert', '--to', 'notebook',
    '--execute', 'analisis.ipynb',
    '--output', 'ejecutado.ipynb'
], check=True)
```

### 4. Ejecución parametrizada con Papermill

Papermill te deja pasar parámetros al notebook. Es como convertir el notebook en una función: ejecutás el mismo notebook con distintos inputs.

```python
import papermill as pm
for region in ['Norte', 'Sur', 'Este']:
    pm.execute_notebook('template.ipynb', f'reporte_{region}.ipynb',
                        parameters={'region': region, 'anio': 2024})
```

Papermill agrega una celda con parámetros que el notebook lee con `papermill.parameters`. Ideal para generar un reporte por cliente, sucursal, o período.

### 5. Exportar a otros formatos

```bash
# A script Python (limpio, sin outputs)
jupyter nbconvert --to script analisis.ipynb

# A HTML (con outputs incluidos)
jupyter nbconvert --to html analisis.ipynb

# A PDF (requiere LaTeX instalado)
jupyter nbconvert --to pdf analisis.ipynb
```

## Alternativas

- **Papermill vs nbconvert --execute**: Papermill te da parametrización, lo que lo hace ideal para notebooks reutilizables. `nbconvert --execute` es más simple y no necesita instalación extra.
- **Quarto**: [Quarto](https://quarto.org) es el sucesor espiritual de Jupyter Notebooks para publishing. Te deja escribir en markdown con código嵌入, ejecutar, y exportar a HTML/PDF/Word. Si generás reportes para otros, Quarto da resultados más profesionales.
- **JupyterLab vs VS Code**: Ambos tienen buena integración de notebooks. VS Code es más liviano y mejor para desarrollo. JupyterLab es mejor para exploración visual con widgets.
- **Notebooks vs scripts**: Para producción, los scripts ganan siempre (más fáciles de testear, versionar, y ejecutar en pipelines). Usá notebooks para exploración y reportes, no para código de producción.

## Anti-patrones

- ❌ **Notebooks en producción**: Ejecutar notebooks como parte de un pipeline ETL. Los notebooks son para explorar, no para producir. Convertilos a scripts antes.
- ❌ **Celdas fuera de orden**: Ejecutar celdas en orden no lineal (saltar, volver atrás). Cuando otro corre el notebook de arriba a abajo, explota todo. Reiniciá el kernel y ejecutá todo en orden antes de compartir.
- ❌ **Outputs enormes en el notebook**: `df.head(1000)` o plots en base64 que ocupan 50 MB. Usá `nbstripout` o limpiá outputs antes de commitear.
- ❌ **No usar nbformat**: Editar .ipynb como JSON a mano o con `json.load()`. `nbformat` maneja la versión, el esquema, y la estructura correctamente.
- ❌ **Código sin markdown**: Un notebook con solo celdas de código es un script disfrazado. Usá markdown para explicar qué hacés y por qué.

## Comandos

```bash
# Instalar herramientas
pip install nbformat nbconvert papermill jupyter

# Ejecutar notebook
jupyter nbconvert --to notebook --execute analisis.ipynb --output ejecutado.ipynb

# Exportar a script
jupyter nbconvert --to script analisis.ipynb

# Ver ejecución sin abrir navegador
jupyter nbconvert --to html analisis.ipynb --stdout | head -50
```
