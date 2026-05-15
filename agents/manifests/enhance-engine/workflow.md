# Enhance Engine — Workflow

## Ciclo de mejora paralela

```
1. RECIBIR INPUT
   ├── ¿Qué hay que mejorar? (código, archivo, feature, doc, arquitectura)
   ├── Contexto: specs, diseño, propósito
   └── Objetivo: ¿qué significa "mejor" en este caso?

2. PREPARAR 10 MIRADAS
   ├── Cada sub-agente recibe el MISMO input
   ├── Cada uno recibe UNA perspectiva específica (performance, security, etc.)
   ├── Todos se lanzan en PARALELO (no esperes a que termine uno para lanzar el otro)
   └── Timeout: si un sub-agente tarda más de lo razonable, seguí sin él

3. RECOLECTAR RESULTADOS
   ├── ¿Cuáles volvieron con cambios? → priorizarlos
   ├── ¿Cuáles volvieron vacíos? → descartarlos
   ├── ¿Hay conflictos entre mejoras? → identificar
   └── Ordenar por impacto: breaking > performance > security > quality > testing > docs > acc > UX > mant

4. CONSOLIDAR
   ├── Output final = input base + mejoras de todas las perspectivas aplicadas
   ├── Conflictos: documentar tradeoff, elegir la mejor opción para el objetivo
   ├── CHANGELOG: registrar qué cambió y por qué
   └── Engram: guardar el patrón de mejora usado (topic_key: pattern/enhance-{area})

5. REPORTAR
   ├── Cuántas perspectivas encontraron algo que cambiar
   ├── Cuáles fueron los cambios más significativos
   ├── Si hubo conflictos, cómo se resolvieron
   └── Recomendación: ¿vale la pena aplicar todas o solo un subconjunto?
```

## Output consolidado

```markdown
# Enhance Report: {qué se mejoró}

## Resumen
- {N} perspectivas encontraron mejoras
- {M} perspectivas sin cambios
- Impacto general: {bajo | medio | alto}

## Mejoras aplicadas
| # | Ángulo | Cambio | Impacto |
|---|--------|--------|---------|
| 1 | Performance | {cambio} | {alto} |
| 2 | Quality | {cambio} | {medio} |

## Conflictos resueltos
- Entre {P1} y {P2}: se eligió {opción} porque {razón}

## Archivos modificados
- {path} — {qué cambió}

## Recomendación
- {aplicar todo | aplicar subset | no aplicar}
```

## Anti-patterns

- ❌ Lanzar los 10 secuencialmente (mata el propósito)
- ❌ Descartar perspectivas "porque no van a encontrar nada"
- ❌ Consolidar promediando (quedarse con lo peor de cada uno)
- ❌ No documentar conflictos entre perspectivas
