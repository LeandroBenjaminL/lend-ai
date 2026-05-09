---
name: regex-data
description: >
  Expresiones regulares para limpieza y extracción de datos con Python y Pandas.
  Trigger: Cuando necesitás limpiar strings, extraer patrones (emails, teléfonos, precios, fechas), o validar formatos en un DataFrame.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "2.0"
  model_tier: T2-fast
---

# Skill: regex-data

## Para qué sirve

Las expresiones regulares (regex) son patrones para buscar y manipular texto. En data analysis se usan todo el tiempo para limpiar datos sucios, extraer información de strings (emails, teléfonos, precios), y validar formatos. No necesitás ser un genio de regex — con 5-6 patrones básicos resolvés el 90% de los casos.

## Trigger (cuándo cargar esta skill)

- Tenés columnas de texto con formatos inconsistentes (teléfonos, fechas, precios)
- Necesitás extraer información de un string (ej: sacar el dominio de un email)
- Querés validar que los datos cumplan un formato (CUIT, DNI, código postal)
- Tenés que normalizar texto: espacios, acentos, mayúsculas inconsistentes

## Workflow paso a paso

1. **Identificá el patrón**: ¿qué estás buscando? (email, teléfono, fecha, precio)
2. **Escribí el regex**: arrancá con un patrón simple, probalo con un par de ejemplos
3. **Probá en Python**: usá `re.findall()` o `re.match()` en una muestra antes de aplicar a todo el DF
4. **Aplicá al DataFrame**: `.str.extract()`, `.str.replace()`, o `.str.contains()` según lo que necesites
5. **Validá resultados**: revisá algunos valores que NO deberían matchear para asegurarte de que no hay falsos positivos

## Patrones esenciales

### 1. Patrones más usados en data analysis

Acá están los patrones que más vas a usar. Tenelos a mano para no reinventar la rueda cada vez.

```python
import re
import pandas as pd

PATRONES = {
    'email':      r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'telefono':   r'(?:\+54|0)?(?:11|[2-9]\d{1,2})[\s\-]?\d{4}[\s\-]?\d{4}',
    'precio':     r'\$?\s*(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)',
    'fecha':      r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b',
    'dni':        r'\b\d{7,8}\b',
    'cuit':       r'\b\d{2}-\d{8}-\d\b',
    'url':        r'https?://[^\s]+',
    'codigo_postal': r'\b[A-Z]?\d{4}[A-Z]{0,3}\b',
}
```

### 2. Pandas .str — el más usado en data analysis

Los métodos `.str.` de pandas aplican regex a cada celda de una Serie. Son la forma más rápida y limpia de limpiar columnas enteras.

```python
# Extraer parte de un string (ej: dominio del email)
df['dominio'] = df['email'].str.extract(r'@(.+)$')

# Reemplazar caracteres no deseados
df['precio'] = df['precio_texto'].str.replace(r'[$.,\s]', '', regex=True).astype(float)

# Validar formato — devuelve True/False
df['email_valido'] = df['email'].str.match(r'^[^@]+@[^@]+\.[^@]+$')

# Extraer múltiples grupos a la vez
df[['dia', 'mes', 'anio']] = df['fecha'].str.extract(r'(\d{2})/(\d{2})/(\d{4})')

# Filtrar filas que contienen un patrón
df_con_numeros = df[df['codigo'].str.contains(r'\d', regex=True, na=False)]

# Split en columnas
df[['nombre', 'apellido']] = df['nombre_completo'].str.split(r'\s+', n=1, expand=True)
```

### 3. Limpiar texto inconsistente

Los datos de entrada vienen sucios: espacios de más, mayúsculas mezcladas, acentos raros. Esta función normaliza todo en una pasada.

```python
def normalizar_texto(serie: pd.Series) -> pd.Series:
    return (serie
        .str.strip()
        .str.lower()
        .str.replace(r'\s+', ' ', regex=True)          # múltiples espacios → uno
        .str.replace(r'[áàäâ]', 'a', regex=True)        # normalizar acentos
        .str.replace(r'[éèëê]', 'e', regex=True)
        .str.replace(r'[íìïî]', 'i', regex=True)
        .str.replace(r'[óòöô]', 'o', regex=True)
        .str.replace(r'[úùüû]', 'u', regex=True)
        .str.replace(r'[^a-z0-9\s]', '', regex=True)    # sacar caracteres especiales
    )
```

### 4. Extraer precios con formato argentino

El problema clásico: "$1.234,56" tiene punto de miles y coma decimal. Hay que normalizarlo.

```python
def precio_a_float(valor) -> float | None:
    if pd.isna(valor):
        return None
    limpio = re.sub(r'[^\d.,]', '', str(valor))
    if ',' in limpio and '.' in limpio:
        limpio = limpio.replace('.', '').replace(',', '.')  # 1.234,56 → 1234.56
    elif ',' in limpio:
        limpio = limpio.replace(',', '.')
    return float(limpio) if limpio else None

df['precio'] = df['precio_texto'].apply(precio_a_float)
```

## Alternativas

- **re (stdlib) vs regex**: El módulo `regex` (pip install regex) soporta Unicode avanzado, lookbehind variable, y es más potente que `re`. Instalalo si necesitás features avanzadas.
- **Pandas .str vs apply con re**: `.str.extract()` y `.str.replace()` son vectorizados (rápidos). `apply()` con `re.search()` es más flexible pero más lento. Preferí `.str.*` primero.
- **Regex vs métodos específicos**: Para fechas, usá `pd.to_datetime()`. Para URLs, `urllib.parse`. Para JSON, `json` module. Regex es el martillo — no todo es un clavo.

## Anti-patrones

- ❌ **Regex demasiado complejo**: Si tu regex tiene más de 50 caracteres y no lo entendés ni vos, dividilo en pasos. Un `str.extract()` simple + otro `str.replace()` es más mantenible que un regex monstruo.
- ❌ **No escapar puntos**: `e.mail.com` matchea con el regex `e.mail.com` porque `.` significa "cualquier caracter". Usá `\.` para matchear un punto literal.
- ❌ **Aplicar regex sin probar antes**: `df['col'].str.extract(r'regex_complejo')` sin probar en 3-4 ejemplos puede darte resultados erróneos sin que te des cuenta. Probá siempre con `re.findall()` en una muestra.
- ❌ **Olvidar `na=False`**: `.str.contains(r'\d', na=False)` — si hay nulos, `str.contains` devuelve NaN sin `na=False` y rompe filtros booleanos.

## Comandos

```python
# Probar un regex rápido
import re
texto = "Mi email es juan@empresa.com.ar y mi tel es 011-4567-8901"
emails = re.findall(r'\b[\w.+-]+@[\w-]+\.[\w.-]+\b', texto)
print(emails)  # ['juan@empresa.com.ar']

# Ver todos los matches con posición
for m in re.finditer(r'\d+', 'ventas: 1234, costos: 567'):
    print(f'{m.group()} en posición {m.start()}')
```
