---
description: Revisar y optimizar la estructura de Engram (topic_keys, tipos, proyecto)
agent: lend-ai
subtask: true
---

# /engram-optimize

Revisá que las memorias de Engram estén bien organizadas: topic_key correcto, tipo adecuado, sin duplicados, sin huérfanas.

## Uso

```
/engram-optimize                 → escaneo completo
/engram-optimize --project <p>   → solo un proyecto
/engram-optimize --dry-run       → solo reportar, no modificar
/engram-optimize --fix           → aplicar fixes automáticos
```

## Qué revisa

| Check | Busca |
|-------|-------|
| 🔍 topic_key faltante | Memorias sin topic_key que deberían tenerlo |
| 🔍 tipo incorrecto | `architecture` usado para bugs, `discovery` para decisiones |
| 🔍 scope incorrecto | Preferencias de usuario con scope project |
| 🔍 formato inconsistente | Sin What/Why/Where/Learned |
| 🔍 duplicados | Dos entradas sobre el mismo tema sin topic_key compartido |
| 🔍 huérfanas | Memorias de proyectos que ya no existen |
| 🔍 user_preference | Preferencias del usuario que deberían estar en personal |

## Formato de reporte

```
📊 Engram Health — proyecto: lend-ai
━━━━━━━━━━━━━━━━━━━━━━━
✅ topic_key: 15/18 correctos
⚠️  3 sin topic_key → #120, #121, #122
✅ tipos: todos correctos
⚠️  1 discovery que parece bugfix → #115
✅ scope: todo ok
📦 Perfil usuario: actualizado hace 2 días

Archivo de preferencias: preference/perfil-leandro (#298)
Nuevas preferencias detectadas: 2 → guardar como user_preference
```

## Acciones automáticas (con --fix)

- Asignar topic_key faltante según contenido
- Corregir tipo si está mal clasificado
- Mover scope incorrecto a personal
- Fusionar duplicados detectados

## REGLAS

- No modifiques nada sin `--fix`
- Mostrá diff de cambios si aplicás fixes
- Si encontrás info del usuario sin guardar → guardala como user_preference
