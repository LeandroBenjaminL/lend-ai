---
description: Generación rápida de visualizaciones — histogramas, scatter, boxplots, barras
agent: data-analyst
subtask: true
---

Generá visualizaciones del dataset según lo que pida el usuario o lo que tenga sentido.

FLUJO:
1. Cargá el dataset
2. Identificá columnas numéricas y categóricas
3. Generá automáticamente:
   - Histogramas para numéricas
   - Barras para categóricas (top 10)
   - Boxplots para detectar outliers
   - Scatter matrix si hay pocas numéricas
   - Matriz de correlación
4. Si el usuario pide algo específico, priorizá eso

SKILLS A CARGAR:
- data-visualization

REGLAS:
- Preferí Plotly para interactividad, Seaborn para publicación
- Usá `plt.tight_layout()` siempre
- No guardes archivos sin preguntar
- Si hay muchas columnas, seleccioná las más relevantes

## Uso

`@data-analyst /viz dataset.csv --type scatter --x age --y income`

`@data-analyst /viz ventas.csv --type histogram --x precio --bins 30 --hue categoria`

## Ejemplo

Input: `@data-analyst /viz clientes.csv --type scatter --x edad --y ingreso --hue churn`

Output:
```
📊 Generando visualización: scatter (edad × ingreso)

Columnas: edad (num), ingreso (num), churn (cat, 2 clases)
Librería: Seaborn (publicación)

Gráfico: Scatter plot con 1,500 puntos
  • Eje X: edad (rango 18-75)
  • Eje Y: ingreso (rango $0-$250K)
  • Color: churn (rojo = sí, azul = no)
  • Tendencia: churn se concentra en ingresos <$50K

Insight visual: los clientes con menor ingreso y edad
intermedia (30-45) tienen mayor tasa de churn.
```
