# Patterns: Web Scraping Cheat Sheet

## 1. requests + BeautifulSoup (HTML estático)

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
})

resp = session.get('https://ejemplo.com/productos', timeout=10)
soup = BeautifulSoup(resp.text, 'html.parser')

# Selectores CSS
items = soup.select('.producto-card')
for item in items:
    titulo = item.select_one('h2.titulo').text.strip()
    precio = item.select_one('.precio').text.strip()
    link = item.select_one('a')['href']

# Tablas directamente a DataFrame
df = pd.read_html(str(soup.find('table')))[0]
```

## 2. Puppeteer (SPA / JS dinámico)

```javascript
// Usando el MCP puppeteer — navegación y espera
await puppeteer_navigate({ url: 'https://ejemplo-spa.com' });

// Esperar a que un selector esté presente
await puppeteer_evaluate({
  script: `document.querySelector('.data-loaded') !== null`
});

// Extraer datos desde el DOM
const datos = await puppeteer_evaluate({
  script: `
    JSON.stringify(
      [...document.querySelectorAll('.producto')].map(el => ({
        titulo: el.querySelector('h2').innerText,
        precio: el.querySelector('.precio').innerText
      }))
    )
  `
});
```

### Puppeteer: Infinite scroll

```javascript
let previousHeight = 0;
while (true) {
  const newHeight = await puppeteer_evaluate({
    script: `
      window.scrollTo(0, document.body.scrollHeight);
      document.body.scrollHeight
    `
  });
  if (newHeight === previousHeight) break;
  previousHeight = newHeight;
  await new Promise(r => setTimeout(r, 2000)); // esperar carga
}
```

### Puppeteer: Screenshot para debug

```javascript
await puppeteer_screenshot({ name: 'debug-pagina', fullPage: true });
```

## 3. Selenium (alternativa Python a Puppeteer)

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--user-agent=Mozilla/5.0 ...')

driver = webdriver.Chrome(options=options)
driver.get('https://ejemplo-dinamico.com')

# Esperar elemento
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.resultados'))
)

# Extraer
elementos = driver.find_elements(By.CSS_SELECTOR, '.item')
datos = [el.text for el in elementos]

df = pd.read_html(driver.page_source)[0]
driver.quit()
```

## 4. Selectores: CSS vs XPath

| Caso | CSS Selector | XPath |
|---|---|---|
| Por clase | `.precio` | `//*[@class='precio']` |
| Por ID | `#main-content` | `//*[@id='main-content']` |
| Por atributo | `[data-id="123"]` | `//*[@data-id='123']` |
| Por texto contenido | — | `//h2[contains(text(), 'Oferta')]` |
| Hijo directo | `.card > .titulo` | `//div[@class='card']/h2` |
| n-ésimo hijo | `.item:nth-child(3)` | `(//div[@class='item'])[3]` |
| Siguiente hermano | — | `//h2/following-sibling::span` |

Regla: **CSS para lo simple, XPath para lo complejo.**

## 5. Paginación

### Patrón A: URL con `?page=N`

```python
base_url = 'https://ejemplo.com/productos?page={}'
pagina = 1
todos = []
while True:
    url = base_url.format(pagina)
    resp = session.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, 'html.parser')
    items = soup.select('.producto')
    if not items:  # página vacía = fin
        break
    todos.extend(items)
    pagina += 1
    time.sleep(random.uniform(1, 3))
```

### Patrón B: Next button

```python
url = 'https://ejemplo.com/productos'
while url:
    resp = session.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, 'html.parser')
    # ... extraer datos ...
    next_btn = soup.select_one('a.next, [rel="next"]')
    url = next_btn['href'] if next_btn else None
    time.sleep(random.uniform(1, 3))
```

### Patrón C: Puppeteer infinite scroll (ver sección 2)

## 6. Rate Limiting y politeness

```python
import random
import time

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4) AppleWebKit/605.1.15 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36',
]

# Delay base + jitter
def polite_delay(min_s=1.0, max_s=3.0):
    time.sleep(random.uniform(min_s, max_s))

# Rotar User-Agent
def random_ua():
    return random.choice(USER_AGENTS)

session.headers.update({'User-Agent': random_ua()})
```

## 7. Retry con backoff exponencial

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(
    total=5,
    backoff_factor=1,  # espera: 1s, 2s, 4s, 8s, 16s
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=['GET']
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
```

## 8. Guardado incremental

```python
import pandas as pd
from pathlib import Path

ruta = Path('datos_extraidos.csv')
primera_vez = not ruta.exists()

for pagina in range(1, total_paginas + 1):
    df_pagina = extraer_pagina(pagina)  # tu función
    df_pagina['fecha_extraccion'] = pd.Timestamp.now()
    df_pagina['pagina_origen'] = pagina

    df_pagina.to_csv(
        ruta,
        mode='a',
        header=primera_vez,
        index=False
    )
    primera_vez = False
```

## 9. Validación post-extracción

```python
df = pd.read_csv('datos_extraidos.csv')

# Checks básicos
assert len(df) > 0, 'DataFrame vacío'
assert df['precio'].dtype in ['float64', 'int64'], 'Precio no es numérico'
assert not df.duplicated().any(), 'Hay duplicados'
assert (df['precio'] > 0).all(), 'Precios negativos o cero'

# Muestra aleatoria para verificación manual
df.sample(5).to_dict('records')
```

## 10. Scrapy (para proyectos grandes)

```python
# scrapy shell para testeo interactivo
# scrapy shell 'https://ejemplo.com'

# Configuración en settings.py
DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 2
AUTOTHROTTLE_ENABLED = True
ROBOTSTXT_OBEY = True

# Spider típica
import scrapy

class ProductosSpider(scrapy.Spider):
    name = 'productos'
    start_urls = ['https://ejemplo.com/productos']

    def parse(self, response):
        for producto in response.css('.producto-card'):
            yield {
                'titulo': producto.css('h2::text').get(),
                'precio': producto.css('.precio::text').get(),
            }

        # Paginación
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

## 11. Detección de API oculta (antes de scrapear HTML)

```javascript
// Buscar en Network tab o ejecutar en consola
// __NEXT_DATA__ (Next.js)
const data = JSON.parse(document.getElementById('__NEXT_DATA__').textContent);

// __NUXT__ (Nuxt.js)
const data = window.__NUXT__;

// __INITIAL_STATE__ (Vue/Vuex)
const data = window.__INITIAL_STATE__;

// GraphQL endpoint
// Buscar en Network tab → Fetch/XHR → filtrar "graphql"
```

Si encontrás datos estructurados en el HTML (JSON-LD, `<script type="application/ld+json">`), extraelos con `json.loads()` — es más limpio que parsear el DOM.

## 12. Checklist rápida

- [ ] ¿Revisé `robots.txt`? → `curl https://ejemplo.com/robots.txt`
- [ ] ¿Busqué API/JSON antes de scrapear HTML?
- [ ] ¿Elegí la herramienta correcta? (BS4 vs Puppeteer vs Scrapy)
- [ ] ¿Puse rate limiting? (delay + jitter, User-Agent rotativo)
- [ ] ¿Guardado incremental para no perder progreso?
- [ ] ¿Validé tipos, duplicados, y valores plausibles?
- [ ] ¿Agregué `fecha_extraccion` y `url_origen` en cada registro?
