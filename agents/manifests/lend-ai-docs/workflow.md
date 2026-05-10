# Lend.Ai Docs — Workflow

## 1. Estructura multi-archivo

En lugar de un README.md gigantesco, separar por preocupaciones:

| Archivo | Propósito | ¿Quién lo lee? |
|---------|-----------|----------------|
| `README.md` | Puerta de entrada: qué hace, cómo instalar (en 2 min), cómo ejecutar | Nuevos devs, visitantes |
| `CONTRIBUTING.md` | Reglas del juego: entorno de desarrollo, estándares, PRs, tests | Contribuidores |
| `ARCHITECTURE.md` | Big picture: diagramas, estructura de carpetas, por qué tal librería | Seniors, arquitectos |
| `CHANGELOG.md` | Historial de versiones (Keep a Changelog) | Todos |
| `DEVELOPMENT.md` | Comandos frecuentes, ADR, decisiones técnicas | El equipo |
| `docs/` | Guías detalladas, tutoriales, documentación generada (Sphinx/MkDocs) | Usuarios avanzados |

## 2. Docstrings: Google Style

Toda función o clase pública debe tener:

```python
def procesar_datos(input_path: str, threshold: float = 0.5) -> pd.DataFrame:
    """
    Limpia y filtra los datos de entrada basados en un umbral de confianza.

    Args:
        input_path: Ruta al archivo CSV con los datos crudos.
        threshold: Valor mínimo de confianza para incluir un registro.

    Returns:
        Un DataFrame de pandas con los datos filtrados y normalizados.

    Raises:
        FileNotFoundError: Si la ruta de entrada no existe.
        ValueError: Si el umbral no está entre 0 y 1.
    """
```

### Checklist de docstring

- [ ] Type hints en la firma de la función
- [ ] Descripción corta (qué hace, no cómo)
- [ ] Args documentados (uno por línea, con tipo implícito)
- [ ] Returns documentado
- [ ] Raises si aplica
- [ ] Notes si la lógica es compleja (explica el por qué)

## 3. ADR (Architecture Decision Records)

Cuando tomás una decisión técnica importante, crear un ADR en `docs/adr/`:

```
docs/adr/
├── 001-usar-pathlib-en-lugar-de-os-path.md
├── 002-elegir-fastify-sobre-express.md
└── README.md
```

Formato de cada ADR:

```markdown
# ADR-001: Usar pathlib en lugar de os.path

**Fecha**: 2026-05-10
**Contexto**: Necesitamos manejar rutas de archivos en todo el proyecto.
**Decisión**: Usar pathlib.Path por ser más legible y orientado a objetos.
**Consecuencias**: + legibilidad, - compatibilidad con código legacy que usa os.path.
**Estado**: Aceptado
```

## 4. Cuándo generar cada archivo

- **README.md**: siempre, es la puerta de entrada
- **CONTRIBUTING.md**: cuando el proyecto tenga >1 contribuidor o seas vos en 6 meses
- **ARCHITECTURE.md**: cuando el proyecto tenga >5 archivos o >3 carpetas
- **CHANGELOG.md**: desde el primer commit, siguiendo Keep a Changelog
- **DEVELOPMENT.md**: cuando haya comandos frecuentes que olvidás
- **ADR**: cada vez que elegís una librería, framework o patrón sobre otro
- **Docstrings**: en toda función/clase pública desde el día 1
