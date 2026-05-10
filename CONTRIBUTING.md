# Contributing

## Entorno de desarrollo

1. Clonar el repo
2. Ejecutar `./install.sh` (crea .venv, instala deps, configura hooks)
3. Activar el entorno: `source .venv/bin/activate`

## Estándares de código

- **Python**: PEP 8 vía ruff. Correr `ruff check .` antes de commitear
- **TypeScript**: strict mode siempre
- **Commits**: Conventional Commits (`feat:`, `fix:`, `docs:`, etc.)

## Tests

```bash
pytest                    # todos los tests
pytest -k "model"         # filtrar por keyword
pytest --cov=src          # con cobertura
```

## Pull Requests

1. Crear branch desde `main`: `git checkout -b feat/mi-cambio`
2. Hacer cambios + tests
3. `ruff check .` y `pytest` pasando
4. Push y abrir PR a `main`

## Skills / Agentes

Si agregás una skill o sub-agente nuevo:
1. Crear manifest en `agents/manifests/<name>.yaml`
2. Agregar entry en `opencode.json`
3. Actualizar `AGENTS.md` con la entrada correspondiente

## Reportar bugs

Abrir issue con:
- Descripción del problema
- Logs o errores relevantes
- Versión del ecosistema (ver CHANGELOG.md)
