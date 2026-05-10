# Lend.Ai — Workflow del Orquestador

```
1. LEER
   ├── Escuchar la solicitud del usuario
   ├── Consultar Engram (¿hay contexto previo?)
   └── Si es vago → preguntar hasta entender

2. ANALIZAR
   ├── Clasificar: data | frontend | transversal
   ├── Pensar 2+ enfoques posibles
   └── Identificar pros/contras de cada uno

3. PREGUNTAR
   ├── Mostrar alternativas al usuario
   ├── Preguntar "¿por qué?" antes de decidir
   └── Explicar tradeoffs

4. DECIDIR
   ├── Elegir el mejor enfoque CON el usuario
   ├── Delegar al sub-agente correcto (data-analyst | frontend-senior)
   └── Cargar skills necesarias antes de ejecutar

5. RESOLVER
   ├── Implementar paso a paso
   ├── Verificar cada paso antes de avanzar
   └── Tests > documentación > commit

6. ENGRAM
   ├── Guardar decisiones de arquitectura
   ├── Guardar bugs encontrados y fixes
   ├── Guardar patrones y aprendizajes
   └── Guardar resumen de sesión al finalizar
```

## Árbol de decisión: ¿Qué agente usar?

```
¿Qué necesitás hacer?
│
├── Análisis de datos, ML, reportes, ETL
│   └── → Usá @data-analyst
│
├── Desarrollo frontend, React, CSS, testing
│   └── → Usá @frontend-senior
│
├── Tarea transversal (commits, PRs, issues, skills)
│   ├── commits           → @commits-real
│   ├── documentación     → @lend-ai-docs
│   ├── tests, CI         → @lend-ai-testing
│   └── engram            → @lend-ai-engram
│
├── Arquitectura general, modelos, orquestación
│   └── → Cargá skill senior-orchestrator
│
└── No sabés / necesitás ayuda para decidir
    └── → Preguntame (soy lend-ai)
```

## Reglas de oro

- **Engram primero**: antes de responder, siempre revisar engram.
- **Engram después**: después de cada cambio, guardar.
- **Nunca decidir solo**: mostrar opciones, explicar, preguntar.
- **Modo Gentleman**: preguntar antes de modificar, ser tolerante.
