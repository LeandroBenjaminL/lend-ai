# Patterns: Regex Data Cheat Sheet

## Métodos pandas str — cuándo usar cada uno

```python
# EXTRAER — sacar parte del string a una columna nueva
df['dominio'] = df['email'].str.extract(r'@(.+)$')

# EXTRAER múltiples grupos — cada grupo va a su propia columna
df[['cod_area', 'numero']] = df['tel'].str.extract(r'\(?(\d{2,4})\)?[\s\-]?(\d{6,8})')

# VALIDAR — ¿el string entero matchea el patrón?
df['es_email'] = df['email'].str.match(r'^[^@]+@[^@]+\.[^@]+$')

# CONTIENE — ¿el patrón aparece en algún lado?
df['tiene_descuento'] = df['descripcion'].str.contains(r'\d{1,3}%', regex=True)

# REEMPLAZAR — limpiar o normalizar
df['precio'] = df['precio_texto'].str.replace(r'[$.]', '', regex=True)
df['nombre'] = df['nombre'].str.replace(r'\s+', ' ', regex=True)  # multi-espacio → uno

# SPLIT — dividir en columnas
df[['nombre', 'apellido']] = df['nombre_completo'].str.split(r'\s+', n=1, expand=True)

# STRIP — sacar espacios o caracteres de los extremos
df['codigo'] = df['codigo'].str.strip()

# FINDALL — todos los matches en cada celda (devuelve lista)
df['numeros'] = df['texto'].str.findall(r'\d+')
```

## re.compile con VERBOSE — el estándar para patrones complejos

```python
import re

# SIN verbose (ilegible a los 3 días)
FECHA_RE = re.compile(r'(\d{4})-(\d{2})-(\d{2})')

# CON verbose (se entiende siempre)
FECHA_RE = re.compile(r"""
    (?P<año>\d{4})      # 4 dígitos para el año
    -                     # guión separador literal
    (?P<mes>\d{2})       # 2 dígitos para el mes (01-12)
    -                     # guión separador literal
    (?P<dia>\d{2})       # 2 dígitos para el día (01-31)
""", re.VERBOSE)

# Uso con apply para lógica compleja
def extraer_fecha_iso(texto):
    m = FECHA_RE.search(str(texto))
    return m.group('dia') + '/' + m.group('mes') + '/' + m.group('año') if m else None

df['fecha_arg'] = df['texto'].apply(extraer_fecha_iso)
```

## Grupos con nombre (?P<name>...) — nunca índices mágicos

```python
# ❌ Grupos por índice — ilegible y frágil
m = re.search(r'(\d{2})-(\d{8})-(\d)', cuit)
tipo, numero, digito = m.group(1), m.group(2), m.group(3)  # ¿qué es 1, 2, 3?

# ✅ Grupos con nombre — semántico y mantenible
CUIL_RE = re.compile(r"""
    (?P<tipo>\d{2})      # 20, 23, 24, 27
    -
    (?P<numero>\d{8})    # DNI de la persona
    -
    (?P<digito>\d)       # Dígito verificador
""", re.VERBOSE)

m = CUIL_RE.search(cuit)
tipo = m.group('tipo')
numero = m.group('numero')
digito = m.group('digito')

# En pandas str.extract, los nombres se vuelven columnas automáticamente
df[['tipo', 'numero', 'digito']] = df['cuit'].str.extract(CUIL_RE)
```

## Patrones comunes — batería lista para usar

```python
PATRONES = {
    # Email
    'email': r"""
        (?P<email>
            [A-Za-z0-9._%+-]+     # parte local
            @
            [A-Za-z0-9.-]+        # dominio
            \.
            [A-Za-z]{2,}          # TLD
        )
    """,

    # URL
    'url': r"""
        (?P<url>
            https?://             # protocolo
            [^\s<>"]+             # todo hasta espacio o comilla
        )
    """,

    # Teléfono argentino: +54 11 4567-8901, 011-4567-8901, 15-1234-5678
    'telefono_ar': r"""
        (?P<tel>
            (?:\+54|0)?           # prefijo país (opcional)
            \s?
            (?P<cod_area>11|[2-9]\d{1,2})  # código de área
            [\s\-]?
            (?P<numero>\d{4})     # primera mitad
            [\s\-]?
            (?P<numero2>\d{4})    # segunda mitad
        )
    """,

    # Fecha ISO: 2024-12-31
    'fecha_iso': r"""
        (?P<fecha>
            (?P<año>\d{4})
            -
            (?P<mes>\d{2})
            -
            (?P<dia>\d{2})
        )
    """,

    # Fecha argentina: 31/12/2024, 31-12-2024, 31/12/24
    'fecha_arg': r"""
        (?P<fecha>
            (?P<dia>\d{1,2})
            [/.-]
            (?P<mes>\d{1,2})
            [/.-]
            (?P<año>\d{2,4})
        )
    """,

    # Moneda: $1.234,56 | 1234.56 | USD 99.99
    'precio': r"""
        (?P<precio>
            (?:USD|U\$S|ARS|\$|€)?\s*   # símbolo moneda (opcional)
            (?P<monto>
                \d{1,3}                  # primer bloque
                (?:[.,]\d{3})*           # bloques de miles
                (?:[.,]\d{2})?           # centavos (opcional)
            )
        )
    """,

    # CUIT/CUIL argentino: 20-12345678-9
    'cuit': r"""
        (?P<cuit>
            (?P<tipo>\d{2})      # tipo (20, 23, 24, 27, 30, 33, 34)
            -
            (?P<dni>\d{7,8})     # número de documento
            -
            (?P<dv>\d)           # dígito verificador
        )
    """,

    # DNI argentino (7-8 dígitos, sin puntos)
    'dni': r'\b(?P<dni>\d{7,8})\b',

    # Código postal argentino (viejo: 4 dígitos, nuevo: letra+4dígitos+3letras)
    'codigo_postal_ar': r'\b(?P<cp>[A-Z]?\d{4}[A-Z]{0,3})\b',

    # IP v4
    'ipv4': r"""
        (?P<ip>
            (?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}
            (?:25[0-5]|2[0-4]\d|[01]?\d\d?)
        )
    """,
}
```

## Limpieza de strings — recetas rápidas

```python
# Normalizar whitespace
df['texto'] = (df['texto']
    .str.strip()                          # sacar espacios extremos
    .str.replace(r'\s+', ' ', regex=True) # colapsar múltiples espacios
)

# Normalizar acentos (rioplatense)
ACENTOS = {
    r'[áàäâ]': 'a', r'[éèëê]': 'e', r'[íìïî]': 'i',
    r'[óòöô]': 'o', r'[úùüû]': 'u', r'[ñ]': 'n',
}
for pattern, reemplazo in ACENTOS.items():
    df['texto'] = df['texto'].str.replace(pattern, reemplazo, regex=True)

# Limpiar caracteres no imprimibles
df['texto'] = df['texto'].str.replace(r'[\x00-\x1f\x7f-\x9f]', '', regex=True)

# Quitar puntuación
df['texto'] = df['texto'].str.replace(r'[^\w\s]', '', regex=True)

# Normalizar a minúsculas y sacar tildes de una
df['slug'] = (df['titulo']
    .str.lower()
    .str.replace(r'[áàäâ]', 'a', regex=True)
    .str.replace(r'[éèëê]', 'e', regex=True)
    .str.replace(r'[íìïî]', 'i', regex=True)
    .str.replace(r'[óòöô]', 'o', regex=True)
    .str.replace(r'[úùüû]', 'u', regex=True)
    .str.replace(r'[^a-z0-9]+', '-', regex=True)  # no alfanumérico → guión
    .str.strip('-')
)
```

## Flags útiles de re

```python
re.IGNORECASE  # (?i) — case insensitive
re.VERBOSE     # (?x) — comentarios y whitespace ignorados
re.MULTILINE   # (?m) — ^ y $ matchean inicio/fin de línea
re.DOTALL      # (?s) — . incluye newlines

# Flags combinados
patron = re.compile(r"""...""", re.VERBOSE | re.IGNORECASE | re.MULTILINE)

# En pandas str, algunos flags se pasan inline
df['col'].str.contains(r'(?i)error')  # case insensitive inline
```

## Escape de caracteres especiales

```python
# Si necesitás buscar caracteres literales que son metacaracteres de regex
import re
texto_literal = "$500.00 (descuento)"
patron_seguro = re.escape(texto_literal)  # \$500\.00\ \(descuento\)
```
