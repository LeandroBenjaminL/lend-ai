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
