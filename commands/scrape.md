---
description: Scrapeo rápido de un sitio web — extraer datos estructurados
agent: data-analyst
subtask: true
---

Extraé datos de un sitio web de forma estructurada.

FLUJO:
1. Preguntá URL y qué datos extraer
2. Elegí método: pandas read_html, BeautifulSoup o Puppeteer
3. Ejecutá el scrapeo
4. Devolvé los datos como tabla
5. Explicá cómo funciona cada método y cuándo usarlo

SKILLS A CARGAR: web-scraping

REGLAS:
- Verificá que el sitio lo permita (robots.txt)
- No hagas requests agresivos (1s entre cada uno)
- Si el sitio tiene JS, usá Puppeteer MCP

## Uso

`@data-analyst /scrape https://example.com/prices`

`@data-analyst /scrape https://lista.mercadolibre.com.ar/electronica --selector ".ui-search-result"`

## Ejemplo

Input: `@data-analyst /scrape https://example.com/prices`

Output:
```
🌐 Scrapeando: https://example.com/prices
  Método: pandas read_html (tablas HTML)
  Datos extraídos: 47 filas × 5 columnas

  | Producto     | Precio | Stock | Categoría   |
  |--------------|--------|-------|-------------|
  | Laptop XYZ   | $1,200 | 15    | Electrónica |
  | Mouse ABC    | $35    | 200   | Accesorios  |
  | ...

  ⚠️ robots.txt permite scrapeo
  ⏱ 1.2s por request (1 request total)
```
