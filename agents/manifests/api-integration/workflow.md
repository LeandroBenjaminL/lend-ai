# Workflow: API Integration

## Flujo principal

```
Orchestrator → [1. Leer docs] → [2. Autenticar] → [3. Probe] → [4. Paginar] → [5. Rate limit] → [6. Transformar] → [7. Guardar] → Orchestrator
```

## Paso a paso

### 1. Leer documentación de la API
- Si tiene OpenAPI/Swagger: leer el spec, identificar endpoints, parámetros, y modelos de respuesta.
- Si es docs HTML: leer la página de autenticación, los endpoints principales, y los query params.
- Identificar: método HTTP, URL base, path params, query params, headers requeridos, formato de respuesta.
- Anotar límites conocidos: rate limit por minuto/hora, máximo de resultados por página, timeout.

### 2. Autenticación
- **Sin auth**: APIs públicas abiertas — request directo.
- **API Key**: `headers = {"X-API-Key": key}` o `params = {"api_key": key}`. Preferir header sobre query param por seguridad.
- **Bearer Token / JWT**: `headers = {"Authorization": "Bearer <token>"}`. Si el token expira, implementar refresh automático.
- **OAuth 2.0**: identificar grant type (client_credentials, authorization_code). Usar `requests_oauthlib` si es complejo.
- **Basic Auth**: `requests.get(url, auth=(user, pass))` — solo sobre HTTPS.

### 3. Hacer request de prueba
- Un endpoint simple con pocos datos (ej: status, health, o lista con `limit=1`).
- Validar: status code 200, Content-Type JSON, estructura de respuesta esperada.
- Si falla: analizar el error, ajustar auth/headers/URL, reintentar.
- Extraer la ruta hacia los datos reales en el JSON de respuesta (`results`, `data`, `items`, etc.).

### 4. Manejar paginación
- **Offset-based**: `?offset=0&limit=100`. Loop incrementando offset. Detectar fin cuando `len(results) < limit` o respuesta vacía.
- **Cursor-based**: `?cursor=next_token` o `Link` header con `rel="next"`. Más robusto, preferirlo si la API lo ofrece.
- **Page-based**: `?page=1&per_page=100`. Loop incrementando página. Detectar fin cuando no hay más resultados.
- **Tope de seguridad**: siempre poner un `max_pages` o `max_results` para evitar loops infinitos.

### 5. Rate limiting y backoff
- Leer headers de rate limit: `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After`.
- Si la API devuelve 429: esperar `Retry-After` segundos (con margen) y reintentar.
- Si no hay headers de rate limit: usar delay fijo entre requests (ej: `time.sleep(1)`) o backoff exponencial con jitter vía `tenacity`.
- Controlar requests por segundo: `time.sleep(1 / rate_limit)` para APIs con límite conocido.

### 6. Transformar respuesta a DataFrame
- Usar `pd.json_normalize()` para aplanar JSON anidado.
- Si la respuesta es una lista simple: `pd.DataFrame(data)`.
- Para JSONs profundos: navegar la ruta de datos primero (`data["response"]["items"]`), luego normalizar.
- Asegurar tipos correctos: `parse_dates`, `dtype` en la creación del DataFrame.

### 7. Guardar datos
- **CSV**: `df.to_csv("datos.csv", index=False)` — universal, legible.
- **Parquet**: `df.to_parquet("datos.parquet")` — preferido para datasets grandes, preserva tipos.
- **SQLite**: `df.to_sql("tabla", conn, if_exists="replace")` — para consultas posteriores.
- Incluir metadata en el guardado: timestamp, URL de origen, parámetros usados.
