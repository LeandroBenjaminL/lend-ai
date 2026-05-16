---
description: Traer datos de una API REST — JSON a DataFrame automático
agent: data-analyst
subtask: true
---

Obtené datos de una API REST y convertilos a tabla.

FLUJO:
1. Preguntá URL de la API
2. Mostrá el request que vas a hacer (método, headers, params)
3. Ejecutá el request con fetch MCP o requests
4. Aplaná el JSON a DataFrame
5. Mostrá los datos
6. Explicá cómo funciona la API y sus endpoints

SKILLS A CARGAR: api-integration

REGLAS:
- Si la API requiere API key, preguntá al usuario
- Si el JSON está muy anidado, aplaná con json_normalize
- Mostrá el código del request para que el usuario aprenda

## Uso

`@data-analyst /api-fetch https://api.example.com/data`

`@data-analyst /api-fetch https://api.github.com/repos/user/repo --method GET --params '{"per_page": 5}'`

## Ejemplo

Input: `@data-analyst /api-fetch https://jsonplaceholder.typicode.com/posts?_limit=3`

Output:
```json
[
  {"userId": 1, "id": 1, "title": "sunt aut facere...", "body": "quia et suscipit..."},
  {"userId": 1, "id": 2, "title": "qui est esse", "body": "est rerum tempore..."},
  {"userId": 1, "id": 3, "title": "ea molestias quasi", "body": "et iusto sed quo..."}
]
→ DataFrame de 3 filas × 4 columnas (userId, id, title, body)
```
