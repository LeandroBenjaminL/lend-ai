# Workflow: Data Validation

## Flujo principal

```
Orchestrator → [1. Definir schema/rules] → [2. Elegir herramienta] → [3. Ejecutar validación] → [4. Reportar resultados] → [5. Decidir: reject o warn] → [6. Documentar contrato] → Orchestrator
```

## Paso a paso

### 1. Definir schema y reglas de validación

Leer el prompt o el dataset para entender qué se espera. Documentar explícitamente cada regla antes de escribir código:

- **Tipos esperados:** ¿`int64`, `float64`, `str`, `datetime`, `bool`? Sin ambigüedad.
- **Rangos:** edad 0-120, precio ≥ 0, porcentaje 0-100. Si no hay rango definido, preguntar.
- **Required vs nullable:** ¿qué columnas admiten nulos? ¿Cuál es el umbral de nulos tolerable?
- **Unique:** ¿hay columnas que deben ser únicas? ¿Combinaciones de columnas (compound key)?
- **FK-like checks:** ¿valores de esta columna deben existir en otra tabla o conjunto de referencia?
- **Regex / formatos:** emails, teléfonos, CUIT, fechas con formato específico.
- **Chequeos entre columnas:** `fecha_fin >= fecha_inicio`, `total = cantidad * precio_unitario`.

Si el schema no está definido por el usuario, inferilo del dataset de referencia con `pa.infer_schema()` — pero siempre revisalo manualmente. La inferencia automática es un punto de partida, no una verdad.

### 2. Elegir la herramienta correcta

Usar esta tabla de decisión:

| Contexto | Herramienta | Por qué |
|---|---|---|
| APIs, modelos de datos, registros individuales | **Pydantic** | Type-safe, validación por instancia, integración con FastAPI, serialización JSON nativa |
| DataFrames, análisis exploratorio, batches | **Pandera** | Schemas column-wise, integración directa con pandas, lazy validation, inferencia de schema |
| Pipelines ETL complejos, data warehouses | **Great Expectations** | Expectations como documentación viva, data docs automáticos, profiling, integración con Spark/SQL/DBs |
| Validación rápida en notebook | **Pandera (infer)** | `pa.infer_schema(df_ref).validate(df_new)` — 2 líneas |

**Regla de oro:** si estás validando un DataFrame, usá Pandera. Si estás validando datos que entran por una API, usá Pydantic. Si es un pipeline productivo con múltiples fuentes y necesitás documentar expectativas, usá Great Expectations.

### 3. Ejecutar la validación

- **Pandera:** `schema.validate(df, lazy=True)` para obtener todos los errores de una sola pasada (no fallar al primer error). Siempre preferí `lazy=True` salvo que pidan específicamente lo contrario.
- **Pydantic:** validar fila por fila, recolectar errores en una lista con índice de fila y mensaje.
- **Great Expectations:** crear Suite, ejecutar `validator.validate()`, revisar `validator.validate().success`.

Capturar siempre el output de validación — no solo el booleano de pasa/no pasa, sino los failure cases con ejemplos concretos.

### 4. Reportar resultados

El reporte debe incluir sí o sí:

- ✅ **Qué pasó la validación** — con cantidades (ej. "45/50 columnas OK").
- ❌ **Qué falló** — columna, regla violada, cantidad de filas afectadas, % del total.
- 📋 **Ejemplos concretos** — primeras 3-5 filas que fallaron cada regla. Sin ejemplos, el reporte es inútil.
- 📊 **Resumen numérico:** total de filas, filas con al menos un error, tasa de error general.

Formato del reporte: tabla Markdown o DataFrame con columnas `columna | regla | fallos | % | ejemplos`. Si lo pide el usuario, delegar a `data-reporter` para generar PDF/HTML.

### 5. Decidir: ¿reject o warn?

Basado en la severidad del error y el contexto del negocio:

| Tipo de error | Acción por defecto | Justificación |
|---|---|---|
| Columna faltante | **Reject** | El schema está roto — no se puede procesar |
| Tipo de dato incorrecto | **Reject** | `str` en columna numérica = corrupción |
| Clave primaria duplicada | **Reject** | Integridad referencial comprometida |
| Valor fuera de rango | **Reject** si rango es hard constraint, **Warn** si es estadístico |
| Nulos > umbral | **Reject** si columna es `nullable=False`, **Warn** si el umbral es blando |
| Formato inconsistente | **Warn** | Fechas en formato mixto: se puede normalizar, pero hay que avisar |
| Distribución anómala | **Warn** | Puede ser seasonality legítima — no rechazar sin investigar |

Si hay dudas entre reject y warn, siempre preguntar al usuario. "Che, esta columna tiene 15% de nulos cuando el umbral acordado era 5%. ¿Rechazo el batch o lo marcamos como warning y dejamos que el consumer decida?"

### 6. Documentar el contrato actualizado

Si se modificó el schema durante el proceso (se agregaron reglas, se ajustaron rangos, se descubrieron edge cases), actualizar la documentación del contrato:

- Guardar el schema final (Pandera: `schema.to_yaml()`, Pydantic: código del modelo, GE: `context.save_expectation_suite()`).
- Registrar edge cases descubiertos.
- Si se usa un sistema de data contracts (DataHub, schemas registry), actualizarlo.
