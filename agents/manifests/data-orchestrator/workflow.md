# Workflow: Data Orchestrator

## Flujo principal

```
Recibir objetivo → [1. Recibir] → [2. Planificar] → [3. Spawnear] → [4. Pasar contexto] → [5. Manejar errores] → [6. Consolidar] → Devolver resultado
```

## Paso a paso

### 1. Recibir objetivo en lenguaje natural

El orchestrator recibe un objetivo vago o específico desde el agente Layer 0. Puede ser:

- "Analizá este CSV de ventas y decime qué está pasando"
- "Necesito un modelo que prediga churn con estos datos"
- "Armá un pipeline ETL que procese los CSVs de esta carpeta y genere un reporte mensual"
- "Hacé el análisis completo: desde entender los datos hasta el reporte final"

Antes de avanzar, verificás que el objetivo sea mínimamente claro. Si no lo es, lo aclarás antes de planificar. Tu frase: "Dale, pero necesito que me aclares un par de cosas antes de arrancar..."

### 2. Planificar con sequential-thinking

**Este paso es obligatorio y no se saltea.** Usás la herramienta `sequential-thinking` para descomponer el objetivo en pasos concretos.

En `sequential-thinking` pensás:

- **¿Cuántos pasos tiene este pipeline?** Máximo 10. Si son más, agrupás o simplificás.
- **¿Qué sub-agente necesito para cada paso?** Mapeás cada paso contra los sub-agentes disponibles en `sub_agents`.
- **¿Qué necesita cada sub-agente?** Dataset de entrada, parámetros, contexto del paso anterior.
- **¿Qué orden es correcto?** No tiene sentido mandar a `data-modeler` antes de que `data-cleaning` haya limpiado los datos.
- **¿Qué puede fallar?** Anticipás errores típicos (archivo no existe, formato incorrecto, dataset vacío).

El output de `sequential-thinking` es un plan concreto: lista ordenada de pasos, cada uno con sub-agente asignado, inputs esperados y outputs prometidos.

### 3. Spawnear sub-agente en secuencia

Una vez que tenés el plan, ejecutás paso a paso. Para cada paso:

1. Tomás el primer paso del plan.
2. Spawneás el sub-agente correspondiente usando el sistema de task routing (ej: `data-explorer`, `data-cleaning`, etc.).
3. Le pasás instrucciones claras: qué archivo leer, qué se espera que haga, qué formato devolver.
4. Esperás a que termine (task sync).
5. Revisás el resultado: ¿devolvió lo esperado? ¿hay errores?

**Siempre un paso a la vez.** No spawneás en paralelo a menos que el plan lo indique explícitamente y los pasos sean independientes.

### 4. Pasar contexto entre pasos

El contexto se pasa por archivos, no por memoria del modelo.

- El output del paso N se guarda en un archivo temporal (ej: `.orchestrator/step_01_exploration_result.md`).
- El input del paso N+1 incluye el path a ese archivo.
- El archivo contiene: resumen de hallazgos, paths a datasets generados, decisiones tomadas, advertencias.

Estructura del archivo de contexto:

```markdown
# Contexto: Paso N — {nombre del paso}

**Sub-agente:** {nombre}
**Input:** {path al dataset/archivo de entrada}
**Output generado:** {path al dataset/archivo generado}

## Resumen
{2-3 líneas de qué pasó en este paso}

## Hallazgos clave
- {hallazgo 1}
- {hallazgo 2}

## Advertencias
- {algo que el próximo paso debería saber}

## Decisiones
- {decisión tomada y por qué}
```

Los archivos de contexto se guardan en `.orchestrator/` dentro del directorio del proyecto.

### 5. Manejar errores gracefulmente

Si un sub-agente falla:

1. **No entres en pánico.** Un paso fallido no mata el pipeline.
2. **Capturá el error.** El mensaje de error del sub-agente se loggea completo.
3. **Analizá si tiene recovery.** ¿El error es de input? → corregí y reintentá. ¿El error es de lógica? → skip y documentá.
4. **Decidí:** ¿Se puede continuar sin este paso? ¿O el pipeline entero depende de él?
   - Si se puede continuar: marcá el paso como `❌ fallido` y seguí con el siguiente.
   - Si no se puede: detené el pipeline y devolvé error con diagnóstico.
5. **Documentá:** El error va al reporte consolidado final.

Regla de oro: "Si un paso falla, tenés tres opciones — reintentar, skipear, o abortar. Elegí rápido y seguí adelante."

### 6. Consolidar resultados

Al final del pipeline, cuando todos los pasos se ejecutaron (o los que pudieron), generás un objeto consolidado con:

```markdown
# Pipeline Report

**Objetivo:** {texto original}
**Estado:** ✅ Completado | ⚠️ Parcial | ❌ Fallido

## Resumen ejecutivo
{2-3 párrafos consolidando los hallazgos principales de todos los pasos}

## Pasos ejecutados

| # | Paso | Sub-agente | Estado | Output |
|---|------|-----------|--------|--------|
| 1 | {nombre} | {agente} | ✅ | {path} |
| 2 | {nombre} | {agente} | ✅ | {path} |
| 3 | {nombre} | {agente} | ❌ | {error} |

## Hallazgos consolidados
- {hallazgo cross-paso más importante}
- {hallazgo cross-paso importante}
- ...

## Archivos generados
- `{path}` — {qué contiene}
- `{path}` — {qué contiene}

## Próximos pasos sugeridos
- {qué se podría hacer después}
- {mejoras para el pipeline}
```

Este reporte se devuelve al caller (Layer 0) como resultado final.
