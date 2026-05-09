# Workflow: Regex Data

## Flujo principal

```
Orchestrator → [1. Identificar] → [2. Escribir y testear] → [3. Documentar] → [4. Aplicar] → [5. Validar] → Orchestrator
```

## Paso a paso

### 1. Identificar el patrón a extraer/validar

Leés el prompt del orchestrator y clarificás:

- **¿Qué buscás?** Extraer información, validar formato, limpiar ruido, normalizar, o splitear.
- **¿Sobre qué columna?** Nombre, tipo (`dtype`), muestra de valores reales (primeras y últimas filas, únicos frecuentes).
- **¿Qué formato tiene el dato?** Ejemplos concretos del orchestrator o inspeccionás la columna con `.head(20)` y `.value_counts().head(10)`.
- **¿Casos borde?** Nulos, strings vacíos, formatos alternativos válidos, datos parciales.

Si el patrón no está claro, **preguntás**. No adivinás. "Che, veo teléfonos con y sin prefijo, ¿querés capturar ambos o solo los que tienen +54?"

### 2. Escribir la regex incrementalmente y testear

No escribís el patrón entero de una. Armás por partes, testeás, iterás.

```python
import re

# Empezá con la parte más específica del patrón
patron = r'\d{2,4}'  # probá solo el prefijo
# Después agregás el resto
patron = r'[\d\s\-\(\)]{7,}'  # probá estructura general
# Finalmente armás el patrón completo con grupos
```

**Kit de prueba mínimo para cada regex:**

```python
# Casos positivos — DEBEN matchear
positivos = [
    "juan@empresa.com",
    "maria.lopez@org.gob.ar",
]
# Casos negativos — NO deben matchear
negativos = [
    "no-es-email",
    "faltapunto@incompleto",
    "",
    None,
]

patron = re.compile(r'...')
for p in positivos:
    assert patron.search(p), f"FALLA positivo: {p}"
for n in negativos:
    if n is not None:
        assert not patron.search(n), f"FALLA negativo: {n}"
```

### 3. Documentar la regex con verbose mode

Si la regex tiene más de 20 caracteres, la pasás a `re.VERBOSE` con comentarios. Sin excepción.

```python
EMAIL_RE = re.compile(r"""
    (?P<usuario>                       # Grupo: parte local
        [A-Za-z0-9._%+-]+              # Caracteres válidos del usuario
    )
    @                                   # Arroba literal
    (?P<dominio>                        # Grupo: dominio
        [A-Za-z0-9.-]+                  # Nombre del dominio
        \.                              # Punto separador
        [A-Za-z]{2,}                    # TLD (mínimo 2 letras)
    )
""", re.VERBOSE | re.IGNORECASE)
```

Cada patrón complejo queda documentado con:
- Nombre descriptivo de la variable (`EMAIL_RE`, `CUIL_RE`, `PRECIO_ARS_RE`).
- Grupos con nombre (`(?P<nombre>...)`) para acceder por semántica, no por índice mágico.
- Comentarios en cada línea explicando qué captura.

### 4. Aplicar a la columna con pandas str

Elegís el método correcto según la operación:

| Operación | Método pandas | Cuándo usarlo |
|-----------|--------------|---------------|
| Extraer | `str.extract(r'...')` | Sacar parte del string (email de un texto) |
| Extraer múltiples | `str.extract(r'(a)(b)(c)')` | Varios grupos → columnas nuevas |
| Validar | `str.match(r'...')` | ¿Empieza con el patrón? |
| Contiene | `str.contains(r'...')` | ¿Tiene el patrón en algún lado? |
| Reemplazar | `str.replace(r'...', 'x', regex=True)` | Limpiar caracteres, normalizar |
| Encontrar todos | `str.findall(r'...')` | Múltiples matches por celda |
| Splitear | `str.split(r'...', expand=True)` | Dividir en columnas |

Si el caso es complejo (lógica condicional, pre-procesamiento), usás `re.compile` + `df['col'].apply()`.

```python
# Ejemplo: extraer email y dominio en dos columnas nuevas
df[['usuario', 'dominio']] = df['texto'].str.extract(EMAIL_RE)
```

### 5. Validar resultados con ejemplos positivos y negativos

No soltás el DataFrame hasta verificar:

- **Cuantitativamente:** ¿Cuántas filas matchearon? ¿Hay nulos nuevos? ¿Coincide con lo esperado?
  ```python
  df['col_extraida'].isnull().mean()  # % de no-matches
  df[df['col_extraida'].isnull()]['col_original'].sample(10)  # ¿qué no matcheó?
  ```

- **Cualitativamente:** Muestra de matches y no-matches para revisión visual.
  ```python
  # Matches
  df[df['col_extraida'].notna()]['col_extraida'].sample(10)
  # No-matches — ¿son legítimos o hay que ajustar la regex?
  df[df['col_extraida'].isnull()]['col_original'].head(20)
  ```

- **Casos borde explícitos:** Si había nulos de entrada, ¿siguen siendo nulos? Si había strings vacíos, ¿se manejaron correctamente?

Si la tasa de no-match es alta (>10%) o hay falsos positivos, volvés al paso 2 y refinás la regex.
