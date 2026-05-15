# Enhance Engine — Patterns

## Patrón de mejora paralela

```
INPUT → 10x PARALLEL → CONSOLIDATE → OUTPUT
```

Cada vez que alguien pide mejorar algo, la respuesta es "lo miramos desde 10 ángulos".

## Patrón de sub-agente efímero

Cada mirada (performance, security, etc.) ES un sub-agente que:
1. Nace con el input + su perspectiva
2. Analiza desde su ángulo
3. Produce un diff/sugerencia o "sin cambios"
4. Muere

No se guarda estado. No tiene memoria. Es una lente descartable.

## Patrón de consolidación con conflictos

```
Si P1 dice "optimizar bucle" y P2 dice "extraer a función":
  → Las dos se aplican (no son excluyentes)

Si P3 dice "validar input en API" y P9 dice "simplificar flujo":
  → Se aplican las dos (son capas distintas)

Si P8 dice "agregar ARIA labels" y P10 dice "reducir markup":
  → Se aplican las dos (accesibilidad y simplicidad no son mutuamente excluyentes)
```

Los conflictos reales son raros porque las perspectivas operan en capas distintas.

## Patrón de prioritización

```
Breaking changes > Performance > Security > Quality > Testing
> Documentation > Error Handling > Accessibility > UX > Maintainability
```

Si dos cambios tocan el mismo archivo, aplicar primero el de mayor prioridad y después adaptar el otro.
