# Workflow: Data Cleaning

## Flujo principal

```
Orchestrator → [1. Recibir] → [2. Diagnosticar] → [3. Estrategia] → [4. Limpiar por capas] → [5. Validar] → [6. Devolver] → Orchestrator
```

## Paso a paso

### 1. Recibir dataset del orchestrator
Leer el prompt completo. Identificar: fuente del dataset (archivo, BD, API), formato, tamaño estimado, restricciones de dominio conocidas, y qué espera el orchestrator como output.

### 2. Diagnosticar SIN tocar
Este paso es sagrado. No se modifica NADA todavía.

- **Nulos:** `df.isnull().sum()` y porcentaje por columna. Clasificar: <5% (imputables), 5-60% (evaluar), >60% (candidatas a drop).
- **Duplicados:** `df.duplicated().sum()`. Si hay, mostrar muestra de duplicados para decidir si son legítimos o error.
- **Outliers:** Boxplot stats y/o IQR para columnas numéricas. Mostrar cuántos, en qué columnas, y contexto.
- **Tipos:** `df.dtypes`. Detectar columnas mal tipadas (numéricas como object, fechas como string, etc.).
- **Calidad general:** Cardinalidad de categóricas, valores únicos sospechosos, distribuciones anómalas.

### 3. Definir estrategia y consultar
Con el diagnóstico en mano, presentás al orchestrator:

- **Plan de limpieza:** qué operaciones vas a hacer, en qué orden, y por qué.
- **Decisiones de alto impacto que requieren aprobación:**
  - Dropear columnas con >60% nulos
  - Dropear duplicados cuando no hay certeza de si son legítimos
  - Eliminar outliers que podrían ser datos válidos
  - Transformaciones que cambian la semántica (ej: imputar con 0 no es lo mismo que con la mediana)

No avances sin confirmación en estos casos. Si la decisión es de bajo impacto (ej: strip() en strings, convertir tipos obvios), actuás directo.

### 4. Limpiar por capas — en este orden estricto

**Capa 1 — Nulos:**
- Columnas con >60% nulos: `dropna(axis=1, thresh=len(df)*0.4)`.
- Imputaciones según estrategia acordada: `fillna()` con media, mediana, moda, forward-fill, o valor constante.
- Registrás cada columna imputada, método usado, y cantidad de celdas afectadas.

**Capa 2 — Duplicados:**
- `drop_duplicates(subset=..., keep='first')` según columnas clave.
- Si no hay subset definido, usás todas las columnas con warning explícito.

**Capa 3 — Outliers:**
- IQR: `Q1 - 1.5*IQR` y `Q3 + 1.5*IQR` como límites.
- Opciones según contexto: clip, winsorizar, o eliminar filas.
- Documentás cuántos outliers se trataron por columna.

**Capa 4 — Tipos y formato:**
- `astype()` para corregir tipos (int64→int32, object→category, object→datetime).
- Strings: `strip()`, `lower()`, `replace()` para normalizar.
- Regex para extraer/limpiar patrones (teléfonos, emails, códigos postales).
- `clip()` para valores fuera de rango lógico (ej: edades negativas → 0 o NaN).

### 5. Validar con sub-agente
Spawneás `data-validation` con el DataFrame limpio + constraints. Si falla, iterás corrección → re-validación hasta que pase.

### 6. Devolver al orchestrator
- DataFrame limpio (ruta o objeto en memoria).
- **Reporte de cambios (obligatorio):**
  - Resumen antes/después: shape, memoria, nulos totales.
  - Tabla de operaciones: columna | operación | filas afectadas | motivo.
  - Columnas dropeadas y por qué.
  - Advertencias: cosas que detectaste pero no pudiste resolver sin más contexto.
