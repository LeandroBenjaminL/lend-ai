# Lend.Ai Engram — Patterns

## Ejemplo entrada de decisión

```
title: "Migración de Express a Fastify"
type: "decision"
content: |
  **What**: Reemplazamos Express por Fastify en el API server
  **Why**: Express no soporta async/await nativo y el throughput era limitado
  **Where**: src/server.ts, package.json, src/middleware/
  **Learned**: Fastify requiere adaptadores para middleware Express, pero rinde 2x
```

## Ejemplo entrada de bugfix

```
title: "Fixed N+1 query en listado de usuarios"
type: "bugfix"
content: |
  **What**: Agregamos eager loading con JOIN para evitar N+1
  **Why**: Cada usuario disparaba una query separada para traer sus posts
  **Where**: src/repositories/user-repo.ts
  **Learned**: Siempre revisar las queries generadas por ORM antes de hacer deploy
```

## Ejemplo session-summary

```
mem_session_summary(
  id="session-20260510-001",
  content="..."
)
```

## Cuándo NO guardar

- Cambios triviales sin aprendizaje (ej: rename de variable)
- Tareas incompletas sin decisión tomada
- Información sensible (tokens, passwords, secrets)
