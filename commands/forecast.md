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

## Uso

`@data-analyst /forecast sales.csv --period 12 --frequency monthly`

`@data-analyst /forecast ingresos.csv --column fecha --column valor --model arima`

## Ejemplo

Input: `@data-analyst /forecast ventas_mensuales.csv --period 6 --frequency monthly`

Output:
```
📈 Forecast — ventas_mensuales (Ene 2023 - Dic 2024)
Modelo: Prophet | Frecuencia: mensual | Horizonte: 6 meses

Período       │ Predicción │ IC 80% (min-max)
──────────────┼────────────┼──────────────────
Enero 2025    │ 142,500    │ 128,000 - 157,000
Febrero 2025  │ 138,200    │ 121,000 - 155,000
...
Junio 2025    │ 165,100    │ 147,000 - 183,000

Tendencia: ↗️ 3.2% anual
Estacionalidad: pico en diciembre, valle en febrero
```
