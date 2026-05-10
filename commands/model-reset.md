# /model reset
_Restaura el tier default de una skill o agente_

## Uso
```
/model reset skill <nombre-skill>
/model reset agent <nombre-agente>
```

## Descripción
Vuelve al tier default (T3 — DeepSeek Medium) la skill o el agente especificado. Es útil cuando personalizaste un modelo para una tarea puntual y querés que vuelva a operar con la configuración normal.

Si el nombre no existe o no está personalizado, el comando muestra un aviso sin errores.

## Ejemplos
```
/model reset skill data-cleaning
/model reset agent data-modeler
/model reset skill ml-modeling
/model reset agent data-etl
```

## Ejecución
Al ejecutar este comando, el agente debe ejecutar:
```
python3 scripts/model-commands.py reset-skill <skill>
python3 scripts/model-commands.py reset-agent <agent>
```

## Skills que se pueden resetear
Cualquier skill listada en `/model set skill`:
`data-analysis`, `data-visualization`, `data-cleaning`, `ml-modeling`, `sql-analysis`, `api-integration`, `time-series-analysis`, `web-scraping`, `statistical-testing`, `streamlit`, `notebook-integration`, `data-validation`, `git-data`, `file-formats`, `python-environment`, `database-connections`, `regex-data`, `data-profiling`, `reporting`, `etl-pipelines`, `data-verify`, `data-archive`, `data-design`, `data-question`

## Agentes que se pueden resetear
Cualquier agente listado en `/model set agent`:
`data-explorer`, `data-cleaning`, `data-modeler`, `data-reporter`, `data-etl`, `data-validation`, `data-question`, `data-design`, `data-verify`, `data-archive`, `sdd-init`, `sdd-propose`, `sdd-spec`, `sdd-design`, `sdd-tasks`, `sdd-apply`, `sdd-verify`, `sdd-archive`, `sdd-explore`, `sdd-onboard`

## Tiers disponibles
| Tier | Modelo | Para qué |
|------|--------|----------|
| T1 | Minimax Free | Tareas mecánicas |
| T2 | Minimax | Tareas simples |
| T3 | DeepSeek Medium | Default diario |
| T4 | DeepSeek Pro | Razonamiento |
| T5 | DeepSeek Pro Max | Máxima complejidad |

> **Nota:** El default siempre es T3 (DeepSeek Medium). Si querés cambiar el default global, hablá con el orquestador del sistema.

## Ver también
- `/model list` — ver qué skills/agentes están personalizados
- `/model set skill <nombre> <tier>` — cambiar tier de una skill
- `/model set agent <nombre> <tier>` — cambiar tier de un agente
