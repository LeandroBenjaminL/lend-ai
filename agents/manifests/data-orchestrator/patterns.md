# Patterns: Orchestrator Playbook

## Pattern 1: Sequential-Thinking Planning

Antes de spawnear CUALQUIER sub-agente, ejecutás `sequential-thinking` con esta estructura:

```
Thought 1: ¿Cuál es el objetivo final?
Thought 2: ¿Qué pasos necesito para llegar?
Thought 3: ¿Qué sub-agente necesito en cada paso?
Thought 4: ¿Qué necesita cada sub-agente para trabajar? (inputs, contexto)
Thought 5: ¿Qué me va a devolver cada sub-agente? (outputs esperados)
Thought 6: ¿Cuál es el orden correcto de los pasos?
Thought 7: ¿Qué puede salir mal en cada paso?
Thought 8: ¿Cómo manejo cada posible error?
Thought 9: Plan final — lista ordenada de pasos.
```

El output del planning se guarda en `.orchestrator/plan.md` antes de ejecutar.

### Template: Plan de pipeline

```yaml
pipeline:
  objetivo: "Descripción del objetivo"
  pasos:
    - orden: 1
      nombre: "Exploración inicial"
      sub_agente: data-explorer
      input: "data/raw/dataset.csv"
      output_esperado: "Resumen de EDA con estadísticas y alertas"
      error_strategy: "critical"  # si falla, aborta el pipeline

    - orden: 2
      nombre: "Limpieza de datos"
      sub_agente: data-cleaning
      input: ".orchestrator/step_01_exploration_result.md"
      output_esperado: "Dataset limpio en data/processed/ y resumen de transformaciones"
      error_strategy: "retry"  # reintenta una vez, luego aborta

    - orden: 3
      nombre: "Análisis y modelado"
      sub_agente: data-modeler
      input: "data/processed/dataset_clean.csv"
      output_esperado: "Modelo entrenado + métricas + feature importance"
      error_strategy: "skip"  # si falla, salteamos pero seguimos

  max_pasos: 10
```

## Pattern 2: Context File Structure

Los archivos de contexto siguen esta estructura y se guardan en `.orchestrator/`:

```
.projects/{project_name}/.orchestrator/
├── plan.md                    ← Plan generado por sequential-thinking
├── step_01_exploration.md     ← Output de data-explorer
├── step_02_cleaning.md        ← Output de data-cleaning
├── step_03_modeling.md        ← Output de data-modeler
├── step_04_report.md          ← Output de data-reporter
├── pipeline_report.md         ← Reporte consolidado final
└── error_log.md               ← Log de errores (si los hubo)
```

**Convenciones:**
- Los archivos son Markdown con estructura predecible.
- Si un sub-agente genera un dataset, el path absoluto o relativo va en el archivo de contexto.
- Cada archivo de contexto incluye: `sub-agente`, `input`, `output`, `hallazgos`, `advertencias`.
- El nombre del archivo indica el orden del paso: `step_01_`, `step_02_`, etc.

## Pattern 3: Result File Structure

El resultado consolidado sigue esta estructura y se devuelve al caller:

```json
{
  "status": "completed | partial | failed",
  "objective": "Objetivo original recibido",
  "executive_summary": "Resumen en 2-3 párrafos",
  "steps": [
    {
      "order": 1,
      "name": "Exploración inicial",
      "agent": "data-explorer",
      "status": "completed",
      "output_path": ".orchestrator/step_01_exploration.md",
      "errors": []
    },
    {
      "order": 2,
      "name": "Limpieza de datos",
      "agent": "data-cleaning",
      "status": "failed",
      "output_path": ".orchestrator/step_02_cleaning.md",
      "errors": [
        {
          "type": "file_not_found",
          "message": "El archivo data/raw/dataset.csv no existe",
          "recovery": "Skipped — se continuó sin limpieza"
        }
      ]
    }
  ],
  "generated_files": [
    ".orchestrator/pipeline_report.md",
    "data/processed/dataset_clean.csv"
  ],
  "next_steps_suggested": [
    "Corregir el path del dataset y re-ejecutar el paso de limpieza",
    "Explorar los outliers detectados en el paso 1"
  ]
}
```

## Pattern 4: Validation

Validación pre-vuelo antes de spawnear un sub-agente:

| Qué validar | Cómo | Acción si falla |
|------------|------|-----------------|
| El input del paso existe | `filesystem` → verificar path | Reintentar con path corregido o abortar |
| El sub-agente está disponible | Verificar lista `sub_agents` en manifest | Loggear error y skipear paso |
| El formato del output es el esperado | Verificar que el archivo generado existe | Marcar paso como ⚠️ parcial |
| No se superó el límite de 10 pasos | Contar pasos en el plan | Re-planificar agrupando pasos |
| El archivo de contexto no se pisó | Nombre único por paso (`step_NN_`) | Si pisa, error de diseño — corregir plan |

### Template: Pre-flight check

```
Paso {N}: {nombre}
  ✅ Input existe: {path}
  ✅ Sub-agente disponible: {nombre}
  ✅ Output esperado definido
  ✅ Paso anterior completado (o es el primero)
  → Spawneando...
```

## Pattern 5: Error Handling

### Matriz de decisión de errores

| Tipo de error | ¿Reintentar? | ¿Skip? | ¿Abortar? |
|--------------|-------------|--------|-----------|
| Archivo no encontrado | Sí (1 vez) | Depende | Si es paso crítico |
| Sub-agente no disponible | No | Sí | No |
| Output vacío o corrupto | No | Sí | No |
| Error de ejecución del sub-agente | Sí (1 vez) | Depende | Si es paso crítico |
| Timeout (>2 min) | No | Sí | No |
| Error de formato en contexto | Sí (corregir y reintentar) | No | No |

### Template: Log de error

```markdown
## Error en Paso {N}: {nombre}

**Tipo:** {tipo de error}
**Sub-agente:** {nombre}
**Mensaje:** {mensaje de error completo}
**Input esperado:** {path}
**Timestamp:** {YYYY-MM-DD HH:mm}

**Decisión:** [reintentar | skipear | abortar]
**Recovery:** {qué se hizo para recuperarse o por qué se skipió}

**Impacto:** {cómo afecta esto al resultado final}
```

### Estrategias de recovery

- **Reintentar:** Corregir el input o parámetro y spawnear de nuevo al mismo sub-agente. Máximo 1 reintento.
- **Skipear:** Marcar el paso como `❌ skip`, documentar por qué, y continuar con el siguiente paso. El reporte final indica que este paso no se ejecutó.
- **Abortar:** Detener el pipeline entero, devolver error con diagnóstico completo de qué pasó y en qué paso. No se genera reporte consolidado (solo diagnóstico de error).
- **Degradar:** Si un paso falla pero no es crítico, se puede ejecutar una versión simplificada del paso usando otro sub-agente (ej: si `data-modeler` falla, `data-analysis` puede hacer un análisis básico como fallback).
