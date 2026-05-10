# Lend.Ai Testing — Workflow

## ¿Qué es CI (Integración Continua)?

La CI es una práctica donde cada cambio que subís se integra y verifica automáticamente. El objetivo no es solo "subir código", sino asegurar que cada cambio que llega a main sea funcional, seguro y siga los estándares del proyecto.

En GitHub, esto se maneja con **GitHub Actions**.

## ¿Cómo funciona internamente?

```
Evento (trigger)
    │
    ▼
Archivo .github/workflows/*.yaml
    │
    ▼
Runner (VM temporal: Linux, macOS o Windows)
    │
    ▼
Jobs (unidades de ejecución)
    │
    ▼
Steps (tareas secuenciales dentro de un Job)
```

1. **Evento**: Un `git push` o un PR dispara el workflow
2. **Config**: GitHub busca ` .github/workflows/*.yaml` — el manual de instrucciones
3. **Runner**: Una VM limpia y temporal ejecuta los jobs
4. **Jobs**: Unidades de ejecución (ej: "Tests" y "Linting" van separados)
5. **Steps**: Tareas secuenciales (instalar deps → correr tests → subir reporte)

## Los 3 pilares de CI en Python

Antes de permitir un merge, el CI debe validar:

| Pilar | Herramienta | ¿Qué revisa? |
|-------|-------------|--------------|
| **Linting** | ruff, flake8, black | PEP 8, código legible y estandarizado |
| **Tests** | pytest, unittest | Que el código funcione |
| **Seguridad** | pip-audit, bandit, Dependabot | Vulnerabilidades en dependencias |

## Tipos de tests

| Tipo | Framework | Cuándo |
|------|-----------|--------|
| Unitarios | pytest (Python) / Vitest (frontend) | Funciones, utils, hooks, componentes aislados |
| Integración | pytest + httpx / Testing Library | APIs, servicios, interacción entre componentes |
| E2E | Playwright | Flujos completos del usuario |
| Snapshots | pytest-snapshot / Vitest | UI estable, outputs predecibles |

## Estructura de archivos

```
tests/
├── unit/
│   ├── test_<modulo>.py  (Python)
│   └── <Component>.test.tsx  (frontend)
├── integration/
│   └── test_api_<endpoint>.py
└── e2e/
    └── <feature>.spec.ts
.github/workflows/
    └── ci.yaml
```

## CI (GitHub Actions)

### Checklist de workflow

- [ ] Trigger: push a main + PRs a main
- [ ] Run: linters primero (fallo rápido), después tests, después coverage
- [ ] Cobertura mínima: 80% (warning bajo 80%, failure bajo 70%)
- [ ] Cache de dependencias entre runs
- [ ] Matrix de versiones de Python/Node si aplica
- [ ] Security scan: Dependabot o pip-audit

### Estructura base de workflow

```yaml
name: Python CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run Tests
      run: |
        pytest
```

## Reglas

- Cada PR debe incluir tests para el cambio que introduce
- No se mergea con tests fallando (obvio) ni con coverage decreciente
- Tests lentos (>1s cada uno) merecen un mark `@pytest.mark.slow`
- Los mocks son necesarios pero no abuses — si mockeás todo, no estás probando nada
- El CI es tu red de seguridad: podés experimentar con refactors grandes porque si rompés algo, CI te avisa al toque
