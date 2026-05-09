# Patterns: API Integration Cheat Sheet

## Request con headers y auth

```python
import requests
session = requests.Session()
session.headers.update({"Authorization": "Bearer <token>", "Accept": "application/json"})
resp = session.get(url, params={"limit": 100}, timeout=30)
resp.raise_for_status()
data = resp.json()
```

## Paginación offset vs cursor

```python
# Offset
items = []
for offset in range(0, 10000, 100):
    r = session.get(url, params={"offset": offset, "limit": 100})
    batch = r.json()["data"]
    if not batch: break
    items.extend(batch)

# Cursor
cursor, items = None, []
while True:
    r = session.get(url, params={"cursor": cursor})
    batch = r.json()
    items.extend(batch["items"])
    cursor = batch.get("next_cursor")
    if not cursor: break
```

## Rate limiting y backoff

```python
from time import sleep
def rate_limited_get(url, delay=1.0):
    resp = session.get(url)
    if resp.status_code == 429:
        wait = int(resp.headers.get("Retry-After", 10))
        sleep(wait + 1)
        return rate_limited_get(url, delay)
    sleep(delay)
    return resp
```

## Retry con tenacity

```python
from tenacity import retry, stop_after_attempt, wait_exponential
@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=60))
def fetch(url):
    r = session.get(url, timeout=30)
    r.raise_for_status()
    return r.json()
```

## JSON → DataFrame

```python
import pandas as pd
df = pd.json_normalize(data, record_path="items", meta=["total"])
# Sin record_path para aplanar todo:
df = pd.json_normalize(data)
```

## Manejo de errores HTTP

```python
try:
    r = session.get(url, timeout=30)
    r.raise_for_status()
except requests.exceptions.Timeout:
    print("Timeout — reintentando con más margen")
except requests.exceptions.HTTPError as e:
    if r.status_code == 401: raise Exception("Token expirado")
    if r.status_code == 429: raise Exception("Rate limit alcanzado")
    raise e
```

## Guardar resultado

```python
df.to_parquet("datos.parquet", index=False)       # preferido
df.to_csv("datos.csv", index=False)                # portátil
df.to_sql("tabla", conn, if_exists="replace")      # consultable
```
