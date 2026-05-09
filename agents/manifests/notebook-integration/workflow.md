# Workflow: Notebook Integration

## Flujo principal

```
Orchestrator → [1. Evaluar] → [2. Crear/Estructurar] → [3. Ejecutar] → [4. Verificar] → [5. Limpiar] → [6. Exportar] → Orchestrator
```

## Paso a paso

### 1. Evaluar la solicitud
Leer el prompt completo. Identificar: ¿crear notebook nuevo, modificar existente, ejecutar, o exportar? ¿Qué datos se van a usar? ¿Hay parámetros variables?

### 2. Crear o estructurar el notebook
**Si es notebook nuevo:**
- Crear con `nbformat.v4.new_notebook()`.
- Estructura obligatoria:
  1. Celda Markdown: título descriptivo + breve intro del análisis.
  2. Celda Code: todos los imports juntos (`import pandas as pd`, `import matplotlib.pyplot as plt`, `%matplotlib inline`, etc.).
  3. Celda Markdown: sección de carga de datos.
  4. Celda Code: carga y primeras exploraciones (`df.head()`, `df.shape`, `df.info()`).
  5. Celdas Markdown + Code alternadas: cada paso del análisis con su explicación.
  6. Celda Markdown: conclusiones.
- Usar `new_markdown_cell()` y `new_code_cell()` de `nbformat.v4`.

**Si es notebook existente:**
- Leer con `nbformat.read()`.
- Auditar estructura: ¿las celdas están en orden? ¿Hay imports dispersos? ¿El `Kernel > Restart & Run All` funciona?
- Si está desordenado, reordenar celdas y consolidar imports antes de ejecutar.

### 3. Ejecutar celdas en orden
- **Ejecución simple:** `jupyter nbconvert --to notebook --execute --inplace notebook.ipynb` o `ExecutePreprocessor` de `nbconvert`.
- **Ejecución parametrizada:** `papermill` cuando el notebook tiene variables que cambian entre ejecuciones (rutas de archivos, fechas, thresholds). `papermill input.ipynb output.ipynb -p param value`.
- Siempre ejecutar de arriba a abajo. Si una celda falla, arreglar la causa, no saltearla.

### 4. Verificar que no haya errores
- Revisar el output de la ejecución: ¿todas las celdas corrieron sin errores?
- Validar que `Restart & Run All` complete sin fallos.
- Si hay warnings, evaluar si son aceptables o hay que suprimir/fixear.
- Chequear que las celdas Markdown tengan sentido después de los resultados obtenidos.

### 5. Limpiar output si es necesario
- `jupyter nbconvert --to notebook --clear-output notebook.ipynb` para borrar todos los outputs.
- Útil antes de commitear a git (evita blobs gigantes de imágenes/base64).
- También se puede limpiar programáticamente con `nbformat`: iterar celdas y vaciar `cell.outputs`.

### 6. Exportar si se necesita compartir
- **HTML:** `jupyter nbconvert --to html notebook.ipynb` — ideal para compartir con no-técnicos.
- **PDF:** `jupyter nbconvert --to pdf notebook.ipynb` — requiere `nbconvert[webpdf]` o LaTeX.
- **Script Python:** `jupyter nbconvert --to script notebook.ipynb` — para convertir a `.py`.
- **Slides:** `jupyter nbconvert --to slides notebook.ipynb` — presentación con Reveal.js.
- Si exporta a HTML/PDF, asegurarse de que los gráficos se rendericen bien (`%matplotlib inline` en la primera celda de código).
