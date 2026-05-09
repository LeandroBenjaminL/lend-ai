# Workflow: Análisis de Perfil de Datos

Seguí estos 5 pasos en orden. Cada paso avanza en profundidad; no saltees ninguno.

---

## Paso 1: Primer contacto — shape, tipos, memoria

**Objetivo:** Entender la estructura del dataset en segundos.

```python
import pandas as pd
import numpy as np

df = pd.read_csv("dataset.csv")  # o el formato que corresponda
```

Qué mirar:
- `df.shape` — filas × columnas
- `df.dtypes` — tipos de cada columna, identificar categóricas vs numéricas
- `df.memory_usage(deep=True).sum() / 1024**2` — tamaño en MB
- `df.head(3)` y `df.tail(3)` — primeras/últimas filas para detectar encabezados raros, footers, o datos basura al final

Salida esperada: un panorama general en 2-3 líneas. Ej: _"15 columnas, 250k filas, 18 MB. 8 numéricas, 5 categóricas, 2 datetime. Sin encabezados raros."_

---

## Paso 2: Reporte automático — ydata-profiling o sweetviz

**Objetivo:** Generar un reporte HTML completo sin escribir código manual.

**Decisión:** ¿cuál usar?

| Herramienta | Cuándo |
|---|---|
| `ydata-profiling` | Dataset único, querés reporte exhaustivo con alertas automáticas |
| `sweetviz` | Querés comparar dos datasets (train/test, antes/después de limpieza) o segmentos |

```python
# Opción A: ydata-profiling
from ydata_profiling import ProfileReport
profile = ProfileReport(df, title="Perfil de Dataset", explorative=True)
profile.to_file("reporte_profiling.html")

# Opción B: sweetviz
import sweetviz as sv
reporte = sv.analyze(df)
reporte.show_html("reporte_sweetviz.html")
```

Si el dataset es grande (>100k filas), usá `minimal=True` en ydata-profiling para que no se cuelgue.

Salida esperada: archivo HTML con visualizaciones, stats, alertas y correlaciones.

---

## Paso 3: Identificar anomalías

**Objetivo:** Detectar todo lo que está fuera de lugar antes de seguir.

Checklist obligatorio — respondé cada una con números:

- [ ] **Nulos:** ¿qué columnas tienen nulos? ¿qué porcentaje? Si +60%, considerar dropear la columna.
- [ ] **Duplicados:** ¿hay filas duplicadas? ¿cuántas? ¿son duplicados reales o IDs repetidos?
- [ ] **Cardinalidad alta:** ¿hay categóricas con +90% de valores únicos? Posible ID mal tipeado.
- [ ] **Outliers:** en numéricas, ¿hay valores extremos según IQR (3×)? ¿son errores o datos legítimos?
- [ ] **Distribuciones raras:** ¿columnas con un solo valor (constantes)? ¿skewness extremo? ¿distribuciones bimodales?
- [ ] **Correlaciones sospechosas:** ¿columnas con correlación 0.99+ (redundantes)? ¿features que deberían estar correlacionadas y no lo están?
- [ ] **Tipos incorrectos:** ¿números como strings? ¿fechas como strings? ¿booleanos como 0/1 en vez de bool?
- [ ] **Valores centinela:** ¿-1, -999, "N/A", "missing" como marcadores de nulo que pandas no detecta?

Salida esperada: lista priorizada de hallazgos. Lo más crítico primero. Con números, no opiniones.

---

## Paso 4: Análisis dirigido a anomalías

**Objetivo:** Investigar a fondo los problemas detectados en el paso 3.

Para cada anomalía encontrada, profundizá:

- **Nulos por columna:** ¿hay patrón? ¿son aleatorios (MAR, MCAR)? ¿correlacionan con otra columna?
- **Outliers:** ¿son de una categoría particular? ¿un rango de fechas? ¿un lote de datos mal cargado?
- **Correlaciones raras:** graficá scatter plots de las parejas sospechosas. ¿Es relación espuria por una tercera variable?
- **Cardinalidad alta:** ¿esa columna de 100k valores únicos tiene sentido como categórica o es una clave primaria?

Salida esperada: explicación de cada anomalía con evidencia visual y numérica.

---

## Paso 5: Entregar reporte final

**Objetivo:** Cerrar con un resumen ejecutivo + reporte HTML.

El resumen final incluye:

1. **Ficha técnica:** filas, columnas, tipos, tamaño, % nulos global
2. **Top 3-5 hallazgos:** los más relevantes, explicados en una frase cada uno
3. **Recomendaciones:** qué columnas dropear, cuáles necesitan limpieza, qué transformaciones se sugieren
4. **Reporte HTML:** adjuntar ruta al archivo generado

Ejemplo de cierre:

> _"Dataset de 250k filas y 15 columnas. Tres hallazgos clave: (1) la columna 'customer_id' tiene 99.8% de unicidad — es una PK, no un feature; (2) 'income' tiene 23% de nulos, todos pertenecen al segmento 'student'; (3) 'signup_date' y 'first_purchase_date' tienen correlación 0.97 — una de las dos es redundante. El reporte completo está en `reporte_profiling.html`."_
