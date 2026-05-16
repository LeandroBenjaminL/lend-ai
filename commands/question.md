---
description: Definir preguntas, hipótesis y objetivos del análisis antes de empezar
agent: data-analyst
subtask: true
---

Antes de tocar datos, definamos qué queremos descubrir.

FLUJO:
1. Preguntá al usuario: ¿qué necesita saber?
2. Aplicá marco SMART: específico, medible, alcanzable, relevante, temporal
3. Definí hipótesis comprobables
4. Identificá métricas de éxito
5. Devolvé especificación clara del problema

SKILLS A CARGAR: data-question

## Uso

`@data-analyst /question "What drives customer churn?"`

`@data-analyst /question "Which products have the highest margin?"`

## Ejemplo

Input: `@data-analyst /question "What drives customer churn?"`

Output:
```
🎯 Pregunta SMART

Específica: ¿Qué factores (demográficos, comportamiento, soporte)
            predicen el churn de clientes en los próximos 90 días?

Métrica: Tasa de churn = clientes perdidos / clientes totales

Hipótesis:
  H1: Clientes con menos de 3 logins/semana tienen mayor churn
  H2: Tickets de soporte sin resolver >48h → churn +40%
  H3: Descuento inicial >30% atrae clientes menos leales

Éxito: Modelo con AUC > 0.80 en validación
```
