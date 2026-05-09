---
name: data-design
description: >
  Diseñar la estrategia de análisis, elegir el enfoque y planificar la implementación.
  Trigger: Cuando ya tenés clara la pregunta y necesitás decidir cómo abordarla.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "2.0"
  model_tier: T2-fast
---

# Skill: data-design

El diseño es el puente entre la pregunta de negocio y el código. Es donde definís **qué vas a hacer, con qué herramientas, y por qué ese enfoque**. Saltarse esta etapa es el error más común: agarrar los datos y empezar a codear sin plan, lo que lleva a resultados inconsistentes, idas por las ramas y pérdida de tiempo.

Pensalo así: no construirías una casa sin plano. Tampoco construyas un análisis sin diseño.

## Trigger

- Ya definiste la pregunta de negocio (usá data-question primero)
- Hay múltiples caminos posibles y necesitás elegir uno
- Estás por arrancar a codificar — detenete y pensá el enfoque primero
- Vas a presentar una propuesta técnica y necesitás justificar tus decisiones

## Workflow

### 1. Aclarar el tipo de análisis
¿Es descriptivo (qué pasó), diagnóstico (por qué pasó), predictivo (qué va a pasar) o prescriptivo (qué deberíamos hacer)? Cada tipo pide métodos y herramientas distintas.

### 2. Elegir el método
Estadístico (tests de hipótesis), ML (modelo predictivo), visual (tendencias y patrones gráficos) o híbrido. No elijas ML porque "queda bien" — si una visualización responde la pregunta, es más simple y más defendible.

### 3. Definir las variables
¿Cuáles son tus variables independientes y dependientes? ¿Qué columnas vas a necesitar? ¿Hay variables proxy si no tenés la medida exacta?

### 4. Planificar la validación
¿Cómo vas a saber si el análisis es correcto? Train/test split, cross-validation, contraste con datos históricos, o revisión manual con un experto de negocio.

### 5. Estimar el esfuerzo
¿Cuánto va a tomar cada etapa (limpieza, análisis, visualización, documentación)? Esto evita prometer resultados que no podés entregar a tiempo.

## Patrones y ejemplos

### Matriz de decisión de enfoque

```markdown
| Pregunta | Enfoque recomendado | Herramientas |
|----------|--------------------|--------------|
| "¿Cuánto vendimos?" | Descriptivo (agregaciones) | Pandas, SQL |
| "¿Por qué cayó?" | Diagnóstico (comparación + filtros) | Pandas, visualización |
| "¿Qué va a pasar?" | Predictivo (serie temporal / ML) | Prophet, scikit-learn |
| "¿Qué deberíamos hacer?" | Prescriptivo (simulación / optimización) | SimPy, PuLP, what-if |
```

### Esqueleto de plan de análisis

```python
plan = {
    "pregunta": "¿El nuevo layout aumenta la conversión?",
    "tipo": "diagnóstico",
    "metodo": "A/B test con bootstrap",
    "variables": {
        "independiente": "versión_layout (A/B)",
        "dependiente": "tasa_conversión",
        "control": "tráfico, día_semana, dispositivo"
    },
    "validacion": "bootstrap con 10k repeticiones, IC 95%",
    "datos_necesarios": [
        "eventos_usuario (60 días antes y después)",
        "tabla_layout_por_usuario"
    ],
    "riesgos": [
        "Efecto novelty: los primeros días pueden no ser representativos",
        "Estacionalidad semanal: comparar mismo día de semana"
    ]
}
```

### Tradeoffs a considerar

| Decisión | Ventaja | Riesgo |
|----------|---------|--------|
| **Modelo simple vs complejo** | Simple se explica solo, fácil de mantener | Puede no capturar patrones finos |
| **Muestra vs todo el dataset** | Rápido para iterar | La muestra puede no ser representativa |
| **Código ad-hoc vs pipeline** | Flexible, rápido al principio | Difícil de reproducir y mantener |
| **Visual vs estadístico** | La visual es intuitiva | Difícil de cuantificar certeza |

**Regla de oro**: empezá siempre por lo más simple que pueda funcionar. Solo agregá complejidad cuando el enfoque simple no alcance.

## Alternativas

- **Diagramas de flujo**: dibujá el pipeline antes de codificar (Miro, Draw.io, o papel)
- **RFCs técnicos**: documentos formales de diseño para proyectos grandes (usá sdd-design si estás en SDD)
- **Pair design**: diseñá con un colega — dos cabezas atrapan más riesgos
- **Notebook prototipo**: para dudas metodológicas, hacé un mini prototipo antes de diseñar el análisis completo

## Anti-patrones

- ❌ **Diseñar en la cabeza sin escribirlo** — lo que no está escrito no existe y no se puede criticar
- ❌ **Elegir método por moda** — "usemos ML" no es una decisión de diseño, es una respuesta automática
- ❌ **No considerar limitaciones de datos** — diseñás un análisis que necesita datos que no tenés
- ❌ **Diseño sin validación** — si no sabés cómo vas a verificar, no sabés si el resultado vale algo
- ❌ **Pasar directo de la pregunta al código** — el diseño es lo que evita que tengas que rehacer todo
