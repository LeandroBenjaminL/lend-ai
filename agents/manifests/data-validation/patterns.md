# Patterns: Data Validation Cheat Sheet

## Elección de herramienta

| Herramienta | Para | Contra |
|---|---|---|
| **Pydantic** | APIs, modelos, registros individuales | Por fila — lento para DataFrames grandes |
| **Pandera** | DataFrames, batches, análisis | Solo pandas (no Spark nativo) |
| **Great Expectations** | Pipelines productivos, documentación viva | Setup más pesado, overhead para tareas simples |

---

## Pandera — Schema para DataFrames

### Schema básico con checks

```python
import pandera as pa
from pandera import DataFrameSchema, Column, Check
import pandas as pd

schema = DataFrameSchema({
    'id': Column(int, Check.greater_than(0), nullable=False, unique=True),
    'nombre': Column(str, Check.str_length(1, 100), nullable=False),
    'edad': Column(int, Check.in_range(0, 120), nullable=True),
    'email': Column(str, Check.str_matches(r'^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$'), nullable=False),
    'salario': Column(float, Check.greater_than_or_equal_to(0), nullable=True),
    'fecha': Column(pd.DatetimeTZDtype, nullable=True),
    'categoria': Column(str, Check.isin(['A', 'B', 'C']), nullable=False),
})
```

### Validación lazy (todos los errores juntos)

```python
try:
    validated_df = schema.validate(df, lazy=True)
except pa.errors.SchemaErrors as e:
    print(f"❌ {len(e.failure_cases)} fallos de validación")
    print(e.failure_cases[['column', 'check', 'failure_case', 'index']])
```

### Inferir schema desde referencia

```python
# Inferir y validar en 2 líneas
schema = pa.infer_schema(df_referencia)
validated = schema.validate(df_nuevo, lazy=True)
```

### Schema compuesto (múltiples columnas)

```python
# Check que involucra 2 columnas
schema = DataFrameSchema(
    columns={
        'fecha_inicio': Column(pd.DatetimeTZDtype),
        'fecha_fin': Column(pd.DatetimeTZDtype),
        'total': Column(float),
        'cantidad': Column(int),
        'precio_unitario': Column(float),
    },
    checks=[
        Check(lambda df: (df['fecha_fin'] >= df['fecha_inicio']).all(),
              name='fecha_fin >= fecha_inicio'),
        Check(lambda df: (df['total'] == df['cantidad'] * df['precio_unitario']).all(),
              name='total = cantidad * precio_unitario', element_wise=True),
    ]
)
```

### Exportar / importar schema

```python
# Guardar como YAML
schema.to_yaml('schema_usuarios.yaml')

# Cargar desde YAML
schema = pa.io.from_yaml('schema_usuarios.yaml')
```

---

## Pydantic — Validación para APIs y modelos

### BaseModel con validación por campo

```python
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import date

class UsuarioModel(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    edad: Optional[int] = Field(None, ge=0, le=120)
    salario: Optional[float] = Field(None, ge=0)
    fecha_registro: date
    categoria: str = Field(..., pattern='^[A-C]$')

    @field_validator('fecha_registro')
    @classmethod
    def fecha_no_futura(cls, v):
        if v > date.today():
            raise ValueError('La fecha de registro no puede ser futura')
        return v
```

### Validar fila por fila (DataFrame → Pydantic)

```python
errores = []
for idx, row in df.iterrows():
    try:
        UsuarioModel(**row.to_dict())
    except Exception as e:
        errores.append({'fila': idx, 'error': str(e)})

if errores:
    print(f"❌ {len(errores)} filas con errores de validación")
else:
    print("✅ Todas las filas pasaron la validación")
```

### Pydantic v2 (field_validator)

```python
from pydantic import field_validator

@field_validator('email')
@classmethod
def validar_email(cls, v):
    if '@' not in v or '.' not in v.split('@')[-1]:
        raise ValueError('Email inválido')
    return v.strip().lower()
```

---

## Great Expectations — Expectations para pipelines

### Estructura conceptual

```python
import great_expectations as gx

context = gx.get_context()

# Crear suite de expectations
validator = context.sources.pandas_default.read_csv('datos.csv')

validator.expect_column_values_to_not_be_null('id')
validator.expect_column_values_to_be_unique('id')
validator.expect_column_values_to_be_between('edad', min_value=0, max_value=120)
validator.expect_column_values_to_match_regex('email', r'^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$')
validator.expect_column_values_to_be_in_set('categoria', ['A', 'B', 'C'])
validator.expect_column_mean_to_be_between('salario', min_value=1000, max_value=50000)

# Ejecutar y guardar
validator.save_expectation_suite()
```

---

## Catálogo de checks comunes

### Null checks

```python
# Pandera
Column(str, nullable=False)
Check(lambda s: s.isna().sum() / len(s) <= 0.05, name='nulos_max_5%')

# Pydantic
nombre: str = Field(...)          # required, no null
edad: Optional[int] = Field(None) # nullable
```

### Range checks

```python
# Pandera
Check.in_range(0, 120)
Check.greater_than_or_equal_to(0)

# Pydantic
edad: int = Field(ge=0, le=120)
precio: float = Field(gt=0)
```

### Unique checks

```python
# Pandera
Column(int, unique=True)

# Combinación única (compound key)
Check(lambda df: ~df[['codigo', 'sucursal']].duplicated().any(),
      name='unique_codigo_sucursal')
```

### Regex / format validation

```python
# Pandera
Check.str_matches(r'^\d{2}-\d{8}-\d{1}$')  # CUIT argentino

# Pydantic
Field(..., pattern=r'^\d{2}-\d{8}-\d{1}$')
```

### Set membership (valores permitidos)

```python
# Pandera
Check.isin(['pendiente', 'aprobado', 'rechazado'])

# Pydantic
from enum import Enum
class Estado(str, Enum):
    pendiente = 'pendiente'
    aprobado = 'aprobado'
    rechazado = 'rechazado'
```

### Custom validators

```python
# Pandera — función lambda o función externa
Check(lambda s: s.str.len().between(1, 100).all(), name='str_length')

def es_cuit_valido(series):
    return series.astype(str).str.match(r'^\d{2}-\d{8}-\d{1}$')
Check(es_cuit_valido, name='cuit_valido')

# Pydantic
@field_validator('cuit')
@classmethod
def validar_cuit(cls, v):
    # Lógica de dígito verificador
    if not cuit_es_correcto(v):
        raise ValueError('CUIT inválido')
    return v
```

---

## Reporte de calidad rápido (sin librerías externas)

```python
def reporte_calidad(df):
    import pandas as pd
    return pd.DataFrame({
        'columna': df.columns,
        'tipo': df.dtypes.values,
        'nulos': df.isna().sum().values,
        '%_nulos': (df.isna().sum() / len(df) * 100).round(1).values,
        'unicos': [df[c].nunique() for c in df.columns],
        'min': [df[c].min() if df[c].dtype in ('int64', 'float64') else None for c in df.columns],
        'max': [df[c].max() if df[c].dtype in ('int64', 'float64') else None for c in df.columns],
        'ejemplo': [df[c].dropna().iloc[0] if not df[c].dropna().empty else None for c in df.columns],
    })
```

---

## Reglas de oro de validación

1. **Validá temprano.** Apenas los datos entran al pipeline, no al final cuando ya generaste 3 agregaciones sobre basura.
2. **Nunca validés en modo fail-fast** (salvo que lo pidan). `lazy=True` siempre — mostrá todos los errores juntos.
3. **Cada regla tiene un nombre descriptivo.** `Check(..., name='edad_entre_0_y_120')` — en 6 meses ese nombre te salva.
4. **El schema es código.** Versioná los schemas en git junto con el pipeline. Un schema es tan parte del sistema como una función de transformación.
5. **Documentá edge cases.** "Esta columna es `float` pero históricamente vino con strings vacíos que imputamos a 0" — eso no se adivina, se documenta.
6. **No valides lo que no entendés.** Si no sabés qué rango tiene sentido para una variable de negocio, preguntá al SME antes de poner `Check.in_range(0, 999999)`.
