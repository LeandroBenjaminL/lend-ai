# ADR-004: Skills como sub-agentes ejecutables

**Estado**: Aceptado

## Contexto

El ecosistema necesita instrucciones reutilizables para tareas específicas (análisis de datos, desarrollo frontend, commits, etc.). Estas instrucciones deben ser:
- Descubribles por agentes y humanos
- Versionables en git
- Cargables bajo demanda (no saturar el contexto)

Alternativas consideradas:
- **Prompts inline en código**: No descubribles, no versionables
- **Documentación suelta**: Difícil de cargar programáticamente
- **SKILL.md + manifests YAML**: Archivos markdown con instrucciones, indexados en AGENTS.md, cargables por el agente orquestador

## Decisión

Cada skill es un directorio con `SKILL.md` como entrada principal. El agente orquestador decide qué skill cargar según la tarea. El índice de skills está en `AGENTS.md`.

Estructura:
```
skills/
├── data-analysis/SKILL.md
├── frontend-react-development/SKILL.md
├── commits-real/SKILL.md
└── ...
```

## Consecuencias

- **Positivas**: Skills modulares, versionables, descubribles. Carga bajo demanda sin contaminar el contexto. Fácil de agregar nuevas skills sin tocar código del orquestador.
- **Negativas**: El agente debe decidir qué skill cargar — requiere un sistema de routing (trigger matching).
- **Neutras**: Las skills no son plugins ejecutables, son instrucciones para el agente. La ejecución la hace el agente basado en esas instrucciones.
