# Workflow: Data Archive

## Flujo principal

```
Orchestrator → [1. Revisar] → [2. Documentar] → [3. Limpiar] → [4. Versionar] → [5. README] → [6. Archivar] → Orchestrator
```

## Paso a paso

### 1. Revisar qué se hizo en el proyecto

Leer el prompt del orchestrator y hacer un barrido inicial del directorio del proyecto. Entender:

- **Pregunta de negocio:** ¿qué se quiso responder?
- **Datos usados:** fuentes, formato, tamaño, período, ubicación (`raw/` vs `data/`).
- **Enfoque:** ¿análisis exploratorio, modelo de ML, pipeline ETL, dashboard, reporte?
- **Entregables:** ¿qué outputs se generaron? (gráficos, reportes, modelos entrenados, datasets procesados).
- **Dependencias:** ¿hay `requirements.txt`, `environment.yml`, `pyproject.toml`? ¿Está actualizado?

Si el proyecto está en un estado caótico (archivos sueltos, sin estructura clara, notebooks sin nombre), lo señalás explícitamente. No podés archivar sin ordenar primero.

### 2. Documentar decisiones clave y tradeoffs

Antes de tocar un solo archivo, documentás:

- **Decisiones de diseño:** ¿por qué se eligió ese modelo y no otro? ¿por qué se imputó con mediana y no con KNN? ¿por qué se dropeó esa feature?
- **Tradeoffs:** "Elegimos Random Forest sobre XGBoost porque priorizamos interpretabilidad sobre 2% de accuracy extra."
- **Limitaciones:** "Los datos solo cubren hasta diciembre 2025, cualquier predicción más allá de esa fecha es especulación."
- **Aprendizajes:** "Si arrancáramos de nuevo, haríamos el feature engineering ANTES del split train/test para evitar leakage."

Esta documentación va al README de cierre y también se guarda en Engram como memoria persistente del proyecto.

### 3. Limpiar archivos temporales e intermedios

Revisión quirúrgica del directorio:

- **Notebooks:** correr `nbstripout` para eliminar outputs. Un notebook commiteado con outputs es una bomba de diffs.
- **Archivos temporales:** eliminar `*.tmp`, `*.bak`, `*_old`, `*_v2_final_FINAL.csv`, y todo lo que huela a "esto era para probar".
- **Datasets intermedios:** si `processed/` tiene 15 versiones del mismo CSV, dejás solo la final. Las versiones de prueba no se archivan.
- **Outputs de debugging:** `debug_*.csv`, `print(df.head())` sueltos, screenshots en la raíz del proyecto — fuera.
- **Variables de entorno:** asegurarse de que `.env` esté en `.gitignore` y que no haya API keys hardcodeadas en notebooks.
- **Archivos grandes:** verificar `.gitignore` para datasets pesados (>100MB). Si no está, lo agregás y usás `git rm --cached`.

Si encontrás algo que no sabés si es basura o tesoro, consultás al orchestrator antes de borrar. Regla de oro: ante la duda, preguntar.

### 4. Versionar código final y datasets procesados

Todo lo que sobrevive la limpieza se versiona:

- **Código:** asegurarse de que los notebooks estén ejecutables de principio a fin (restart & run all). Si algo falla, lo reportás.
- **Datasets:** los procesados se guardan en Parquet (más eficiente que CSV, preserva tipos). Si el dataset es muy grande, considerás compresión o splitteo.
- **Modelos entrenados:** si hay `.pkl`, `.joblib`, `.h5`, se guardan en `models/` con nombre descriptivo y fecha.
- **requirements.txt** actualizado: correr `pip freeze > requirements.txt` dentro del entorno del proyecto.
- **Git commit:** mensaje claro, sin ambigüedades. Ej: `"archivo: cierre de análisis de churn Q1 2025. Modelo final: XGBoost, AUC 0.87"`.

### 5. Crear README de cierre

Este es el paso más importante. El README de cierre es el mapa que va a usar cualquier persona (incluido tu yo del futuro) para entender y reproducir el proyecto. Usás la estructura definida en patterns.md.

El README va en la raíz del proyecto y debe responder:
- ¿Qué problema resolvimos?
- ¿Qué datos usamos?
- ¿Qué hicimos y por qué?
- ¿Qué encontramos?
- ¿Cómo se reproduce?
- ¿Qué haríamos distinto?

### 6. Archivar en storage final

- **Git:** commit final con el README, push al remoto. Si el proyecto estaba en una rama, merge a `main` (o lo que defina el orchestrator).
- **Engram:** guardar memoria con los hallazgos clave y la ubicación del repo.
- **Datos grandes:** si hay datasets que no entran en git (>100MB), se documenta dónde están almacenados (S3, GCS, Drive, NAS).
- **Confirmación:** devolvés al orchestrator un resumen de lo archivado, con paths relativos, commit hash, y cualquier advertencia que haya quedado pendiente.
