# Development

## Comandos frecuentes

```bash
source .venv/bin/activate    # Activar entorno
pip install -r requirements.txt -r requirements-dev.txt  # Instalar deps
ruff check .                 # Linter
ruff format .                # Formatear código
pytest                       # Tests
pytest --cov=src             # Tests con cobertura
pytest -k "model"            # Tests filtrados
python scripts/model-commands.py list  # Ver modelos
```

## ADR (Architecture Decision Records)

Las decisiones técnicas importantes se documentan en `docs/adr/`.

### ADRs activos

| # | Decisión | Estado |
|---|----------|--------|
| 001 | Usar pathlib en lugar de os.path | Aceptado |
| 002 | Sistema de tiers para modelos (T1-T5) | Aceptado |
| 003 | OpenCode como plataforma de agentes | Aceptado |
| 004 | Skills como sub-agentes ejecutables | Aceptado |

### Cómo crear un ADR

```
cp docs/adr/TEMPLATE.md docs/adr/XXX-titulo-breve.md
# Completar: Contexto → Decisión → Consecuencias → Estado
```

## Debug

```bash
# Ver MCP servers activos
ls mcp-servers/

# Testear agente-router
python3 mcp-servers/agent-router.py --health

# Ver modelo activo
python3 scripts/model-commands.py list
```
