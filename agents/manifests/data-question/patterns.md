# Patterns: Framework de Preguntas Analíticas

> _Esto no es código. Es estrategia. Acá no se habla de DataFrames ni de modelos — se habla de problemas de negocio._

## Framework de preguntas: las 4W + H

Antes de aceptar un pedido de análisis, respondé estas 5 preguntas. Si no podés responderlas todas, el pedido no está listo.

| Dimensión | Pregunta | Ejemplo malo | Ejemplo bueno |
|-----------|----------|-------------|---------------|
| **What** | ¿Qué queremos medir o descubrir? | "Analizar ventas" | "Comparar el ticket promedio por canal (online vs físico) en Q1 2026" |
| **Why** | ¿Por qué importa? ¿Qué decisión habilita? | "Porque el CEO lo pidió" | "Para decidir si duplicamos la inversión en marketing digital o en puntos de venta" |
| **Who** | ¿Quién consume esto? ¿Qué nivel técnico tiene? | "El equipo" | "La gerencia comercial — necesitan un dashboard ejecutivo, no un notebook" |
| **When** | ¿En qué período? | "Reciente" | "Enero 2025 a Marzo 2026, con comparación interanual" |
| **How** | ¿Cómo se va a usar el resultado? | "Para tenerlo" | "Se presenta al directorio el 15 de mayo para aprobar presupuesto Q3" |

## SMART Hypotheses

Toda hipótesis debe cumplir los 5 criterios. Si falla uno, volvé a refinarla.

| Criterio | Pregunta guía | Trampa común |
|----------|--------------|--------------|
| **S**pecífico | ¿Qué exactamente? | "Las ventas están bajando" → ¿Qué producto? ¿En qué región? |
| **M**edible | ¿Cómo cuantificamos? | "Mejorar la experiencia" → ¿NPS? ¿Tasa de rebote? ¿Tiempo en página? |
| **A**lcanzable | ¿Tenemos los datos? | Asumir que datos existen sin verificar con IT |
| **R**elevante | ¿Aporta valor real? | Análisis interesantes pero que no cambian ninguna decisión |
| **T**emporal | ¿En qué plazo? | "Tendencia histórica" sin especificar desde cuándo ni granularidad |

### Ejemplo de hipótesis SMART

```
❌ MAL: "Los clientes jóvenes compran más."
✅ BIEN:
   Hipótesis: Clientes de 18-30 años tienen un ticket promedio mayor que los de 31-50
              en compras online durante 2025.
   Métrica: Diferencia de medias de ticket promedio entre segmentos.
   Criterio de éxito: Diferencia > 15% con p < 0.05.
   Datos: tabla 'orders' + tabla 'customers', columna 'birth_date' y 'channel'.
   Riesgos: Sesgo de autoselección (los jóvenes que compran online ya son tech-savvy).
```

## Cómo evitar preguntas ambiguas

### Síntomas de ambigüedad (⚠️ detectalos temprano)

| Síntoma | Ejemplo | Antídoto |
|---------|---------|----------|
| Adjetivos vagos | "Mejorar", "optimizar", "analizar" | Pedí la métrica concreta |
| Verbos sin objeto | "Entender el comportamiento" | ¿Comportamiento de qué? ¿Medido cómo? |
| Tiempo indefinido | "Últimamente", "recientemente" | Fechas exactas o al menos rango |
| Sujeto colectivo | "Los clientes" | Segmentá: ¿nuevos? ¿recurrentes? ¿por canal? |
| Sin criterio de éxito | "Quiero ver qué sale" | ¿Qué resultado te haría tomar acción? |

### Técnica de los 5 porqués

Cuando el pedido inicial es superficial, aplicá esta secuencia. Ejemplo real:

1. _"Analizame las ventas."_ → ¿Por qué?
2. _"Porque están bajando."_ → ¿Por qué creés que están bajando?
3. _"Creo que es por la competencia."_ → ¿Por qué pensás que es la competencia?
4. _"Perdimos dos clientes grandes el mes pasado."_ → ¿Por qué se fueron esos clientes?
5. _"Dicen que nuestro precio es más alto."_ → **Pregunta real definida:** ¿Somos más caros que la competencia para el mismo volumen de compra?

De _"analizame las ventas"_ a una hipótesis comprobable en 5 preguntas.

## Checklist pre-análisis

Antes de pasarle el plan a los agentes técnicos (data-profiling, data-analysis), verificá:

- [ ] La pregunta de negocio cabe en UNA oración sin ambigüedad
- [ ] Cada hipótesis tiene métrica, criterio de éxito y datos especificados
- [ ] Las fuentes de datos fueron confirmadas (no asumidas) con el dueño del dato
- [ ] Los riesgos y limitaciones están documentados y el stakeholder los conoce
- [ ] La matriz impacto/viabilidad fue revisada y aprobada por quien toma decisiones
- [ ] El output esperado está alineado con el nivel técnico de quien lo consume (dashboard, notebook, PDF, presentación)
- [ ] Hay un criterio de cierre claro: ¿cuándo decimos "esto ya está respondido"?
- [ ] El stakeholder sabe qué decisiones va a tomar con cada posible resultado

## Anti-patrones: lo que NUNCA hacés

- **No tirás a adivinar.** Si te falta información, preguntás. No asumís.
- **No aceptás "para tenerlo" como objetivo.** Todo análisis existe para habilitar una decisión.
- **No prometés lo que los datos no pueden dar.** Si la calidad es mala, lo decís. Si el dato no existe, lo marcás.
- **No priorizás vos solo.** La matriz impacto/viabilidad se comparte y el stakeholder decide.
- **No arrancás a codear antes de tener la pregunta clara.** _"Primero preguntá, después medí."_
