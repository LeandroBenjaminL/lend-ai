# Workflow: Data Question

## Flujo principal

```
Orchestrator → [1. Contexto] → [2. Refinar] → [3. Hipótesis] → [4. Datos] → [5. Priorizar] → [6. Documentar] → Orchestrator
```

## Paso a paso

### 1. Entender el contexto de negocio

Entrá sin prejuicios, escuchá primero. Preguntá:

- ¿Cuál es el problema de negocio real, más allá de lo que pidieron?
- ¿Quién va a usar los resultados? ¿Qué decisión van a tomar con esto?
- ¿Qué harían distinto si tuvieran esta respuesta?
- ¿Cuál es el costo de NO tener esta información?

Si el pedido es vago ("analizame las ventas"), retrocedé hasta encontrar el verdadero objetivo. _"¿Qué decisión dependiente de este análisis están postergando?"_

### 2. Hacer preguntas para refinar (método socrático)

Cada respuesta del stakeholder abre una nueva capa. No asumas, preguntá:

- **De la métrica:** "¿Ventas en pesos, en unidades, o margen bruto?"
- **Del alcance:** "¿Todos los productos o solo una categoría? ¿Todos los clientes o un segmento?"
- **Del tiempo:** "¿Comparado con qué período? ¿Querés tendencia, estacionalidad, o cambio puntual?"
- **Del por qué:** "¿Qué pasó en el negocio que disparó esta pregunta ahora?"
- **De la acción:** "Si el resultado es X, ¿qué harías? ¿Y si es Y?"

Regla de oro: **nunca aceptés la primera definición de un problema.** Siempre hay una pregunta mejor debajo.

### 3. Definir hipótesis concretas

Transformá la discusión en hipótesis comprobables. Usá el formato canónico:

```
Hipótesis N: [variable A] afecta a [variable B] en [contexto]
Métrica: [cómo medimos el efecto]
Criterio de éxito: [umbral que confirma la hipótesis]
Datos necesarios: [qué columnas/datasets se requieren]
Riesgos: [qué podría sesgar el análisis]
```

Cada hipótesis debe ser falsable — tiene que poder ser refutada con datos. Si no se puede refutar, no es una hipótesis, es una opinión.

### 4. Identificar qué datos se necesitan

Para cada hipótesis definida en el paso 3, especificá:

- **Qué variables** (columnas, fuentes, granularidad)
- **Dónde están** (DB, CSV, API, sistema legacy)
- **Cuánto período** (ventana temporal necesaria)
- **Calidad esperada** (¿hay nulos? ¿las fechas son confiables? ¿hay duplicados conocidos?)
- **Qué NO tenemos** (datos faltantes que podrían limitar el análisis — sé honesto acá)

Si los datos no existen o son de mala calidad, lo marcás ya. Mejor saberlo antes que descubrirlo después de dos semanas de análisis.

### 5. Priorizar preguntas por impacto

No todas las hipótesis se investigan. Evaluá cada una contra dos ejes:

| Eje | Pregunta |
|-----|----------|
| Impacto | ¿Cambia una decisión de negocio significativa? |
| Viabilidad | ¿Tenemos los datos? ¿En qué estado están? |

Clasificá en:

- **Prioridad 1:** Alto impacto + datos disponibles → **YA**
- **Prioridad 2:** Alto impacto + datos dudosos → investigar factibilidad primero
- **Prioridad 3:** Bajo impacto + datos disponibles → si sobra tiempo
- **Archivar:** Bajo impacto + sin datos → no pierdas tiempo

Presentá esta matriz al stakeholder. Que elijan ELLOS dónde poner el esfuerzo, conociendo los tradeoffs.

### 6. Documentar el plan de análisis

Salida final: un documento que cualquier persona del equipo pueda leer y ejecutar. Estructura mínima:

1. **Pregunta de negocio** (una sola oración, clara)
2. **Hipótesis priorizadas** (tabla con hipótesis, métrica, criterio de éxito)
3. **Matriz impacto vs viabilidad** (visual, para compartir con stakeholders)
4. **Fuentes de datos requeridas** (qué, dónde, período, contacto del dueño)
5. **Riesgos y limitaciones conocidas** (datos faltantes, calidad dudosa, sesgos potenciales)
6. **Próximos pasos** (qué agente se encarga de qué — data-profiling, data-analysis, etc.)
7. **Criterio de cierre** (¿cuándo damos por respondida la pregunta?)
