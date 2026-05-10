# ADR-003: OpenCode como plataforma de agentes

**Estado**: Aceptado

## Contexto

Necesitamos una plataforma de agentes que soporte:
- MCP (Model Context Protocol) para herramientas extensibles
- Sistema de skills reutilizables
- Orquestación de múltiples agentes
- Integración con editores y CLI

Alternativas consideradas:
- **Cline**: Buena integración con IDE pero menos flexible en orquestación multi-agente
- **Aider**: Excelente para pair programming pero no diseñado para ecosistema de agentes
- **OpenCode**: Soporte nativo de MCP, skills como archivos, multi-agente, CLI-first

## Decisión

Usar OpenCode como plataforma base. La configuración vive en `opencode.json` (agentes, MCP servers, skills). Cada agente se define como manifest YAML en `agents/manifests/`.

## Consecuencias

- **Positivas**: Ecosistema MCP rico (engram, agent-router, model-router). Skills como archivos versionables. Comunidad activa. CLI nativo.
- **Negativas**: Relativamente nuevo — menos herramientas de terceros que alternativas más maduras.
- **Neutras**: Al ser config-driven, migrar a otra plataforma en el futuro requeriría solo cambiar el entrypoint.
