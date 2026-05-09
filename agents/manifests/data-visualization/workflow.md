# Workflow: Data Visualization

## Flujo principal

```
Orchestrator → [1. Entender la historia] → [2. Elegir chart] → [3. Preparar datos] → [4. Crear gráfico] → [5. Customizar] → [6. Validar legibilidad] → [7. Exportar] → Orchestrator
```

## Paso a paso

### 1. Entender qué historia querés contar
Leer el prompt completo. Identificar: ¿comparación, distribución, composición, relación, tendencia? ¿Quién lo va a ver (técnico, ejecutivo, público general)? Definir el mensaje en una frase. Si no podés resumir la historia en una oración, no arranques.

### 2. Elegir el tipo de chart correcto
Usar la tabla de decisión abajo. Preguntarte: ¿variables categóricas o numéricas? ¿una o múltiples? ¿tiempo involucrado? No uses gráfico de torta a menos que sean ≤3 categorías con diferencias claras. No uses 3D salvo que sea estrictamente necesario (ej. superficie de respuesta).

### 3. Preparar los datos para ese chart
Agrupar, pivotear, normalizar según lo que el chart necesite. Si es un line plot: datos en formato largo (`pd.melt`). Si es un heatmap de correlación: `df.corr()`. Si es un boxplot: agrupar por categoría. Limpiar nulos y outliers que distorsionen la escala.

### 4. Crear el gráfico con la librería adecuada
- **Matplotlib**: control total, publicación científica, multi-panel complejo.
- **Seaborn**: estadístico, elegante por defecto, `hue`/`size`/`style` nativos.
- **Plotly Express**: interactivo, dashboards, compartible como HTML. Si la audiencia necesita hacer zoom o hover, Plotly sin dudarlo.

### 5. Customizar: títulos, etiquetas, colores, leyendas
- `figsize` siempre explícito (nunca defaults).
- `plt.title()`, `plt.xlabel()`, `plt.ylabel()` con información útil, no genérica.
- Paletas accesibles (`'viridis'`, `'cividis'`, `'Set2'` para categóricos). Si usás rojo/verde juntos, pensalo dos veces.
- Leyenda solo si aporta. Si hay una sola serie, la leyenda es ruido.

### 6. Validar que el gráfico sea legible e interpretable
Preguntate: ¿se entiende sin leer el texto que lo acompaña? ¿Las escalas son honestas (no truncadas engañosamente)? ¿Los colores son distinguibles? ¿El mensaje principal salta a la vista en 3 segundos? Si no, iterar.

### 7. Exportar o mostrar
- Estático: `plt.savefig('archivo.png', dpi=300, bbox_inches='tight')`.
- Interactivo: `fig.write_html('archivo.html')` o `fig.show()`.
- Para reportes: delegar a `data-reporter` si se necesita PDF/Markdown/HTML compuesto.

## Tabla de decisión: qué chart usar

| Historia | Tipo de datos | Chart | Alternativa |
|---|---|---|---|
| Comparar categorías | 1 categórica + 1 numérica | Bar plot (horizontal si >5 cats) | Dot plot, lollipop |
| Mostrar ranking | 1 categórica + 1 numérica | Bar plot ordenado | Slope chart |
| Evolución temporal | 1 fecha + 1 numérica | Line plot | Area plot (si apilado) |
| Múltiples series temporales | 1 fecha + N numéricas | Line plot con hue | Small multiples |
| Relación entre 2 numéricas | 2 numéricas | Scatter plot | Hexbin (>10k puntos) |
| Relación con tendencia | 2 numéricas | Scatter + regresión (`regplot`) | Scatter + LOESS |
| Distribución de 1 variable | 1 numérica | Histograma + KDE | Boxplot, violin |
| Distribución por categoría | 1 categórica + 1 numérica | Boxplot / Violin plot | Raincloud plot, sina plot |
| Correlación multivariable | N numéricas | Heatmap (`sns.heatmap`) | Pairplot, correlogram |
| Composición / Partes de un todo | 1 categórica + 1 numérica | Stacked bar | Treemap, waffle chart |
| Proporciones simples | 2-3 categorías | Bar plot horizontal | Pie chart (último recurso) |
