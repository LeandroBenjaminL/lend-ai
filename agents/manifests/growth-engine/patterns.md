# Growth Engine — Patterns

## Patrón de Aprendizaje

Cada aprendizaje sigue esta estructura en Engram:

```
title: "Aprendizaje: {descripción corta}"
type: "learning"
topic_key: "learning/{área}"
content:
  **What**: qué pasó
  **Why**: por qué es relevante
  **Where**: archivos/áreas afectadas
  **Learned**: la lección concreta
```

## Patrón de Detección de Gaps

Cuando algo falla 3+ veces sin una skill que lo cubra → hay un gap.

```
SEÑAL: 3+ bugs de validación de datos
GAP: falta una skill de data-validation en ese pipeline
ACCIÓN: proponer skill o agregar validación a skill existente
```

## Patrón de Inconsistencia YAML-Persona

El error más común y silencioso del ecosistema:

```
CHECK: persona.md lista skills → YAML skills: las declara?
       persona.md lista sub-agents → YAML sub_agents: los declara?
       AGENTS.md tabla → YAML: coincide?
```

## Patrón de Consolidación

Entradas de Engram que deberían ser UNA:

```
SEÑAL: 3+ entradas con contenido similar pero distinto título
ACCIÓN: mem_search → mem_get_observation → mem_update para consolidar
        Usar topic_key para que futuras escrituras hagan upsert automático
```

## Anti-patrones

- ❌ Guardar aprendizajes sin topic_key (no evolucionan)
- ❌ Crear skills sin consultar al usuario
- ❌ Ignorar patrones recurrentes ("ya se arreglará solo")
- ❌ No revisar Engram antes de guardar (duplicados)
- ❌ Usar tipo incorrecto (un learning no es una decision)
