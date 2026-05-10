# Arquitectura

## Estructura de carpetas

```
lend-ai/
├── agents/manifests/    → Manifests YAML de cada agente
│   ├── lend-ai/         → Orquestador principal
│   ├── data-analyst/    → Agente de datos
│   ├── frontend-senior/ → Agente frontend
│   └── ... (90+ agentes)
├── commands/            → Documentación de comandos slash
├── data/                → Datos de análisis (gitignored)
├── docs/                → Guías y documentación detallada
├── mcp-servers/         → Servidores MCP custom
├── openspec/            → Especificaciones SDD
├── profiles/lend-ai/    → Perfiles de identidad y workflow
├── registry/            → Registro central de agentes
├── schemas/             → Schemas de validación
├── scripts/             → Scripts de utilidad (model picker, etc)
├── skills/              → Skills (instrucciones para cada dominio)
│   ├── data-*/          → Data analysis skills
│   ├── frontend-*/      → Frontend skills
│   ├── sdd-*/           → Spec-Driven Development skills
│   └── lend-ai-*/       → Skills transversales del ecosistema
└── tests/               → Tests
```

## Agentes

```
lend-ai (orquestador)
├── data-analyst
│   ├── data-explorer
│   ├── data-modeler
│   ├── data-reporter
│   ├── data-etl
│   └── ...
├── frontend-senior
│   ├── framework-architect
│   ├── ui-crafter
│   ├── styling-engineer
│   └── ...
├── commits-real
├── lend-ai-engram
├── lend-ai-testing
└── lend-ai-docs
```

## Modelos y Tiers

| Tier | Modelo | Uso |
|------|--------|-----|
| T1 | Minimax Free | Tareas mecánicas (limpieza, formateo) |
| T2 | Minimax | Reportes simples, validaciones |
| T3 | DeepSeek Medium | EDA, análisis general (default) |
| T4 | DeepSeek Pro | Arquitectura, ML complejo |
| T5 | DeepSeek Pro Max | Problemas muy difíciles |

Ver `model-routing.config.json` y `scripts/model-commands.py`.

## Decisiones técnicas clave

| Decisión | Elegido | Alternativas |
|----------|---------|--------------|
| Model routing | Sistema propio por tiers | OpenRouter, LiteLLM |
| Platforma | OpenCode | Cline, Aider |
| Skill system | SKILL.md + manifests YAML | Solo prompts |

## MCP Servers

- `engram` — Memoria persistente entre sesiones
- `agent-router` — Resolución y enrutamiento de agentes
- `model-router` — Asignación de modelos por tier
- `filesystem` — Acceso a archivos del proyecto
- `github`, `slack`, `notion`, `google-drive` — Integraciones externas
- `postgres`, `sqlite` — Bases de datos
- `ocr`, `puppeteer`, `web-search` — Utilidades
