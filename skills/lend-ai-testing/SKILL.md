---
name: lend-ai-testing
description: "Guardián de calidad — tests unitarios, integración, E2E, CI/CD y cobertura para el ecosistema Lend.Ai."
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.1"
---

# Skill: lend-ai-testing

Cargá esta skill cuando necesites escribir tests, configurar CI, o revisar calidad de código.

## ¿Qué es CI?

La Integración Continua verifica automáticamente cada cambio que subís. El objetivo es asegurar que cada cambio que llegue a main sea funcional, seguro y siga los estándares del proyecto.

En GitHub, se maneja con **GitHub Actions**: eventos → config YAML → runners → jobs → steps.

## Los 3 pilares de CI en Python

| Pilar | Herramienta | ¿Qué revisa? |
|-------|-------------|--------------|
| **Linting** | ruff, flake8, black | PEP 8, código legible |
| **Tests** | pytest, unittest | Que el código funcione |
| **Seguridad** | pip-audit, bandit, Dependabot | Vulnerabilidades |

## Tipos de tests

| Tipo | Framework | Propósito |
|------|-----------|-----------|
| Unitarios | pytest / Vitest | Funciones, hooks, componentes |
| Integración | pytest+httpx / Testing Library | APIs, servicios |
| E2E | Playwright | Flujos completos |

## CI (GitHub Actions)

- Trigger: push a main + PRs a main
- Orden: linter → tests → security
- Cobertura mínima: 80%
- Cache de dependencias
- Matrix de versiones

## Reglas

- Cada PR incluye tests del cambio
- No se mergea con CI rojo ni coverage decreciente
- Tests lentos → mark como slow
- Mocks necesarios pero sin abusar
- El CI es tu red de seguridad: experimentá con confianza
