---
description: Forecasting automático de series temporales — Prophet, ARIMA, tendencias
agent: data-analyst
subtask: true
---

Generá un forecast automático para una serie temporal.

FLUJO:
1. Preguntá dataset y columna de fecha + valor
2. Detectá frecuencia, tendencia, estacionalidad
3. Elegí modelo: Prophet (default) o ARIMA
4. Generá forecast a N períodos
5. Mostrá gráfico con predicción + intervalos de confianza
6. Explicá los resultados

SKILLS A CARGAR: time-series-analysis

REGLAS:
- Validá que la serie tenga al menos 2 períodos completos
- Explicá qué es estacionalidad, tendencia, residuo
- Si no hay Prophet instalado, usá statsmodels
