# Lend.Ai Docs — Patterns

## Patrón de README.md

```markdown
# Nombre del Proyecto

> Una línea que dice qué hace y para quién.

## Quick Start

\`\`\`bash
git clone <repo>
cd <repo>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
\`\`\`

## Comandos principales

- \`make test\` — corre tests
- \`make lint\` — corre linter

## Stack

- Python 3.11 + Pandas
- Ver [ARCHITECTURE.md](ARCHITECTURE.md)
```

## Patrón de ARCHITECTURE.md

```markdown
# Arquitectura

## Estructura de carpetas

\`\`\`
src/           → Código fuente
  core/        → Lógica de negocio
  api/         → Endpoints
notebooks/     → EDA y experimentos
data/          → Datos (gitignored)
tests/         → Tests
docs/          → Documentación
\`\`\`

## Decisiones técnicas

| Decisión | Opción elegida | Alternativas |
|----------|---------------|--------------|
| Manejo de rutas | pathlib | os.path |
| Testing | pytest | unittest |
```

## Patrón de CHANGELOG.md (Keep a Changelog)

```markdown
# Changelog

## [0.2.0] - 2026-05-10

### Added
- Sistema de autenticación JWT
- Endpoint de registro de usuarios

### Fixed
- Error al procesar fechas vacías en CSV

## [0.1.0] - 2026-05-01

### Added
- Proyecto inicial con estructura base
```

## Patrón de docstring con Notes

```python
def entrenar_modelo(datos: pd.DataFrame, epochs: int = 100) -> Model:
    """
    Entrena un modelo de clasificación con los datos proporcionados.

    Args:
        datos: DataFrame con features y target.
        epochs: Número de épocas de entrenamiento.

    Returns:
        Modelo entrenado listo para inferencia.

    Notes:
        Elegimos LightGBM sobre XGBoost porque maneja mejor
        valores nulos y es más rápido en datasets medianos.
        Si el dataset supera las 100k filas, considerar usar
        la GPU configurando device='gpu'.
    """
    ...
```

## Patrón de ADR

```markdown
# ADR-003: Elegir pytest sobre unittest

**Fecha**: 2026-05-10
**Contexto**: Necesitamos un framework de testing para el proyecto.
**Decisión**: Usar pytest con fixtures y plugins.
**Consecuencias**:
- Positivas: tests más concisos, fixtures reutilizables, plugins poderosos
- Negativas: depende de terceros, curva de aprendizaje para unittest users
**Estado**: Aceptado
```

## Anti-patrones

- README.md de 500 líneas que nadie lee
- Docstrings que repiten el nombre de la función
- ARCHITECTURE.md vacío o desactualizado
- CHANGELOG.md con "various fixes and improvements"
- ADRs que nunca se escriben porque "nos acordamos"
- Documentación que explica el qué (el código ya lo hace) en vez del por qué
