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
