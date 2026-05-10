# Lend.Ai

> Ecosistema unificado de agentes AI: Data Analysis + Frontend Development.

Lend.Ai es un ecosistema de agentes AI orquestados para dos dominios: análisis de datos y desarrollo frontend. Corre sobre OpenCode y utiliza un sistema de skills, sub-agentes y modelos jerárquicos (T1-T5) para optimizar costo y calidad según la tarea.

## Quick Start

```bash
git clone https://github.com/LeandroBenjaminL/lend-ai.git
cd lend-ai
chmod +x install.sh && ./install.sh
```

## Stack

- **Python 3.10+** para data science
- **TypeScript 5.x** para frontend
- **OpenCode** como plataforma de agentes
- **Modelos**: DeepSeek, Minimax, Gemini, Qwen (vía tiers T1-T5)

## Comandos principales

| Comando | Qué hace |
|---------|----------|
| `make test` | Corre tests |
| `make lint` | Corre linter (ruff) |
| `/model list` | Ver agents y skills con sus modelos |
| `/model set agent <name> <tier>` | Cambiar modelo de un agente |

## Documentación

| Archivo | Para qué |
|---------|----------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Big picture del ecosistema |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Cómo contribuir |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Comandos frecuentes y ADR |
| [AGENTS.md](AGENTS.md) | Índice completo de skills y agentes |
| [CHANGELOG.md](CHANGELOG.md) | Historial de versiones |
| [docs/](docs/) | Guías detalladas |

## Licencia

MIT © 2026 Leandro Benjamin L.
