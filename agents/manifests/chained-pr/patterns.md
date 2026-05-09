# Patterns: Chained PRs

> _No existe un cambio "demasiado grande para dividir". Existe una pereza de pensar cómo dividirlo bien._

## Tabla de decisión: elegir estrategia de chain

| Factor | Stacked PRs to main | Feature Branch Chain | size:exception |
|--------|---------------------|---------------------|----------------|
| **Velocidad** | Alta — cada PR mergea al aprobarse | Baja — espera a que toda la cadena esté lista | Alta — un solo PR |
| **Rollback** | Revertir PRs individuales de main | Revertir toda la feature branch | Revertir un solo PR de main |
| **Riesgo** | Features parciales pueden llegar a main | Nada llega hasta que todo está listo | Riesgo de PR gigante sin review completo |
| **Fix flow** | Fix on the go en main | Fix en la integration branch | Fix en el mismo PR |
| **Complejidad** | Simple (rebase + retarget) | Media (tracker PR, branch management) | Mínima |
| **Review por PR** | ~300-400 líneas | ~300-400 líneas | 2000+ líneas (riesgo de burnout) |
| **Mejor para** | Equipos rápidos, startups, features medianas | Releases coordinados, features grandes, equipos分散 | Código generado, migraciones, vendor diffs |

## Tabla de autonomía de cada slice

| Requisito | Stacked PR | Feature Branch PR |
|-----------|-----------|-------------------|
| CI verde en su branch | ✅ Debe pasar | ✅ Debe pasar |
| Scope único | ✅ Un deliverable | ✅ Un deliverable |
| Rollback sin daño colateral | ✅ Revertir solo este PR | ✅ Revertir sin afectar otros slices |
| Verificación incluida | ✅ Tests + docs en el mismo PR | ✅ Tests + docs en el mismo PR |
| Reviewable sin contexto externo | ✅ Con Chain Context section | ✅ Con Chain Context section |
| Base correcta | ✅ Apunta a main o al PR anterior | ✅ Apunta a la feature branch, NUNCA a main |

## Tabla de elementos del Chain Context

| Campo | Qué va | Ejemplo |
|-------|--------|---------|
| **Chain** | Nombre del feature o refactor | `auth-refactor` |
| **Tracker PR** | Número del tracker PR o "Not needed" | `#42` |
| **Position** | N de total | `2 of 4` |
| **Base** | Branch target | `feat/auth` |
| **Depends on** | PRs/issues que necesita antes | `#41 (token model)` |
| **Follow-up** | Próximo PR de la cadena | `#43 (user API)` |
| **Review budget** | Líneas cambiadas / 400 | `380 / 400` |
| **Starts at** | Estado inicial de este PR | `feat/login-flow branch` |
| **Ends with** | Resultado final de este PR | `login flow wired and tested` |

## Anti-patrones de chained PRs

| Anti-patrón | Problema | Solución |
|-------------|----------|----------|
| **Slice no autónomo** | El slice no funciona solo — depende del siguiente | Asegurar que cada slice compile y pase tests independientemente |
| **Child a main en Feature Branch** | Un child PR apunta a main en vez de a la feature branch | Verificar base del PR: `--base feat/my-feature` |
| **Sin mapa de cadena** | No hay diagrama ni tabla de estado | Agregar Chain Overview + Chain Status en cada PR |
| **Slice demasiado chico** | PR de 50 líneas que no es una unidad completa | Combinar slices que son parte de la misma unidad |
| **Slice demasiado grande** | PR de 700 líneas "porque igual ya lo partí en 2" | Partir mejor — máximo 400 por PR |
| **Tracker PR sin draft** | Tracker PR abierto como normal en vez de draft | Usar `--draft` + `no-merge` |
| **Rebase tarde** | Stacked PR espera a que todo esté listo para rebasar | Rebasar cada PR apenas el anterior mergea |
| **Scope creep en medio del chain** | PR 2 agrega algo que no estaba planeado porque "ya que estamos" | El scope de cada slice está fijo. Cambios son nuevo PR |

## Estrategias de splitting según tipo de cambio

| Tipo de cambio | Estrategia de split | Ejemplo |
|----------------|---------------------|---------|
| **Nuevo feature** | Por capa: model → logic → integration → UI/docs | `feat/auth: model + tests` → `feat/auth: service + tests` → `feat/auth: handler + tests` |
| **Refactor grande** | Por módulo: refactor módulo A → refactor módulo B → cleanup | `refactor(db): extract connection pool` → `refactor(db): migrate to new pool` |
| **Bug fix complejo** | Por causa: fix root cause → fix efectos secundarios → tests de regresión | `fix(parser): correct UTC offset` → `fix(api): adjust for correct timestamps` |
| **Migración de datos** | Por fase: schema migration → data migration script → verification | `feat(schema): add new columns` → `feat(migration): backfill data` |
| **Documentación grande** | Por tema: core docs → API docs → examples | `docs: rewrite getting started` → `docs: document all endpoints` |

## Diagramas de ejemplo

**Stacked PRs to main (3 PRs):**
```
main
 └── #41 feat: token model (✅ merged)
      └── #42 feat: login flow (📍 this PR)
           └── #43 feat: user API (⚪ pending)
```

**Feature Branch Chain (4 PRs + tracker):**
```
main
 └── #45 feat: auth refactor (tracker PR, 🟡 draft)
      ├── #41 feat: token model (✅ merged to feat/auth)
      ├── #42 feat: login flow (📍 this PR)
      ├── #43 feat: user API (🟡 open)
      └── #44 docs: auth docs (⚪ pending)
```

## Checklist pre-creación de cada chained PR

- [ ] **Autonomía:** El PR funciona solo (compila, tests pasan)
- [ ] **Scope único:** Un deliverable por PR
- [ ] **Budget:** < 400 líneas cambiadas
- [ ] **Verificación:** Tests o docs incluidos en este PR
- [ ] **Chain Context:** Incluye posición, dependencias, follow-up, diagrama, tabla de estado
- [ ] **Base correcta:** Stacked → PR anterior / Feature Branch → feature branch (NUNCA main)
- [ ] **Rollback:** Revertir no afecta otros slices
- [ ] **Tracker PR:** Si > 2 PRs, el tracker está en draft con status de cada slice

## Principios fundamentales

1. **400 líneas no es un número mágico.** Es el límite de lo que un humano procesa con atención. Respetalo.
2. **Cada PR es un entregable autónomo.** Si no funciona solo, no es un slice — es un fragmento.
3. **El mapa es obligatorio.** Sin diagrama de dependencias, el reviewer no sabe dónde está parado.
4. **La estrategia la elige el equipo, no el tool.** Stacked vs Feature Branch son tradeoffs, no dogmas.
5. **El tracker PR no es para review.** Es un mapa. Reviewá los child PRs, no el tracker.

> _El reviewer burnout es real. Cada línea que agregás a un PR es una línea que alguien tiene que leer. Si llegás a 400, partí. Si llegás a 800, ya deberías haber partido hace rato._
