# Workflow: Data Reporter

## Skills disponibles

Cargá según la tarea:
- `reporting` → reportes HTML/PDF/Markdown (solo para reportes pesados)
- `data-visualization` → gráficos matplotlib, seaborn, plotly
- `streamlit` → dashboards interactivos
- `database-connections` → SQLAlchemy para conectar a BD y traer datos

## Flujo principal

```
Orchestrator → [1. Entender audiencia] → [2. Elegir tipo de gráfico] → [3. Preparar datos] → [4. Diseñar visual] → [5. Revisar accesibilidad] → [6. Generar output] → Orchestrator
```

## Paso a paso

### 1. Entender audiencia y contexto

Antes de escribir una línea de código, definís:

- **¿Quién ve esto?** Ejecutivo (quiere conclusión), técnico (quiere detalle), público general (quiere claridad).
- **¿Qué medio?** Dashboard interactivo, reporte PDF, slide de presentación, embed en web, Slack message.
- **¿Qué acción esperás?** Decidir, explorar, informar, alertar.
- **Restricciones conocidas:** paleta corporativa, formato de salida, tamaño máximo.

Si el orchestrator no explicita la audiencia, preguntás. No asumís.

### 2. Elegir tipo de gráfico según el dato

Usás la tabla de decisión (ver patterns.md). Regla de oro:

| Querés mostrar | Tipo de gráfico |
|---|---|
| Comparación entre categorías | Bar chart (horizontal si son muchas categorías) |
| Evolución temporal | Line chart (una serie) o área (varias) |
| Distribución de una variable | Histograma o boxplot |
| Distribución de dos variables | Scatter plot (con trend line opcional) |
| Composición de un total | Stacked bar (preferido) o treemap. Evitá pie charts. |
| Relación entre variables | Scatter + heatmap de correlación |
| Ranking | Bar chart ordenado descendente |
| Parte de un todo con pocas categorías | Donut chart (solo si son ≤5 categorías) |
| Geográfico | Choropleth map o dot density |
| Flujo entre etapas | Sankey diagram |

Si tenés dudas entre dos opciones, elegís la más simple. "El mejor gráfico es el que se entiende sin leer el eje."

### 3. Preparar los datos para el gráfico

- Agregaciones: groupby + agg antes de plotear. Nunca pasás datos crudos a un chart.
- Filtrar: outliers extremos que rompen la escala, datos incompletos o nulos en la serie.
- Normalizar escalas: si comparás magnitudes distintas, usás escala logarítmica o normalización.
- Timestamps: asegurarse que sean datetime, ordenados, sin gaps no explicados.
- Etiquetas: truncar textos largos, formatear monedas y porcentajes.

### 4. Diseño visual — la jerarquía importa

Orden de atención que diseñás deliberadamente:

1. **Título** — es el hallazgo principal, no la descripción. "Churn bajó 15% post-campaña", no "Gráfico de churn mensual".
2. **Dato principal** — el elemento visual más prominente (barra más alta, línea más marcada, punto más grande).
3. **Contexto** — ejes, leyenda, anotaciones. Deben estar pero no robar atención.
4. **Fuente y notas** — al pie, discretas.

Reglas de diseño:
- Colores: paleta corporate-first. Si no hay, usás ColorBrewer (categórico, secuencial, divergente según corresponda).
- Ejes: siempre arrancás en 0 en barras. En líneas podés recortar pero lo señalás con `//` o un break.
- Grid: sutileza extrema. Gridlines gris claro, o nada. No competís con los datos.
- Fonts: sans-serif (Arial, Helvetica, sistema). Jerarquía de tamaños: título > eje > labels > fuente.
- Animación: solo si suma a la comprensión. No animás por estética.

### 5. Revisión de accesibilidad

Checklist obligatorio antes de entregar:

- [ ] Paleta daltónica: test con simulador (CVD). Usar patrones + colores, no solo color.
- [ ] Contraste suficiente: etiquetas sobre fondos, líneas sobre áreas.
- [ ] Labels directos: preferís etiqueta al lado del punto sobre leyenda separada (menos salto visual).
- [ ] Tamaño mínimo: texto no menor a 10px, elementos interactivos no menores a 24px.
- [ ] Alternativa textual: si el output es HTML, metadata alt text. Si es PDF, descripción en el pie.
- [ ] NO usar rojo/verde como único diferenciador.
- [ ] NO usar solo color para transmitir información (agregar patrones, texturas, etiquetas).

### 6. Generar output según el medio

| Medio | Tool/Lib | Formato |
|---|---|---|
| Dashboard interactivo | Plotly, Streamlit | HTML embed |
| Reporte estático | Matplotlib + Seaborn | PNG, PDF |
| Embed en web | Plotly, Altair | JSON vega-lite, HTML |
| Slides / presentación | Matplotlib | PNG con fondo transparente |
| Slack / chat | Matplotlib + mplib | PNG inline |
| Notebook | Matplotlib + Seaborn | SVG (escalable, no raster) |

Siempre exportás en la resolución adecuada (300dpi para print, 72-150 para web). En formato vectorial (SVG) siempre que sea posible.
