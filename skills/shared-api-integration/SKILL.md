---
name: api-integration
description: >
  Consumo de APIs REST externas para obtener datos de fuentes públicas.
  Trigger: Cuando necesitás traer datos de APIs, hacer requests HTTP, o integrar servicios externos.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "2.0"
  model_tier: T2-fast
---

# Skill: api-integration

## Para qué sirve

Obtener datos de APIs REST externas de forma confiable. El 90% de las APIs públicas funcionan con JSON sobre HTTP. El truco está en manejar bien los errores, la rate limiting, y aplanar la respuesta JSON a un DataFrame sin volverte loco.

## Trigger (cuándo cargar esta skill)

- Necesitás datos de APIs públicas (clima, finanzas, gov, redes sociales)
- Querés automatizar extracción periódica desde servicios REST
- Tenés que combinar datos de múltiples fuentes externas
- Vas a consumir una API con autenticación (API keys, tokens)

## Workflow paso a paso

1. **Leé la documentación**: endpoint base, headers, auth, rate limits, paginación
2. **Probá el request básico** con `curl` o en el navegador primero
3. **Escribí la función de request** con retry, timeout, y manejo de errores
4. **Aplaná el JSON** a DataFrame — los JSON de APIs suelen tener anidamiento
5. **Manejá la paginación** si la API devuelve resultados limitados por página
6. **Respetá el rate limit** — las APIs te banquean si hacés muchas requests seguidas

## Patrones esenciales

### 1. Request con retry y timeout

Las APIs fallan. Cortes de red, servidores sobrecargados, rate limits. Un retry con backoff exponencial (esperar 2s, 4s, 8s) suele resolver la mayoría de los failures transitorios.

```python
import requests
from time import sleep

def fetch_api(url, params=None, headers=None, retries=3, timeout=30):
    """GET con retry y backoff exponencial"""
    for attempt in range(retries):
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=timeout)
            resp.raise_for_status()  # lanza excepción si status >= 400
            return resp.json()
        except requests.exceptions.RequestException as e:
            if attempt == retries - 1:
                raise
            wait = 2 ** attempt
            print(f"  Error (intento {attempt+1}), esperando {wait}s: {e}")
            sleep(wait)
```

**¿Por qué backoff exponencial?** Porque si la API está caída, mandar requests cada 1 segundo no la va a revivir más rápido. Esperar cada vez más tiempo le da chance al servidor de recuperarse sin saturarlo.

### 2. Aplanar JSON anidado a DataFrame

Las APIs devuelven JSON con estructuras jerárquicas. `pd.json_normalize()` te aplana todo en un solo paso.

```python
import pandas as pd

# Data anidado tipico de API
data = {
    "results": [
        {"id": 1, "nombre": "Juan", "direccion": {"ciudad": "CABA", "calle": "Av. Siempre Viva"}},
        {"id": 2, "nombre": "María", "direccion": {"ciudad": "La Plata", "calle": "Calle 12"}}
    ]
}

# Aplanar automáticamente
df = pd.json_normalize(data, sep='_')
#   id nombre  direccion_ciudad direccion_calle
#   1  Juan    CABA             Av. Siempre Viva
#   2  María   La Plata         Calle 12
```

### 3. Paginación — cuando la API no te da todo de una

La mayoría de las APIs limitan los resultados por página. Tenés que iterar hasta obtener todo.

```python
def fetch_all_paginated(base_url, params=None, headers=None, page_size=100):
    todos = []
    page = 1
    while True:
        params = params or {}
        params.update({'page': page, 'per_page': page_size})
        data = fetch_api(f"{base_url}", params=params, headers=headers)
        if not data:  # sin más resultados
            break
        todos.extend(data)
        page += 1
        sleep(0.5)  # respetar rate limit
    return todos
```

### 4. API con autenticación (API Key / Bearer Token)

```python
headers = {
    'Authorization': 'Bearer sk-xxx',  # o 'X-API-Key': 'tu-key'
    'User-Agent': 'Mi-app/1.0'
}
df = pd.read_json('https://api.ejemplo.com/v1/datos', storage_options=headers)
```

## Ejemplos completos

```python
# 1. Clima (API pública sin auth)
resp = requests.get('https://api.weather.gov/points/34.05,-118.25')
data = resp.json()
print(data['properties']['forecast'])

# 2. Datos Argentina (API gov)
resp = requests.get('https://datos.gob.ar/api/3/action/package_list')
datasets = resp.json()['result']
print(f"Datasets: {len(datasets)}")

# 3. Crypto (paginación con pandas directamente)
df = pd.read_json('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd')
print(df[['name', 'current_price', 'market_cap']].head())
```

## Alternativas

- **requests vs httpx**: `httpx` tiene soporte async nativo. Si hacés muchas requests concurrentes, httpx es hasta 10x más rápido.
- **pandas.read_json vs requests + json_normalize**: Si la API devuelve un JSON plano o con estructura simple, `pd.read_json(url)` es más directo. Para JSON anidado, usá `requests` + `json_normalize`.
- **APIs GraphQL**: Algunas APIs modernas usan GraphQL (un solo endpoint, consultas flexibles). Necesitás mandar un POST con query en el body.

## Anti-patrones

- ❌ **Sin timeout**: `requests.get(url)` sin `timeout` puede colgarse para siempre si el servidor no responde. Siempre poné `timeout=30`.
- ❌ **Ignorar rate limits**: Mandar 100 requests por segundo a una API que permite 10. Te van a banear la IP. Usá `sleep()` entre requests o implementá backoff.
- ❌ **No verificar status code**: Asumir que el request siempre funciona. Usá `raise_for_status()` o verificá `resp.status_code`.
- ❌ **API keys hardcodeadas**: `api_key = "sk-12345"` en el código. Usá variables de entorno siempre.
- ❌ **No manejar paginación**: Quedarte con los primeros 20 resultados cuando hay 10,000 y no saberlo.

## Comandos

```bash
pip install requests httpx

# Probar API rápido
curl https://api.publicapis.org/entries | python -m json.tool | head -20
```
