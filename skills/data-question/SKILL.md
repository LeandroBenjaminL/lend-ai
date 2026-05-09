---
name: data-question
description: >
  Definir preguntas de negocio, hipótesis y objetivos antes de analizar.
  Trigger: Cuando arrancás un análisis nuevo y necesitás clarificar qué querés descubrir.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "2.0"
  model_tier: T2-fast
---

# Skill: data-question

El 80% del valor de un análisis está en **hacer la pregunta correcta**. Podés tener los mejores datos, el código más limpio y las visualizaciones más lindas, pero si la pregunta está mal definida, el resultado no sirve.

Esta skill es el primer paso del pipeline analítico. No la saltees aunque tengas "poco tiempo" — una pregunta bien formulada te ahorra horas de idas y vueltas.

## Trigger

- Te pidieron "analizame esto" sin más contexto — hay que aterrizarlo
- Arrancás un proyecto nuevo — antes de tocar datos
- Tenés que alinear expectativas con un stakeholder
- Definiste una pregunta pero no está clara — refinarla antes de seguir

## Workflow

### 1. Escuchá el problema de negocio
No te dejes llevar por lo que te piden literalmente. Si te dicen "hacé un análisis de ventas", preguntate: ¿para qué? ¿Qué decisión se va a tomar con esa información?

### 2. Traducí a una pregunta analítica
Pasá de "necesito entender las ventas" a "¿qué factores explican la caída de ventas en el segmento PyME durante Q4?".

### 3. Aplicá el marco SMART
Asegurate de que la pregunta sea Específica, Medible, Alcanzable, Relevante y con horizonte Temporal.

### 4. Definí la hipótesis
Escribí una hipótesis clara: "Si [variable independiente] cambia, entonces [variable dependiente] se modifica así".

### 5. Validá con el stakeholder
Antes de escribir una línea de código, mostrale la pregunta al que pidió el análisis. Si está de acuerdo, arrancás. Si no, ajustás.

## Patrones y ejemplos

### Marco SMART para preguntas de datos

| Criterio | Pregunta guía | Ejemplo concreto |
|----------|--------------|-----------------|
| **S** específico | ¿Qué exactamente queremos medir? | "tasa de conversión del checkout" (no "rendimiento") |
| **M** medible | ¿Cómo cuantificamos el resultado? | "promedio de conversión semanal" |
| **A** alcanzable | ¿Tenemos los datos? | sí, tenemos eventos de usuario desde enero |
| **R** relevante | ¿Aporta valor real? | impacta directamente en prioridad de features |
| **T** temporal | ¿En qué período? | "comparando antes/después del nuevo checkout (Mar-May vs Jun-Ago)" |

### Estructura de hipótesis documentada

```markdown
## Hipótesis: A/B testing de nuevo checkout
- **Hipótesis**: El nuevo checkout de 1 paso aumenta la tasa de conversión
- **Métrica**: % de usuarios que completan la compra sobre los que inician checkout
- **Criterio de éxito**: aumento ≥ 5% con significancia estadística (p < 0.05)
- **Datos necesarios**: eventos de usuario con timestamp, versión del checkout, dispositivo
- **Riesgos**: efecto novelty (los primeros días pueden no representar comportamiento real)
```

### Mala pregunta → Buena pregunta

| ❌ Mala pregunta | ✅ Buena pregunta |
|-----------------|-------------------|
| "Analizame las ventas" | "¿Qué canales de adquisición tienen mejor retención a 90 días?" |
| "Hacé un modelo de churn" | "¿Qué variables predicen que un usuario abandone en los primeros 30 días?" |
| "Dame insights de clientes" | "¿Los clientes que usan soporte técnico tienen menor tasa de abandono?" |
| "Comparamos con la competencia" | "¿Cómo varía nuestro precio relativo por categoría vs los 3 competidores principales?" |

## Alternativas

| Técnica | Cuándo usarla |
|---------|---------------|
| **SMART** | Preguntas de negocio estándar — es el default |
| **HMW (How Might We)** | Para problemas abiertos o exploratorios |
| **5 Whys** | Cuando el pedido viene muy vago y hay que llegar a la raíz |
| **Jobs to be Done** | Cuando el análisis es sobre comportamiento de usuario |
| **ICE Score (Impact, Confidence, Ease)** | Para priorizar múltiples preguntas/hipótesis |

**Recomendación**: SMART alcanza para el 90% de los casos. Los 5 Whys son útiles cuando el stakeholder no sabe bien qué quiere.

## Anti-patrones

- ❌ **Aceptar la pregunta tal como viene** — "analizame esto" sin chorrear no es una pregunta
- ❌ **Hacer preguntas que no se pueden responder con los datos disponibles** — vas a perder tiempo
- ❌ **Preguntas demasiado amplias** — "¿cómo mejorar el negocio?" no es analizable, hay que acotar
- ❌ **Confundir correlación con causalidad en la hipótesis** — "los clientes que compran X también compran Y" no es "X causa Y"
- ❌ **No validar la pregunta con el stakeholder antes de arrancar** — el mayor riesgo de retrabajo
