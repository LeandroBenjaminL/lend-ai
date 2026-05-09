# Workflow: Data Analysis

## Flujo principal

```
Orchestrator → [1. Recibir] → [2. Evaluar sub-agentes] → [3. Cargar] → [4. Explorar] → [5. Transformar] → [6. Validar] → [7. Devolver] → Orchestrator
```

## Paso a paso

### 1. Recibir tarea del orchestrator
Leer el prompt completo. Identificar: fuente de datos, transformación pedida, output esperado, restricciones.

### 2. Decidir si spawnear sub-agentes
- **data-profiling**: cuando el dataset es nuevo o >10k filas. Le pasás la ruta del archivo/carga y te devuelve un perfil completo. No lo usás para datasets chicos (<5k filas).
- **data-validation**: siempre al final, antes de devolver. Chequea tipos, rangos, nulos residuales, y constraints de negocio.
- Si la tarea es chica (un groupby simple sobre datos conocidos), no spawneás nada.

### 3. Cargar datos
- Si es archivo (CSV, Excel, Parquet, JSON): usar skill `file-formats`.
- Si es SQL: usar `database-connections` o `sqlite`/`mysql` según aplique.
- Tipos correctos desde `read_csv` (parse_dates, dtype, low_memory=False).
- Siempre mostrar shape, tamaño en memoria y tiempo de carga.

### 4. Exploración inicial
- `df.shape`, `df.dtypes`, `df.isnull().sum()`, `df.describe()`, `df.head(5)`.
- Detectar: nulos, duplicados, columnas irrelevantes, tipos incorrectos, cardinalidad alta.
- Si algo huele raro, lo reportás antes de seguir.

### 5. Transformar según necesidad
- Limpieza: nulos con `data-cleaning`, strings con `regex-data`.
- Agregaciones: `groupby`, `pivot_table`, `resample` para time series.
- Features: `crosstab`, `merge`, `query`, `melt`/`pivot`.
- Optimización: usar `patterns.md` como referencia de performance.

### 6. Validar
- Spawneás `data-validation` con el DataFrame final + constraints.
- Si falla, iterás corrección → re-validación.

### 7. Devolver resultados al orchestrator
- Formato claro: DataFrame final, summary de transformaciones, decisiones tomadas.
- Si se pidió visualización, delegás a `data-visualization`.
- Si se pidió reporte, delegás a `reporting`.
