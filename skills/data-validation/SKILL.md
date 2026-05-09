---
name: data-validation
description: >
  Validación y calidad de datos con Pydantic, Pandera y Great Expectations.
  Trigger: Cuando necesitás validar esquemas de datos, garantizar calidad, o definir contratos de datos.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "2.0"
  model_tier: T2-fast
---

# Skill: data-validation

Validar datos es **ponerle barreras a la basura**. Si no definís qué es un dato válido, tu pipeline va a procesar cualquier cosa que le llegue — y cuando el resultado sea incorrecto, no vas a saber si el error fue en los datos de entrada o en el análisis.

La clave: validá temprano, validá fuerte. En el borde del sistema, no en el medio del análisis.

## Trigger

- Definís un pipeline ETL y querés garantizar calidad desde la entrada
- Recibís datos de terceros (APIs, clientes, providers) — no confíes, verificá
- Querés documentar expectativas sobre los datos (contrato de datos)
- Un error silencioso te comió horas de debugging y no querés que se repita

## Workflow

### 1. Elegí el nivel de validación
- **Schema**: tipos de datos, columnas obligatorias, rangos
- **Semántica**: valores válidos, formatos de email, IDs existentes
- **Distribución**: rangos esperados, desvíos, proporciones
- **Temporal**: secuencia de fechas, actualizaciones, rezagos

### 2. Elegí la herramienta según el caso
Pandera para schemas de DataFrames. Pydantic para datos tabulares fila por fila. Great Expectations para pipelines grandes con reporting visual.

### 3. Definí las reglas antes de procesar
Las validaciones se escriben cuando diseñás el pipeline, no cuando descubrís que los datos están rotos.

### 4. Decidí cómo actuar ante fallo
¿Parar el pipeline (strict mode)? ¿Seguir pero loguear los errores? ¿Pasar los datos válidos y rechazar los inválidos?

## Patrones y ejemplos

### 1. Pandera — validación de DataFrames (recomendado para pipelines)

```python
import pandera as pa
from pandera import Column, DataFrameSchema, Check

schema = DataFrameSchema({
    'edad': Column(int, Check.between(0, 120), nullable=False),
    'nombre': Column(str, nullable=False),
    'email': Column(str, Check.str_matches(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )),
    'salario': Column(float, Check.greater_than_or_equal_to(0), nullable=True),
})
# validate() devuelve el DataFrame o tira error
try:
    df_valido = schema.validate(df, lazy=True)  # lazy=True acumula todos los errores
except pa.errors.SchemaErrors as e:
    print(e.failure_cases)  # tabla con fila, columna y descripción de cada fallo
```

**¿Por qué Pandera?**: Se integra directo con Pandas, podés decorar funciones con `@pa.check_types`, y define contratos claros. Ideal cuando trabajás con DataFrames en pipelines.

### 2. Pydantic — validación fila por fila

```python
from pydantic import BaseModel, Field, validator

class UsuarioModel(BaseModel):
    id: int
    nombre: str = Field(..., min_length=1, max_length=100)
    email: str
    edad: int | None = Field(None, ge=0, le=120)

    @validator('email')
    def email_valido(cls, v):
        if '@' not in v or '.' not in v.split('@')[-1]:
            raise ValueError('Email inválido')
        return v
```

**¿Por qué Pydantic?**: Validación rica con tipos de Python estándar, mensajes de error claros, y soporte para validadores custom. Ideal cuando recibís datos JSON o necesitás validar registros individuales (ej: API requests).

### 3. Schema inferido desde datos de referencia

```python
# Pandera infiere el schema de un DataFrame que considerás "bueno"
schema = pa.infer_schema(df_referencia)

# Lo aplicás a datos nuevos
schema.validate(df_nuevo, lazy=True)
```

Esto es útil cuando tenés un batch de datos que sabés que está limpio (validado manualmente) y querés asegurarte de que los siguientes batches tengan la misma estructura.

### 4. Reporte rápido de calidad (para exploración inicial)

```python
def reporte_calidad(df):
    """Resume la calidad de cada columna en un DataFrame"""
    return pd.DataFrame({
        'columna': df.columns,
        'tipo': df.dtypes.values,
        'no_nulos': df.notna().sum().values,
        'nulos': df.isna().sum().values,
        '%nulo': (df.isna().sum() / len(df) * 100).values,
        'unicos': [df[c].nunique() for c in df.columns],
        'nulos_duplicados': [df.duplicated(subset=[c]).sum() for c in df.columns],
    })
```

Este reporte no reemplaza la validación con schema, pero te da una foto rápida de qué esperar.

## Alternativas

| Herramienta | Enfoque | Cuándo conviene |
|-------------|---------|----------------|
| **Pandera** | Schema + checks sobre DataFrames | Pipelines Pandas, decoradores `@check_types` |
| **Pydantic** | Modelos por registro | APIs, datos JSON, validación de filas individuales |
| **Great Expectations** | Suites de expectativas + reporting visual | Pipelines grandes, equipos, data contracts formales |
| **Pandera + Great Ex.** | Schema estricto + monitoreo continuo | El combo más completo para producción |

**Recomendación**: para proyectos chicos/medios, Pandera solo alcanza. Para equipos y datos en producción, Great Expectations agrega reporting y evolución de expectativas.

## Anti-patrones

- ❌ **Validar demasiado tarde** — descubrir datos rotos después de 3 horas de procesamiento
- ❌ **Validar todo con el mismo schema** — diferentes fuentes tienen diferentes calidades y requerimientos
- ❌ **Ignorar errores de validación** — hacer `try: validate(df) except: pass` es no validar nada
- ❌ **Schemas demasiado estrictos** — un NaN en una columna nullable no debería romper el pipeline
- ❌ **No versionar los schemas** — cuando los datos cambian, el schema también tiene que evolucionar
- ❌ **Solo validar tipos, no contenido** — un `int` sigue siendo válido aunque tenga valor `-999`
