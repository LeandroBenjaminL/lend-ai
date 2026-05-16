---
name: content-engine
description: >
  Meta-skill que analiza Engram, trackea mejoras en proyectos,
  actualiza documentación y genera contenido para LinkedIn.
  Se ejecuta después de sesiones significativas.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# Content Engine

## Propósito

Analizar Engram constantemente para entender qué se hizo, detectar patrones de mejora, mantener la documentación al día, y generar contenido profesional (LinkedIn posts, case studies, tips técnicos).

## Ciclo

```
1. LEER ENGRAM
   ├── mem_context → actividad reciente
   ├── mem_search → patrones, bugs, decisiones
   └── git log → commits del proyecto

2. ANALIZAR MEJORAS
   ├── ¿Qué se construyó? (features, skills, agents)
   ├── ¿Qué se arregló? (bugs, fixes, refactors)
   ├── ¿Qué se aprendió? (descubrimientos, patrones)
   └── ¿Qué cambió? (arquitectura, config, docs)

3. SINTETIZAR
   ├── Timeline de progreso
   ├── Logros destacados
   └── Áreas de mejora continua

4. DOCUMENTAR (si detectás cambios no documentados)
   ├── CHANGELOG → agregar entry si falta
   ├── AGENTS.md → actualizar si hay skills nuevas
   ├── README → reflejar estado actual
   └── ARCHITECTURE → si cambió estructura

5. GENERAR CONTENIDO
   ├── LinkedIn post: logro, aprendizaje o tip técnico
   ├── Case study: problema → solución → resultado
   └── Thread: secuencia de aprendizajes

6. GUARDAR TODO EN ENGRAM
   ├── Qué se documentó
   ├── Qué contenido se creó
   ├── Ideas pendientes para después
   └── Próximos pasos sugeridos
```

## Tipos de contenido que genera

| Tipo | Formato | Cuándo |
|------|---------|--------|
| **Post técnico** | 300-500 chars, hook + valor + CTA | Después de un fix o feature significativo |
| **Case study** | Problema → Solución → Resultado | Después de resolver un problema complejo |
| **Thread educativo** | 3-5 tweets, hilo con aprendizajes | Después de una investigación o exploración |
| **Tip rápido** | 1 párrafo, consejo con código o analogía | Después de un discovery o learning |
| **Progreso semanal** | Resumen de avances, métricas, próximos pasos | Semanal o después de sesión larga |

## Reglas

- NO publicar nada — solo generar borradores y guardarlos
- Preguntar antes de publicar o postear en serio
- Siempre incluir qué proyecto/repo está relacionado
- Usar tono profesional pero cercano (no corporativo)
- Incluir hashtags relevantes (#opensource #AI #dev)

## Arsenal

| Skill | Archivo | Cuándo |
|-------|---------|--------|
| `lend-ai-docs` | `skills/lend-ai-docs/SKILL.md` | Para escribir/actualizar documentación |
| `commits-real` | `skills/commits-real/SKILL.md` | Para commits convencionales |
| `lend-ai-engram` | `skills/lend-ai-engram/SKILL.md` | Para gestionar memoria Engram |
