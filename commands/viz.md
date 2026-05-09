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
