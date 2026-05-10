# /model-switch
_Orquestador visual de modelos — TUI interactivo para cambiar modelos en caliente_

## Uso
```
/model-switch
```

## Descripción
Abre un menú interactivo en la terminal (TUI) donde podés:
- Ver todos los modelos asignados a skills y sub-agentes
- Cambiar el modelo de cualquier skill o agente al vuelo
- Resetear overrides para volver al default
- Ver qué overrides están activos

Los cambios se persisten en `model-routing.config.json` inmediatamente.

## Acciones disponibles en el TUI

| Tecla | Acción |
|-------|--------|
| `s` | Cambiar modelo de una **skill** |
| `a` | Cambiar modelo de un **agente** |
| `l` | Listar todas las skills y agentes con modelos |
| `r` | Resetear un override (volver a default) |
| `q` | Salir |

## Implementación

Ejecuta el script TUI:
```
python3 scripts/model-switcher.py
```

## Tiers disponibles

| Tier | Modelo | Uso |
|------|--------|-----|
| T1 | Minimax Free | Tareas mecánicas |
| T2 | Minimax | Tareas simples |
| T3 | DeepSeek Medium | Default diario |
| T4 | DeepSeek Pro | Razonamiento profundo |
| T5 | DeepSeek Pro Max | Máxima capacidad |

## Ver también
- `/models` — comando base de routing de modelos
- `/model list` — ver configuración actual
- `/model set skill <skill> <tier>` — cambiar modelo por CLI
- `/model set agent <agent> <tier>` — cambiar modelo de agente por CLI
- `/model reset` — resetear overrides por CLI
