---
description: Reporte de calidad y perfil del dataset — nulos, outliers, cardinalidad, alertas
agent: data-analyst
subtask: true
---

Generá un perfil de calidad completo del dataset.

FLUJO:
1. Cargá el dataset
2. Detectá problemas: nulos >30%, alta cardinalidad, outliers extremos, columnas constantes
3. Generá reporte de calidad con `data-profiling` skill
4. Devolvé tabla de alertas priorizadas (🔴 crítico, 🟡 warning, 🟢 ok)

SKILLS A CARGAR:
- data-profiling
- data-validation

REGLAS:
- No modifiques archivos
- Si ydata-profiling no está instalado, usá pandas nativo
- Priorizá los problemas más graves primero

## Uso

`@data-analyst /profile dataset.csv`

`@data-analyst /profile clientes.parquet --output report.html`

## Ejemplo

Input: `@data-analyst /profile ventas.csv`

Output:
```
📋 Perfil de Calidad — ventas.csv (5,000 filas × 12 cols)

🔴 Críticos:
  • precio: 40% nulos → requiere acción inmediata
  • email: 30% valores inválidos (sin @)

🟡 Warning:
  • cliente_id: alta cardinalidad (4,800 únicos)
  • descuento: outliers extremos (percentil 99 = 90%)

🟢 Ok:
  • fecha, producto, región → sin problemas

Correlaciones altas: precio ~ ingreso (0.85), cantidad ~ total (0.91)
```
