# Patterns: Jupyter Notebooks Cheat Sheet

## Crear notebook desde cero

```python
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

nb = new_notebook()
nb.metadata.kernelspec = {
    "display_name": "Python 3",
    "language": "python",
    "name": "python3"
}

nb.cells = [
    new_markdown_cell("# Título del Análisis\n\nDescripción breve de lo que vamos a hacer."),
    new_code_cell("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n%matplotlib inline"),
    new_markdown_cell("## Carga de datos"),
    new_code_cell("df = pd.read_csv('datos.csv')\ndf.head()"),
    new_markdown_cell("## Análisis"),
    new_code_cell("df.describe()"),
    new_markdown_cell("## Conclusiones\n\n- Hallazgo 1\n- Hallazgo 2"),
]

with open('analisis.ipynb', 'w') as f:
    nbformat.write(nb, f)
```

## Leer y modificar notebook existente

```python
import nbformat

# Leer
with open('analisis.ipynb', 'r') as f:
    nb = nbformat.read(f, as_version=4)

# Inspeccionar celdas
for i, cell in enumerate(nb.cells):
    print(f"[{i}] {cell.cell_type}: {cell.source[:60]}...")

# Agregar celda al final
nb.cells.append(new_code_cell("df.plot(kind='bar')"))

# Insertar celda en posición específica (ej: después de imports, índice 2)
nb.cells.insert(2, new_markdown_cell("## Nueva sección"))

# Guardar
with open('analisis.ipynb', 'w') as f:
    nbformat.write(nb, f)
```

## Ejecutar notebooks

```bash
# Ejecutar in-place (sobrescribe el original)
jupyter nbconvert --to notebook --execute --inplace notebook.ipynb

# Ejecutar y guardar en otro archivo
jupyter nbconvert --to notebook --execute notebook.ipynb --output ejecutado.ipynb

# Ejecutar con timeout (en segundos)
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 notebook.ipynb
```

```python
# Ejecutar desde Python con nbconvert
from nbconvert.preprocessors import ExecutePreprocessor
import nbformat

with open('notebook.ipynb', 'r') as f:
    nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
ep.preprocess(nb, {'metadata': {'path': './'}})

with open('notebook.ipynb', 'w') as f:
    nbformat.write(nb, f)
```

## Papermill — ejecución parametrizada

```bash
# Ejecutar con parámetros
papermill template.ipynb output.ipynb -p archivo datos_2024.csv -p umbral 0.75

# El notebook origen debe tener una celda con tag "parameters"
```

```python
# Crear celda de parámetros programáticamente
import nbformat
from nbformat.v4 import new_code_cell

param_cell = new_code_cell("# Parámetros\narchivo = 'datos.csv'\numbral = 0.5")
param_cell.metadata.tags = ['parameters']

# Insertar al principio (después de imports si querés)
nb.cells.insert(2, param_cell)
```

## Limpiar outputs

```bash
# Borrar todos los outputs (ideal antes de git commit)
jupyter nbconvert --to notebook --clear-output notebook.ipynb
```

```python
# Limpiar programáticamente
import nbformat

with open('notebook.ipynb', 'r') as f:
    nb = nbformat.read(f, as_version=4)

for cell in nb.cells:
    if cell.cell_type == 'code':
        cell.outputs = []
        cell.execution_count = None

with open('notebook.ipynb', 'w') as f:
    nbformat.write(nb, f)
```

## Exportar notebooks

```bash
# HTML (mejor para compartir)
jupyter nbconvert --to html notebook.ipynb --no-input  # oculta código

# HTML con código visible
jupyter nbconvert --to html notebook.ipynb

# PDF
jupyter nbconvert --to pdf notebook.ipynb
jupyter nbconvert --to webpdf notebook.ipynb  # no requiere LaTeX

# Script Python
jupyter nbconvert --to script notebook.ipynb

# Slides Reveal.js
jupyter nbconvert --to slides notebook.ipynb --post serve

# Markdown
jupyter nbconvert --to markdown notebook.ipynb
```

## Magic commands útiles

| Comando | Qué hace |
|---|---|
| `%matplotlib inline` | Gráficos embebidos en el notebook |
| `%timeit funcion()` | Medir tiempo de ejecución |
| `%%timeit` | Medir tiempo de toda la celda |
| `%who` / `%whos` | Listar variables en memoria |
| `%reset -f` | Limpiar todas las variables |
| `%run script.py` | Ejecutar script Python externo |
| `%load_ext autoreload` | Recargar módulos automáticamente |
| `%autoreload 2` | Activar autoreload |
| `%%writefile archivo.py` | Guardar contenido de celda como archivo |
| `%debug` | Entrar al debugger post-excepción |
| `%pdb` | Debugger automático ante excepciones |
| `%env VAR=valor` | Setear variable de entorno |

## ipywidgets — interactividad

```python
import ipywidgets as widgets
from IPython.display import display

# Slider + función interactiva
@widgets.interact(x=(0, 100, 10))
def filtrar(x=50):
    return df[df['valor'] > x].head()

# Dropdown + output
dropdown = widgets.Dropdown(options=['A', 'B', 'C'], description='Grupo:')
output = widgets.Output()

def on_change(change):
    output.clear_output()
    with output:
        display(df[df['grupo'] == change['new']].describe())

dropdown.observe(on_change, names='value')
display(dropdown, output)
```

## Validación de estructura de notebook

```python
def validar_notebook(nb):
    """Chequea que el notebook tenga estructura mínima."""
    errores = []

    celdas_code = [c for c in nb.cells if c.cell_type == 'code']
    celdas_md = [c for c in nb.cells if c.cell_type == 'markdown']

    if not celdas_md or not celdas_md[0].source.strip().startswith('#'):
        errores.append("Falta título en primera celda Markdown")

    if not any('import ' in c.source for c in celdas_code[:3]):
        errores.append("No hay imports en las primeras celdas")

    if not celdas_md[-1].source.strip():
        errores.append("Última celda Markdown vacía (debería tener conclusiones)")

    return errores if errores else ["✓ Notebook OK"]
```
