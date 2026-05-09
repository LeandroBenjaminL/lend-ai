# Workflow: Verificación de Análisis

Seguí estos 6 pasos en orden. No saltees ninguno — cada error que dejás pasar se amplifica en los pasos siguientes.

---

## Paso 1: Verificar que la pregunta original fue respondida

**Objetivo:** Confirmar que el análisis entregado responde exactamente lo que se preguntó, sin desviarse ni responder otra cosa.

Qué revisar:
- Recuperá la pregunta original (del brief, issue, o conversación inicial). Transcribila textual.
- Compará las conclusiones del análisis contra esa pregunta. ¿La responden directamente?
- ¿El alcance es el correcto? ¿Se analizó la población/segmento correcto, en el período correcto?
- ¿Hay preguntas implícitas sin responder? ("¿Cuál es la tendencia?" → requiere timeframe, magnitud y dirección, no solo "subió")
- ¿Las conclusiones usan métricas que responden la pregunta de negocio o métricas proxy que no significan lo mismo?

Salida esperada: un veredicto claro con 2-3 líneas. Ej: _"La pregunta era '¿qué canal tiene mejor ROI?' y el análisis muestra ROAS por canal con intervalos de confianza. Responde la pregunta. Pero falta el desglose por campaña que se pidió en el brief."_

---

## Paso 2: Revisar supuestos del análisis

**Objetivo:** Identificar todos los supuestos — explícitos e implícitos — y verificar si se cumplen.

Checklist de supuestos comunes:
- [ ] **Supuestos estadísticos:** ¿los tests usados asumen normalidad, homocedasticidad, independencia? ¿Se verificaron?
- [ ] **Supuestos de datos:** ¿se asume que no hay valores faltantes? ¿que los outliers ya se trataron? ¿que las categorías son mutuamente excluyentes?
- [ ] **Supuestos de causalidad:** ¿hay afirmaciones causales basadas en correlación? ¿Se consideraron variables de confusión?
- [ ] **Supuestos de negocio:** ¿la métrica usada realmente mide lo que el negocio cree? (ej: "engagement" medido como clicks vs tiempo en página)
- [ ] **Supuestos temporales:** ¿hay estacionalidad no considerada? ¿períodos comparables?
- [ ] **Supuestos de muestreo:** ¿la muestra es representativa? ¿hay sesgo de selección? ¿los segmentos tienen tamaño suficiente?

Salida esperada: lista de supuestos encontrados con su veredicto (✅ se cumple, ⚠️ dudoso, ❌ no se cumple). Los que fallan o son dudosos requieren explicación de impacto.

---

## Paso 3: Sanity checks

**Objetivo:** Buscar errores obvios que deberían saltar a simple vista.

### 3.1 Sanity checks numéricos

- [ ] ¿Los totales suman? (ej: segmentos que suman más que el total)
- [ ] ¿Los porcentajes suman 100%? (o lo que corresponda)
- [ ] ¿Hay métricas fuera de rango físico? (probabilidades >1 o <0, edades negativas, distancias negativas)
- [ ] ¿Las conversiones de unidades son correctas? (no confundir miles con millones)
- [ ] ¿Los promedios de ratios son correctos o hay paradojas de promedios? (ej: promediar tasas sin ponderar)
- [ ] ¿El orden de magnitud tiene sentido? (ej: un revenue per user de $1M cuando el producto cuesta $10)

### 3.2 Sanity checks de distribuciones

- [ ] ¿Hay valores extremos no explicados que dominan estadísticas?
- [ ] ¿Las distribuciones tienen la forma esperada para el dominio?
- [ ] ¿Hay distribuciones bimodales que sugieren dos poblaciones mezcladas?
- [ ] ¿Hay columnas donde 99% de valores está en un rango pero el 1% restante determina el promedio?

### 3.3 Sanity checks temporales

- [ ] ¿Hay gaps de fechas no justificados?
- [ ] ¿Hay spikes o caídas sin explicación? ¿Se cruzan con eventos externos (feriados, promociones)?
- [ ] ¿Las tendencias cambian de dirección en puntos específicos? ¿Coinciden con cambios metodológicos?

### 3.4 Sanity checks de consistencia interna

- [ ] ¿Métricas derivadas consistentes con las fuentes? (ej: `total = precio × cantidad`)
- [ ] ¿Dos formas de calcular lo mismo dan lo mismo?
- [ ] ¿Las segmentaciones son exhaustivas y mutuamente excluyentes?

Salida esperada: lista de checks con resultado. Los que fallan se reportan con el valor esperado vs el encontrado.

---

## Paso 4: Reproducir pasos clave

**Objetivo:** Verificar que los resultados son reproducibles con los mismos datos y código.

Qué hacer:
- Identificá 2-3 resultados centrales del análisis (los que sostienen las conclusiones principales).
- Para cada uno, intentá reproducirlo desde los datos crudos.
- Verificá que el código corre sin errores en un entorno limpio.
- Si hay aleatoriedad (modelos, splits), verificá que usan seeds fijas y que los resultados son estables (no cambian drásticamente con seeds distintas).
- Si hay parámetros (umbrales, hiperparámetros), verificá que están documentados y justificados.

Señales de alerta:
- El código no corre por dependencias faltantes o versiones no especificadas.
- Resultados que cambian significativamente al correr de nuevo (falta `random_state`).
- Archivos intermedios que no se regeneran (datos obsoletos).
- Pasos manuales no documentados ("después filtré a mano unos outliers").

Salida esperada: para cada resultado clave, un veredicto (✅ reproducible, ⚠️ reproducible con diferencias menores, ❌ no reproducible) con detalles.

---

## Paso 5: Verificar que las conclusiones se sostienen

**Objetivo:** Determinar si las conclusiones se desprenden de los datos o si hay saltos lógicos, interpretaciones forzadas, o explicaciones alternativas más razonables.

Para cada conclusión del análisis, chequeá:

- **Soporte estadístico:** ¿La diferencia es significativa? ¿El tamaño de efecto es relevante prácticamente (no solo estadísticamente)?
- **Causalidad vs correlación:** Si la conclusión implica causalidad, ¿hay evidencia causal o solo correlacional? ¿Se consideraron confounders?
- **Dirección correcta:** ¿Podría la relación ser al revés? (causalidad inversa)
- **Explicaciones alternativas:** ¿Hay otra hipótesis que explique los mismos datos igual de bien o mejor?
- **Paradoja de Simpson:** ¿La tendencia se mantiene al desagregar por grupos relevantes? ¿O se invierte?
- **Robustez:** ¿La conclusión se mantiene si cambiás levemente los supuestos o parámetros?
- **Generalización:** ¿La conclusión aplica solo a este dataset o es generalizable?

Salida esperada: para cada conclusión, una evaluación con nivel de confianza (alta/media/baja) y los caveats identificados.

---

## Paso 6: Reportar hallazgos y warnings

**Objetivo:** Entregar un reporte de verificación claro y accionable, no un paper académico.

Estructura del reporte final:

1. **Veredicto global:** ¿El análisis es sólido, aceptable con caveats, o necesita revisión? 3-4 líneas.

2. **Hallazgos críticos:** (los que invalidan conclusiones)
   - Describir el problema, por qué es grave, y cómo impacta las conclusiones.
   - Cada hallazgo con evidencia concreta (números, no opiniones).

3. **Warnings:** (problemas que no invalidan pero requieren atención)
   - Supuestos no verificados, limitaciones metodológicas, riesgos de interpretación.
   - Cada warning con recomendación de cómo resolverlo.

4. **Lo que está bien:** (porque también hay que reconocer lo bueno)
   - Puntos fuertes del análisis, buenas prácticas encontradas, decisiones metodológicas acertadas.

5. **Recomendaciones:** acciones concretas priorizadas
   - Qué corregir sí o sí antes de presentar.
   - Qué mejorar para la próxima iteración.
   - Qué documentar mejor.

Ejemplo de cierre:

> _"Veredicto: ⚠️ Aceptable con caveats. La conclusión principal (canal A tiene mejor ROAS que canal B) es sólida y reproducible. Pero el análisis de tendencia temporal no controla por estacionalidad — el 'crecimiento' de 15% que reportan es consistente con el patrón estacional de todos los diciembres. Corregir eso antes de presentar a Dirección. Abajo los 3 hallazgos y 5 warnings detallados."_
