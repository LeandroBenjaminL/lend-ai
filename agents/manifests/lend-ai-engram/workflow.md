# Lend.Ai Engram — Workflow

## Cuándo guardar

- Después de cada decisión de arquitectura
- Cuando se encuentra y fixea un bug
- Cuando se establece un patrón o convención nueva
- Al finalizar un cambio significativo (commit, merge, PR)
- Al final de cada sesión (session-summary)
- Cuando se descubre algo que puede ser útil después

## Formato de entrada

Toda entrada debe incluir los 4 campos:

```
**What**: qué se hizo o descubrió (1 línea)
**Why**: por qué se tomó esta decisión o hubo que hacer esto
**Where**: archivos, servicios, herramientas involucradas
**Learned**: qué aprendimos, edge cases, gotchas (opcional si es obvio)
```

## Tipos de entrada

| Tipo | Cuándo usarlo | Ejemplo título |
|------|--------------|----------------|
| `architecture` | Decisiones de diseño, estructura, patrones | "Migración de Express a Fastify" |
| `bugfix` | Bugs encontrados y corregidos | "Fixed FTS5 syntax error en búsqueda" |
| `pattern` | Convenciones, buenas prácticas | "Convención de naming para handlers" |
| `config` | Configuración, herramientas, setup | "Docker MCP reparado" |
| `decision` | Decisiones con alternativas evaluadas | "Elegimos Zustand sobre Redux por simplicidad" |
| `learning` | Descubrimientos técnicos generales | "FTS5 MATCH no es LIKE — sanitizar input" |
| `session` | Resumen de sesión al finalizar | "Sesión: setup de CI + tests unitarios" |

## Estructura de session-summary

```
## Goal
[Una línea: qué intentamos lograr en esta sesión]

## Instructions
[Preferencias del usuario, constraints, cosas a recordar para futuro]

## Discoveries
- [Hallazgo técnico 1]
- [Gotcha o aprendizaje 2]

## Accomplished
- ✅ [Tarea completada — con detalles clave]
- 🔲 [Tarea identificada pero pendiente]

## Next Steps
- [Qué sigue para la próxima sesión]

## Relevant Files
- path/to/file — qué hace o qué cambió
```

## Consulta antes de actuar

Siempre que arranca una tarea:
1. Buscar en Engram por keywords relacionadas
2. Si hay contexto, leerlo antes de avanzar
3. Si se encuentra un conflicto, reportarlo al orquestador
