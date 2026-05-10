---
name: lend-ai-docs
description: "Estándar de documentación senior — multi-archivo, Google-style docstrings, ADR y estructura profesional para el ecosistema Lend.Ai."
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# Skill: lend-ai-docs

Cargá esta skill cuando necesites escribir documentación, generar docstrings, o estructurar la documentación de un proyecto.

## Estructura multi-archivo

| Archivo | Propósito |
|---------|-----------|
| `README.md` | Puerta de entrada: qué hace, cómo instalar, cómo ejecutar |
| `CONTRIBUTING.md` | Reglas del juego: entorno, estándares, PRs, tests |
| `ARCHITECTURE.md` | Big picture: estructura, decisiones técnicas |
| `CHANGELOG.md` | Historial de versiones (Keep a Changelog) |
| `DEVELOPMENT.md` | Comandos frecuentes, ADR |
| `docs/` | Guías detalladas, tutoriales |

## Docstrings: Google Style

Toda función pública necesita:
- Type hints + descripción corta + Args + Returns + Raises + Notes (si aplica)

## ADR

Decisiones técnicas importantes van en `docs/adr/NNN-titulo.md`.
Formato: Contexto → Decisión → Consecuencias → Estado.

## Reglas

- Cada archivo tiene UN propósito
- Progressive disclosure: de lo general a lo específico
- El docstring explica el por qué, no el qué
- ADR ante cualquier decisión técnica con alternativas
- CHANGELOG desde el primer commit
