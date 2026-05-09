---
name: data-visualization
description: >
  Visualización de datos con Matplotlib, Seaborn y Plotly.
  Trigger: Cuando necesitás crear gráficos, visualizar datos, o generar charts para análisis.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "1.1"
  model_tier: T2-fast
---

# Skill: data-visualization

Creación de gráficos y visualizaciones con Matplotlib, Seaborn y Plotly. Cada librería tiene un propósito distinto — elegir bien es la clave.

## Trigger

Cargá esta skill cuando:
- Necesitás gráficos de barras, líneas, scatter, histogramas o boxplots
- Querés visualizar distribuciones, correlaciones o tendencias
- Buscás gráficos publicables (Matplotlib/Seaborn) o interactivos (Plotly)
- Armás dashboards rápidos con múltiples subplots

## Librerías: cuál usar y por qué

| Librería | Cuándo | Por qué |
|----------|--------|---------|
| **Matplotlib** | Control total, personalización fina | Es la base. Si necesitás algo muy custom, vas acá. |
| **Seaborn** | Análisis estadístico, gráficos lindos por defecto | Construye sobre matplotlib con defaults inteligentes. |
| **Plotly** | Interactividad, dashboards, compartir como HTML | Hover, zoom, animación. Ideal para stakeholders. |

**Regla práctica**: arrancá con Seaborn. Si necesitás más control, bajás a Matplotlib. Si querés compartir, subís a Plotly.

## Patrones esenciales

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()  # siempre al inicio

# Bar plot
df.groupby('categoria')['valor'].mean().plot(kind='bar', figsize=(10, 6))
plt.title('Promedio por categoría')
plt.xlabel('Categoría')
plt.ylabel('Valor promedio')
plt.xticks(rotation=45)
plt.tight_layout()

# Scatter plot con Seaborn
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='variable_x', y='variable_y', hue='categoria', size='poblacion')
plt.title('Relación entre X e Y por categoría')

# Plotly interactivo
import plotly.express as px
fig = px.scatter(df, x='variable_x', y='variable_y', color='categoria',
                 size='poblacion', hover_data=['nombre'])
fig.write_html('grafico_interactivo.html')
```

## Reglas de oro

| Regla | Detalle |
|-------|---------|
| **Tamaño** | Siempre fijá `figsize=(ancho, alto)`. Gráficos deformes = datos que no se ven. |
| **Títulos** | `plt.title()`, `plt.xlabel()`, `plt.ylabel()` — siempre. Sin etiquetas no se entiende. |
| **Guardado** | `plt.savefig('archivo.png', dpi=300, bbox_inches='tight')` para calidad publicable. |
| **Multiplots** | Usá `plt.subplots(nrows, ncols, figsize=(w, h))` con `ax` compartido. |
| **Colores** | Seaborn usa paletas lindas por defecto. Evitá colores neón o arcoíris. |

## Anti-patrones

- ❌ **Gráfico de torta para más de 3 categorías**: no se puede comparar ángulos. Usá barras.
- ❌ **No escalar ejes**: si tenés outliers, el gráfico se aplana y no se ve nada. Usá `plt.ylim()` o escala log.
- ❌ **Dual y-axis innecesario**: confunde más de lo que aclara. Mejor dos gráficos separados.
- ❌ **Demasiados colores**: el cerebro no puede trackear más de 5-6 categorías distintas.
- ❌ **No ordenar barras**: las barras sin ordenar son ruido. Ordenalas por valor descendente.

## Alternativas

- **Altair** — gráficos declarativos con sintaxis tipo Vega-Lite. Ideal para notebooks.
- **Bokeh** — interactivo como Plotly, con más control servidor-side.
- **ggplot (plotnine)** — si venís de R, es la traducción más fiel a ggplot2.
- **streamlit** (skill hermana) — para dashboards completos con gráficos embebidos.

## Tools relevantes

- `matplotlib` — base de todo
- `seaborn` — análisis estadístico visual
- `plotly` / `plotly-express` — interactividad
- `altair` — alternativa declarativa
- `missingno` — visualización de patrones de nulos
