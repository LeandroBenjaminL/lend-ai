---
name: web-scraping
description: >
  Extracción de datos de sitios web con BeautifulSoup, Selenium y Scrapy.
  Trigger: Cuando necesitás scrapear sitios web, extraer datos de HTML, o automatizar navegación.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "2.0"
  model_tier: T2-fast
---

# Skill: web-scraping

## Para qué sirve

Extraer datos de páginas web que no tienen API pública. Es el último recurso — siempre es mejor una API. Pero cuando no hay, el scraping bien hecho te salva: extraés HTML, lo convertís a estructuras de datos, y seguís con tu análisis.

## Trigger (cuándo cargar esta skill)

- Los datos que necesitás están en una página web sin API
- Tenés que sacar tablas o listados de portales públicos
- Necesitás automatizar la descarga de reportes o información periódica
- Querés monitorear cambios en contenido web (precios, noticias, etc.)

## Workflow paso a paso

1. **Preguntate: ¿hay API?** — Si el sitio ofrece API oficial, usala. Siempre. Es más rápido, más confiable, y no viola términos de servicio.
2. **Analizá la página**: ¿Es HTML estático (BeautifulSoup) o cargado con JavaScript (Selenium)?
3. **Verificá `robots.txt`**: `sitio.com/robots.txt` — si dice "Disallow: /", no lo rasques. Legalmente puede ser cuestionable.
4. **Hacé el request con headers de navegador**: muchos sitios bloquean requests sin User-Agent.
5. **Parseá y extraé**: usá selectores CSS o expresiones XPath para apuntar a los datos.
6. **Respetá el sitio**: `time.sleep(1)` entre requests, no saturen el servidor.

## Herramientas: cuál usar y por qué

| Herramienta | Cuándo usarla | Ventaja | Limitación |
|-------------|---------------|---------|------------|
| **BeautifulSoup** | HTML estático (carga del server) | Simple, liviano, rápido | No ejecuta JS |
| **Selenium** | HTML dinámico (carga con JS) | Ejecuta JavaScript como un navegador real | Pesado, lento, consume RAM |
| **Scrapy** | Scraping profesional a gran escala | Async, pipelines, middlewares | Curva de aprendizaje, overkill para una página |
| **pandas.read_html** | Tablas HTML en Wikipedia, gov, etc. | Una línea de código | Solo funciona si hay `<table>` |

## Patrones esenciales

### 1. BeautifulSoup — HTML estático

El 70% de los casos: página que el servidor ya te manda completa. Con `select()` usás selectores CSS como los de la consola del navegador.

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

resp = requests.get('https://ejemplo.com/tabla', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})
soup = BeautifulSoup(resp.text, 'html.parser')

# Opción 1: extraer tabla HTML directo a DataFrame
tabla = soup.find('table')
df = pd.read_html(str(tabla))[0]

# Opción 2: extraer elementos específicos con selectores CSS
items = soup.select('.item-class')
for item in items:
    titulo = item.find('h2').text.strip()
    precio = item.select_one('.precio').text.strip()
    print(f"{titulo}: {precio}")
```

### 2. Selenium — JavaScript dinámico

Cuando la página carga datos con JS después del HTML inicial (SPAs, dashboards, carga infinita). Selenium abre un navegador de verdad y espera a que el JS termine.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://ejemplo-dinamico.com')

# Esperar a que aparezca el elemento (hasta 10 segundos)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'data-table'))
)

# Una vez cargado, extraer con pandas
df = pd.read_html(driver.page_source)[0]
driver.quit()
```

**¿Por qué usar `WebDriverWait`?** Porque si intentás leer `driver.page_source` antes de que JS termine de cargar, vas a obtener HTML vacío. `WebDriverWait` espera a que una condición se cumpla (ej: que aparezca un elemento).

### 3. pandas.read_html — el trucazo para tablas

Si lo que necesitás es una tabla HTML, muchas veces no necesitás ni BeautifulSoup. `pd.read_html()` scrapea sola:

```python
# Todas las tablas de una página
dfs = pd.read_html('https://es.wikipedia.org/wiki/Anexo:Pa%C3%ADses_por_poblaci%C3%B3n')
df_poblacion = dfs[0]
print(df_poblacion.head())
```

### 4. Scraping ético con delays

```python
import time
from random import uniform

def scrape_con_respeto(urls):
    resultados = []
    for url in urls:
        time.sleep(uniform(1, 3))  # delay aleatorio entre 1 y 3 segundos
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        resultados.append(resp.text)
    return resultados
```

## Alternativas

- **Playwright vs Selenium**: [Playwright](https://playwright.dev) es más moderno, más rápido, y tiene mejor soporte para async. Instalalo con `pip install playwright`. Si arrancás un proyecto nuevo hoy, preferí Playwright sobre Selenium.
- **Scrapy vs BeautifulSoup**: Scrapy es para scraping profesional (1000+ páginas, pipelines de datos, rotación de proxies). Para un script de una página, BeautifulSoup es suficiente.
- **API scraping**: Si el sitio tiene una API interna (mirá la pestaña Network del navegador), podés llamarla directamente sin scrapear HTML. Es más rápido y no se rompe si cambian el diseño de la página.

## Anti-patrones

- ❌ **No respetar robots.txt**: Además de ser cuestionable legalmente, te pueden banear la IP para siempre.
- ❌ **Scrapear sin User-Agent**: Muchos servidores bloquean requests sin User-Agent porque parecen bots maliciosos. Poné uno de navegador real.
- ❌ **Cero delays entre requests**: Mandar 100 requests por segundo a un sitio chico. Lo vas a tirar abajo y te van a banear.
- ❌ **Datos personales sin consentimiento**: Scrapear datos personales puede violar leyes de privacidad (GDPR, etc.). No lo hagas.
- ❌ **Usar Selenium cuando alcanza BeautifulSoup**: Selenium es 10x más pesado. Si la página es estática, no le metas un navegador entero.

## Comandos

```bash
pip install beautifulsoup4 selenium lxml pandas

# Ver si una tabla HTML es scrapeable
python -c "
import pandas as pd
dfs = pd.read_html('https://es.wikipedia.org/wiki/Anexo:Pa%C3%ADses_por_poblaci%C3%B3n')
print(f'Tablas encontradas: {len(dfs)}')
print(dfs[0].columns.tolist())
"
```
