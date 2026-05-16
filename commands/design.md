---
description: Diseñar la estrategia de análisis, elegir métodos y planificar pasos
agent: data-analyst
subtask: true
---

Diseñemos cómo vamos a responder la pregunta.

FLUJO:
1. Tomá la pregunta/hipótesis definida
2. Presentá 2-3 enfoques posibles con tradeoffs
3. Elegí herramientas y métodos
4. Planificá el orden de ejecución
5. Estimá esfuerzo y complejidad

SKILLS A CARGAR: data-design

## Uso

`@data-analyst /design "predict customer churn"`

`@data-analyst /design "segment users by spending behavior"`

## Ejemplo

Input: `@data-analyst /design "forecast monthly sales for next 6 months"`

Output:
```
📐 Estrategia de Análisis

Objetivo: Forecast de ventas mensuales a 6 meses

Enfoques posibles:
┌──────────┬────────────────────────────────┬──────────┐
│ Enfoque  │ Descripción                    │ Esfuerzo │
├──────────┼────────────────────────────────┼──────────┤
│ Prophet  │ Modelo automático con estac.   │ Bajo     │
│ ARIMA    │ Clásico, requiere tuning       │ Medio    │
│ LSTM     │ Deep learning, muchos datos    │ Alto     │
└──────────┴────────────────────────────────┴──────────┘

Elegido: Prophet (rápido, detecta estacionalidad solo)
Orden: EDA → Detección de frecuencia → Prophet → Validación
```
