---
name: gentle-ai-chained-pr
description: >
  Divide cambios grandes en PRs encadenados para mantener el foco del revisor
  dentro de 400 líneas. Trigger: cuando un PR supera 400 líneas cambiadas,
  o al planificar PRs encadenados.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.1"
  model_tier: T2-fast
---

# Skill: chained-pr

Partir cambios grandes en PRs chicos para que el revisor no se funda.

## Trigger

- Planeaste un cambio y va a superar **400 líneas** (additions + deletions).
- Un reviewer te pidió que dividas el PR.
- SDD forecast dice `Chained PRs recommended: Yes`.
- Querés PRs que se revisen en **60 minutos o menos** cada uno.

## Por qué existe

Un PR de 800 líneas es cara de póker. El revisor arranca con ganas, llega a la
línea 300, ya no sabe qué está revisando y aprueba para salir del paso. Eso es
cómo no revisar. Partir en PRs encadenados no es burocracia: es respeto por la
atención del que revisa. Resultado: bugs se encuentran antes, merge más rápido.

## Estrategias (preguntá al usuario primero)

Antes de dividir, preguntá: "Esto pasa las 400 líneas. ¿Cómo lo dividimos?"

**1. Stacked PRs a main** — cada PR mergea a main en orden.
           Ideal para: velocidad, equipos chicos, slices independientes.

**2. Feature Branch Chain (con tracker)** — todos los PRs mergean a una branch
           compartida. Solo el tracker mergea a main.
           Ideal para: rollback controlado, tests de integración antes de main.

**3. size:exception** — un solo PR si un maintainer aprueba la excepción.
           Ideal para: código generado, migrations, vendor diffs.

## Requisitos de cada PR encadenado

Cada PR individual debe:
- Tener CI verde.
- Tener UN solo entregable claro.
- Poder revertirse sin arrastrar cambios no relacionados.
- Incluir tests/docs para su unidad.
- Poder revisarse sin leer los PRs siguientes.

Si un slice no cumple esto, partilo de otra forma. No es un dump de diffs incompletos.

## Diagrama requerido

Cada PR en la cadena debe mostrar su posición con un `📍`:

```
main
 └── #101 Foundation
      └── #102 Work-unit commits
           └── 📍 #103 Este PR
                └── #104 Docs
```

Y una tabla de estado:

| PR | Scope | Status |
|----|-------|--------|
| #101 | Foundation | ✅ Merged |
| #102 | Core logic | 🟡 Open |
| #103 | Este PR | 📍 Review |

## Chain Context en el PR body

Agregá esta sección extra al template de PR:

```markdown
## Chain Context
| Campo | Valor |
|-------|-------|
| Position | 3 de 4 |
| Base | feat/mi-feature |
| Depends on | #102 |
| Follow-up | #104 |
| Review budget | 180 / 400 |

main └── #101 └── #102 └── 📍 #103 └── #104
```

## Patrones

- **Autonomía**: cada PR debe poder revisarse solo. Si necesita leer otro PR
  para entenderse, está mal dividido.
- **Dependencias claras**: siempre decí de qué PR depende este y cuál sigue.
- **Tracker para +2 PRs**: si son más de 2, creá un draft tracker PR que
  liste todos los child PRs con su estado.
- **Stacked simple**: PR 1 de main, PR 2 de la branch de PR 1, y así.
  Cuando PR 1 mergea, rebaseá PR 2 contra main y cambiá el target.
- **Cachemos la estrategia**: una vez que el usuario eligió, no preguntes de
  nuevo en la misma sesión.

## Anti-patrones

- Mandar un PR de 800 líneas sin aviso → fundís al revisor.
- Dividir por archivo ("este PR es los models, este los services") en vez de
  por comportamiento → ningún PR es revisable solo.
- Poner child PRs apuntando a main cuando elegiste feature branch → bypassa el tracker.
- Mezclar refactors con features en el mismo slice → si hay que revertir, se
  pierde todo.
- No documentar qué cambió entre un PR y el siguiente → el revisor tiene que
  comparar diffs manualmente.
