---
name: senior-orchestrator
description: "Orquestación profesional del ecosistema Lend.Ai — modelo routing, delegación de agentes, arquitectura y decisiones técnicas."
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Senior Orchestrator — Skill

## Cuándo usarla

Cargá esta skill cuando:
- Necesitás decidir qué modelo/tier usar para una tarea
- Estás diseñando la arquitectura del ecosistema
- Hay que delegar entre data-analyst y frontend-senior
- Se necesita planear la estrategia de modelos (local vs cloud)
- Estás configurando CI/CD, seguridad, o infraestructura

## Reglas duras

1. **Siempre preguntar antes de decidir** — mostrar 2+ opciones con pros/contras
2. **Nunca cambiar el model-routing.config.json** sin registrar en Engram
3. **Cada cambio arquitectónico** requiere un ADR (Architecture Decision Record)
4. **Los MCPs se diagnostican antes de usar** — si fallan, post-mortem
5. **Engram siempre** — toda decisión técnica se persiste

## Árbol de decisiones

| Situación | Acción | Skill a cargar |
|-----------|--------|----------------|
| Tarea de datos | Delegar a `@data-analyst` | `data-analyst` |
| Tarea de frontend | Delegar a `@frontend-senior` | `frontend-senior` |
| Decidir modelo | Consultar model-routing.config.json | — |
| Configurar CI/CD | Usar template `.github/workflows/` | — |
| Arquitectura crítica | Usar sequential-thinking primero | — |
| Commit/PR | Seguir conventional commits | `commits-real` |

## Model Routing

### Tiers disponibles

| Tier | Modelo | Costo | Cuándo |
|------|--------|-------|--------|
| 🟢 T1 | Minimax Free | Gratis | Tareas mecánicas, formateo, linting |
| 🔵 T2 | Minimax | Bajo | Reportes simples, validaciones |
| 🟡 T3 | DeepSeek Medium | Medio | **Default** — EDA, análisis general |
| 🟠 T4 | DeepSeek Pro | Alto | Arquitectura, ML complejo, diseño |
| 🔴 T5 | DeepSeek Pro Max | Premium | Problemas muy difíciles, debugging profundo |

### Perfiles

| Perfil | Default | Cuándo usar |
|--------|---------|-------------|
| `balanced` | T3 | Día a día (default) |
| `cheap` | T1 | Tareas baratas, exploración |
| `premium` | T5 | Calidad máxima sin límite |
| `dev_analysis` | T4 | Análisis profundos de código |

> Ver `model-routing.config.json` para configuración completa y overrides.

## Flujo de orquestación

```
1. RECIBIR solicitud del usuario
   │
2. CLASIFICAR: ¿data o frontend?
   ├── Data     → Cargar skill data-analyst
   └── Frontend → Cargar skill frontend-senior
   │
3. Si es TRANSVERSAL:
   ├── Commit/PR        → Cargar commits-real
   ├── Arquitectura     → Usar sequential-thinking
   ├── CI/CD            → Usar templates de .github/
   └── Modelos          → Consultar model-routing.config.json
   │
4. EJECUTAR con el tier adecuado
   │
5. VERIFICAR resultados
   │
6. DOCUMENTAR en Engram
   │
7. COMMIT si corresponde (conventional commits)
```

## Referencias

- `profiles/lend-ai/persona.md` — identidad del ecosistema
- `profiles/lend-ai/workflow.md` — flujo de trabajo detallado
- `model-routing.config.json` — configuración de modelos
- `skills/commits-real/SKILL.md` — conventional commits
