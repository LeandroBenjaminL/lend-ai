# /model list
_Muestra la configuración actual de tiers y modelos_

## Uso
```
/model list
/model list skills
/model list agents
```

## Descripción
Sin argumentos, muestra todas las skills y agentes con su tier asignado y el modelo correspondiente. Los que están en el tier default aparecen sin marca; los que fueron personalizados con `/model set` aparecen destacados.

Los sub-comandos `skills` y `agents` filtran la vista a solo una categoría.

## Ejemplos
```
/model list
/model list skills
/model list agents
```

## Salida esperada

### Vista completa
```
📊  Configuración de modelos

=== SKILLS ===
Skill                  Tier    Modelo              Estado
data-cleaning          T1      Minimax Free        ⚡ personalizado
data-visualization     T3      DeepSeek Medium     default
ml-modeling            T4      DeepSeek Pro        ⚡ personalizado
sql-analysis           T3      DeepSeek Medium     default
time-series-analysis   T3      DeepSeek Medium     default
api-integration        T2      Minimax             default
reporting              T3      DeepSeek Medium     default
data-profiling         T1      Minimax Free        default
etl-pipelines          T2      Minimax             default

=== AGENTES ===
Agente                 Tier    Modelo              Estado
data-explorer          T3      DeepSeek Medium     default
data-cleaning          T1      Minimax Free        ⚡ personalizado
data-modeler           T4      DeepSeek Pro        ⚡ personalizado
data-reporter          T3      DeepSeek Medium     default
data-etl               T2      Minimax             default
sdd-apply              T5      DeepSeek Pro Max    ⚡ personalizado
```

### Vista filtrada: skills
```
Skill                  Tier    Modelo              Estado
data-cleaning          T1      Minimax Free        ⚡ personalizado
ml-modeling            T4      DeepSeek Pro        ⚡ personalizado
sql-analysis           T3      DeepSeek Medium     default
data-visualization     T3      DeepSeek Medium     default
reporting              T3      DeepSeek Medium     default
(...)
```

### Vista filtrada: agentes
```
Agente                 Tier    Modelo              Estado
data-cleaning          T1      Minimax Free        ⚡ personalizado
data-modeler           T4      DeepSeek Pro        ⚡ personalizado
sdd-apply              T5      DeepSeek Pro Max    ⚡ personalizado
data-reporter          T3      DeepSeek Medium     default
(...)
```

## Tiers disponibles
| Tier | Modelo | Para qué |
|------|--------|----------|
| T1 | Minimax Free | Tareas mecánicas |
| T2 | Minimax | Tareas simples |
| T3 | DeepSeek Medium | Default diario |
| T4 | DeepSeek Pro | Razonamiento |
| T5 | DeepSeek Pro Max | Máxima complejidad |

## Ver también
- `/model set skill <nombre> <tier>` — cambiar tier de una skill
- `/model set agent <nombre> <tier>` — cambiar tier de un agente
- `/model reset <skill|agent> <nombre>` — restaurar default
