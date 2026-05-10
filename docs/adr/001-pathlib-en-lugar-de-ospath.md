# ADR-001: Usar pathlib en lugar de os.path

**Estado**: Aceptado

## Contexto

El proyecto Python usaba `os.path.join`, `os.path.exists`, etc. para manipular rutas de archivos. Esto genera código verboso, propenso a errores con separadores de plataforma, y menos legible.

Alternativas consideradas:
- Seguir con `os.path`
- `pathlib.Path` (stdlib, Python 3.4+)

## Decisión

Usar `pathlib.Path` de forma consistente en todo el proyecto. Cada ruta se representa como un objeto `Path` y las operaciones se hacen con métodos del objeto en lugar de funciones sueltas.

```python
# Mal
path = os.path.join("data", "raw", "dataset.csv")
if os.path.exists(path):
    with open(path) as f:
        ...

# Bien
path = Path("data") / "raw" / "dataset.csv"
if path.exists():
    content = path.read_text()
```

## Consecuencias

- **Positivas**: Código más limpio, legible y mantenible. Métodos encadenables. Soporte nativo de operadores (`/` para join).
- **Negativas**: Migración de código legacy requiere cambios puntuales.
- **Neutras**: pathlib es parte de la stdlib desde Python 3.4 — no agrega dependencias.
