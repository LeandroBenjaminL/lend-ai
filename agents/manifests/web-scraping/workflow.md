# Workflow: Web Scraping

## Flujo principal

```
Orchestrator → [1. Inspeccionar] → [2. Elegir herramienta] → [3. Extraer] → [4. Rate limiting] → [5. Edge cases] → [6. Guardar] → [7. Validar] → Orchestrator
```

## Paso a paso

### 1. Inspeccionar la página objetivo

Antes de escribir una línea de código, hacés reconocimiento:

- **¿Es SPA o SSR?** Abrí la página sin JS (o usá `curl`). Si el contenido está en el HTML inicial → SSR/estático. Si vuelve vacío → SPA, necesitás Puppeteer/Selenium.
- **¿Tiene API?** Network tab → filtrá por XHR/Fetch. Buscá endpoints JSON, GraphQL, `__NEXT_DATA__`, `__NUXT__`, `__INITIAL_STATE__`. Si encontrás API, felicitate y usala — es más rápido, más limpio y más estable que parsear HTML.
- **¿Cómo es la paginación?** ¿Next button con `?page=N`? ¿Infinite scroll con offset? ¿Cursor-based con token? Identificá el patrón antes de codear.
- **¿robots.txt?** `curl https://ejemplo.com/robots.txt`. Respetá los `Disallow` y el `Crawl-delay`.
- **¿Requiere login?** Si es contenido autenticado, evaluá si necesitás manejar sesiones, cookies o tokens.

Si la página ya tiene una API REST/GraphQL documentada o descubrible, **usala**. El scraping de HTML es plan B.

### 2. Elegir la herramienta correcta

| Escenario | Herramienta | ¿Por qué? |
|---|---|---|
| HTML estático, pocas páginas | `requests` + `BeautifulSoup` | Simple, rápido, sin overhead |
| HTML estático, miles de páginas | `Scrapy` | Concurrencia, middleware, pipelines |
| SPA con JS (React/Vue/Angular) | `Puppeteer` (MCP) o `Selenium` | Renderiza JS, espera elementos dinámicos |
| Tablas HTML simples | `pd.read_html()` | Directo a DataFrame, cero código |
| Autenticación compleja, captchas | `Puppeteer` o `Selenium` con stealth | Simula navegador real |
| Sitio con infinite scroll | `Puppeteer` con `page.evaluate()` | Scroll programático hasta que no haya más datos |

### 3. Implementar la extracción

- **Selectores robustos:** Preferí clases semánticas y data attributes sobre paths frágiles. `[data-testid="price"]` sobrevive más que `.col-md-3 > span`.
- **CSS vs XPath:** CSS para la mayoría de casos (más legible). XPath cuando necesitás navegar por texto o estructura compleja: `//h2[contains(text(), 'Precio')]/following-sibling::span`.
- **Extracción por lotes:** Si son muchas páginas, guardá incrementalmente. No pierdas 2 horas de scraping por un crash al final.
- **Requests con sesión:** Usá `requests.Session()` para mantener cookies y conexión keep-alive.

### 4. Rate limiting y politeness

NUNCA hagas requests sin delay. Es mala práctica y te van a banear.

- **`time.sleep(random.uniform(1, 3))`** entre requests como mínimo.
- **User-Agent rotativo:** Armate una lista de 5-10 User-Agents reales y rotalos.
- **Respetá `Crawl-delay`** del robots.txt si existe.
- **Scrapy:** Configurá `DOWNLOAD_DELAY`, `CONCURRENT_REQUESTS_PER_DOMAIN`, y `AUTOTHROTTLE_ENABLED`.
- **Sesiones con backoff exponencial:** Si recibís 429 (Too Many Requests) o 503, esperá `2^intento` segundos antes de reintentar.

### 5. Manejar edge cases

- **Cambios en la estructura:** Envolvé la extracción en try/except. Si un selector falla, logueá la URL y el error esperado vs real. No crashees — seguí con la siguiente página.
- **Timeouts:** Siempre seteá timeout en requests: `requests.get(url, timeout=10)`.
- **Bloqueos / CAPTCHAs:** Si detectás bloqueo (403, Cloudflare, captcha), reportalo inmediatamente. No intentés evadir captchas sin autorización explícita.
- **Infinite scroll:** Scroll progresivo con `page.evaluate('window.scrollTo(0, document.body.scrollHeight)')` y esperar a que no aparezcan nuevos elementos.
- **Contenido dinámico lazy-loading:** Esperá elementos específicos con `waitForSelector` o `WebDriverWait`.
- **Encoding:** Verificá `response.encoding` y `response.apparent_encoding`. Sitios en español suelen usar ISO-8859-1 o UTF-8.

### 6. Guardar datos

- **Formato:** CSV para datasets chicos (<100k filas) y compatibilidad. Parquet para datasets grandes (comprime 10x, preserva tipos). JSON para datos anidados.
- **Guardado incremental:** Cada N páginas, append al archivo. Si el scraping muere a la mitad, no perdés todo.
- **Estructura:** Cada registro debe tener `fecha_extraccion`, `url_origen`, y `timestamp` para trazabilidad.
- Usar `pandas` para estructurar y limpiar antes de guardar.

### 7. Validar que los datos tengan sentido

- **Cantidad esperada:** ¿Coincide la cantidad de registros con lo que mostrabas la paginación?
- **Tipos correctos:** Precios como float, fechas como datetime, IDs como string.
- **Sin duplicados:** `df.duplicated().sum()`.
- **Valores plausibles:** Sin precios negativos, fechas futuras, o strings donde debería haber números.
- **Muestra manual:** Agarrá 5 registros al azar y comparalos contra la página original.
- Reportá cualquier anomalía al orchestrator antes de dar por terminado.
