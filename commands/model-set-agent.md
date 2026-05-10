# /model set agent
_Asigna un tier específico a un sub-agente_

## Uso
```
/model set agent <nombre-agente> <tier>
```

## Descripción
Cambia el modelo LLM que usa un sub-agente completo. A diferencia de `/model set skill` que modifica una skill individual, este comando afecta a todas las tareas que ejecuta ese agente.

Útil cuando querés que un agente entero opere con más (o menos) capacidad sin tener que tocar skill por skill.

Si el agente no existe, el comando muestra un error con los agentes válidos.

## Ejemplos
```
/model set agent data-cleaning T1
/model set agent data-modeler T4
/model set agent sdd-apply T5
/model set agent data-reporter T3
```

## Ejecución
Al ejecutar este comando, el agente debe ejecutar:
```
python3 scripts/model-commands.py set-agent <nombre> <tier>
```

## Agentes disponibles
| Agente | Descripción |
|--------|-------------|
| `data-explorer` | Explora y perfila datasets nuevos |
| `data-cleaning` | Limpia y prepara datos |
| `data-modeler` | Entrena modelos de ML |
| `data-reporter` | Genera reportes y visualizaciones |
| `data-etl` | Construye pipelines ETL |
| `data-validation` | Valida calidad y esquemas |
| `data-question` | Define preguntas de negocio |
| `data-design` | Diseña estrategias de análisis |
| `data-verify` | Verifica resultados de análisis |
| `data-archive` | Archiva y documenta proyectos |
| `sdd-init` | Inicializa SDD en un proyecto |
| `sdd-propose` | Crea propuestas de cambio |
| `sdd-spec` | Escribe especificaciones |
| `sdd-design` | Diseña técnicamente cambios |
| `sdd-tasks` | Divide cambios en tareas |
| `sdd-apply` | Implementa cambios |
| `sdd-verify` | Verifica implementaciones |
| `sdd-archive` | Archiva cambios completados |
| `sdd-explore` | Explora ideas antes de cambios |
| `sdd-onboard` | Onboarding del flujo SDD |

## Tiers disponibles
| Tier | Modelo | Para qué |
|------|--------|----------|
| T1 | Minimax Free | Agentes mecánicos (cleaning, etl simple) |
| T2 | Minimax | Agentes de tareas simples |
| T3 | DeepSeek Medium | Default diario — agentes de propósito general |
| T4 | DeepSeek Pro | Agentes de razonamiento (modeler, design) |
| T5 | DeepSeek Pro Max | Agentes críticos (apply, verify, archive) |

## Ver también
- `/model list` — ver configuración actual de todos los agentes
- `/model reset agent <nombre>` — volver un agente al tier default
- `/model set skill <nombre> <tier>` — cambiar tier de una skill individual
