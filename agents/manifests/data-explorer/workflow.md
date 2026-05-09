# Workflow: Data Explorer (EDA)

## Skills disponibles

Cargá según la tarea:
- `data-analysis` → manipulación pesada con Pandas/NumPy (solo si no alcanza con pandas básico)
- `data-profiling` → perfil automático con ydata-profiling (para reporte rápido de calidad)
- `data-visualization` → gráficos con matplotlib/seaborn/plotly
- `regex-data` → limpieza de texto con expresiones regulares
- `file-formats` → lectura/escritura de formatos específicos (Parquet, Excel, JSON)

## Flujo principal

```
Orchestrator → [1. Cargar] → [2. Perfil rápido] → [3. Profundizar] → [4. Hipótesis] → [5. Reportar] → Orchestrator
```

## Paso a paso

### 1. Cargar datos
- Leer archivo con pandas según formato (CSV, Excel, Parquet, JSON)
- Mostrar `shape`, `dtypes`, memoria usada, tiempo de carga
- Si es grande, mostrar solo muestra del head/tail

### 2. Perfil rápido (sanity check)
- `df.info()`, `df.isnull().sum()`, `df.duplicated().sum()`
- `df.describe(include='all')` con transposición
- Detectar: tipos incorrectos, nulos ocultos, columnas constantes, IDs

### 3. Profundizar
Para columnas numéricas:
- Histogramas + boxplots (distribución, outliers, skewness)
- Matriz de correlación (heatmap) si hay 3+ numéricas

Para columnas categóricas:
- Value counts con frecuencia relativa
- Cardinalidad vs tamaño total del dataset

Para series temporales (si aplica):
- Tendencia, estacionalidad, residuos

### 4. Generar hipótesis
- Relaciones potenciales entre variables
- Outliers y su posible explicación
- Patrones estacionales o de agrupamiento
- Columnas candidatas a feature engineering

### 5. Reportar
Devolver estructura clara:
- 🟢 Todo bien
- ⚠️ Cosas para mirar
- 🔴 Problemas que requieren acción
- Hipótesis iniciales para el análisis
