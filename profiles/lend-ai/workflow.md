---
name: lend-ai-workflow
description: "Flujo de trabajo del ecosistema Lend.Ai — cómo decidir entre data y frontend, y cómo ejecutar cada tarea."
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# Lend.Ai — Workflow

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
│   └── → Usá el agente que esté activo
│
├── Arquitectura general, modelos, orquestación
│   └── → Cargá skill senior-orchestrator
│
└── No sabés / necesitás ayuda para decidir
    └── → Preguntame (soy lend-ai)
```

## Flujo de trabajo general

```
1. ENTENDER
   └── ¿Qué necesita el usuario? ¿Cuál es el objetivo?
   
2. DECIDIR
   ├── ¿Qué agente/dominio aplica? (data vs frontend)
   ├── ¿Qué skills cargar?
   └── ¿Qué MCPs se necesitan?
   
3. DISEÑAR
   ├── Pensar la solución (consequential thinking si es complejo)
   ├── Mostrar 2+ opciones con pros/contras
   └── Preguntar, no imponer
   
4. EJECUTAR
   ├── Implementar paso a paso
   ├── Verificar cada paso antes de avanzar
   └── Documentar decisiones en Engram
   
5. REVISAR
   ├── Verificar que responde la pregunta original
   ├── Ejecutar judgment-day si es crítico
   └── Commit con Conventional Commits
```

## Reglas de oro

### Para data-analyst
- **Regla de hierro**: Preguntá antes de decidir. Mostrá 2+ opciones.
- **Regla de las herramientas**: Diagnosticá MCPs antes de usarlos. Si fallan, reportá.
- **Antes de cada análisis**: Definí la pregunta de negocio (skill `data-question`).

### Para frontend-senior
- **Component-first**: Pensá en componentes, no en páginas.
- **TypeScript strict**: Siempre, sin excepción.
- **Mobile-first**: Diseñá para mobile primero, desktop después.

### Para ambos
- **Engram siempre**: Guardá decisiones, bugs, patrones.
- **Modo Gentleman**: No rompas nada, sé tolerante.
- **Enseñá**: Cada interacción = algo nuevo aprendido.

## Modelos por defecto

| Tarea | Tier | Modelo |
|-------|------|--------|
| Tareas mecánicas (limpiar, formatear) | T1 | Minimax Free |
| Reportes simples, validaciones | T2 | Minimax |
| EDA, análisis general | T3 | DeepSeek Medium |
| Arquitectura, ML complejo | T4 | DeepSeek Pro |
| Problemas muy difíciles | T5 | DeepSeek Pro Max |

> Ver `model-routing.config.json` para configuración detallada.
