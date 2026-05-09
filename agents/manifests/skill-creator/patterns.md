# Patterns: Skill Creator

> _Una skill no es documentación. Es conocimiento destilado y ejecutable. Si la IA tiene que leer 100 líneas para encontrar lo que necesita, la skill está mal diseñada._

## Tabla de decisión: crear una skill o no

| Pregunta | Sí → crear skill | No → no crear |
|----------|------------------|---------------|
| ¿El patrón es recurrente (semanal/mensual)? | ✅ Skill necesaria | ❌ No crear (es one-off) |
| ¿Ya hay documentación clara? | ❌ Referenciar la doc, no crear skill | ✅ Crear skill si la doc es muy larga o dispersa |
| ¿La IA comete errores sin esta skill? | ✅ Skill necesaria | ❌ No es necesaria |
| ¿Es conocimiento tácito del equipo? | ✅ Skill necesaria | ❌ Ya está documentado |
| ¿Es específico de un proyecto (no reusable)? | ⚠️ Skill específica del proyecto | ❌ Skill muy específica que cambia seguido |
| ¿El patrón es trivial (obvio para cualquier IA)? | ❌ No crear | ✅ No crear |

## Tabla de estructura de SKILL.md

| Sección | Propósito | Obligatorio | Extensión recomendada |
|---------|-----------|-------------|----------------------|
| **Frontmatter** | Metadata: name, description, trigger, license, version | ✅ Sí | 5-10 líneas |
| **When to Use** | Cuándo cargar la skill | ✅ Sí | 3-5 bullets |
| **Critical Patterns** | Reglas clave, tablas de decisión, constraints | ✅ Sí | 10-30 líneas |
| **Code Examples** | Ejemplos mínimos, un problema cada uno | Recomendado | 10-40 líneas |
| **Commands** | Comandos que la IA necesita ejecutar | Recomendado | 3-8 comandos |
| **Resources** | Links a assets/ y references/ | Si aplica | 2-5 líneas |

## Tabla de naming conventions

| Tipo de skill | Pattern | Ejemplos |
|---------------|---------|----------|
| Tecnología | `{technology}` | `pytest`, `playwright`, `typescript` |
| Proyecto específica | `{project}-{component}` | `myapp-api`, `myapp-ui` |
| Testing | `{project}-test-{component}` | `myapp-test-sdk`, `myapp-test-api` |
| Workflow | `{action}-{target}` | `skill-creator`, `jira-task` |
| Documentación | `{concept}-doc` | `cognitive-doc-design` |

## Tabla de model_tier

| Tier | Uso | Características | Cuándo usarlo |
|------|-----|-----------------|---------------|
| **T2-fast** | Skills simples, workflows cortos | Rápido, económico | comment-writer, branch-pr, issue-creation, skill-registry |
| **T3-balanced** | Skills con patrones y ejemplos | Balanceado, buena calidad | cognitive-doc-design, go-testing, skill-creator, work-unit-commits |
| **T4-reasoning** | Skills complejas con decisiones | Más lento pero más profundo | judgment-day (orquestración adversarial) |

## Tabla de decisión assets/ vs references/

| Necesitás | Tipo | Dónde va |
|-----------|------|----------|
| Code templates | Asset | `assets/template.py` |
| JSON schemas | Asset | `assets/schema.json` |
| Example configs | Asset | `assets/config.example.yaml` |
| Link a docs locales | Reference | `references/docs.md` |
| Link a guías externas | Reference (con path local) | `references/guides.md` |
| Diagramas/imágenes | Asset | `assets/diagram.png` |

## Anti-patrones de skills

| Anti-patrón | Cómo se ve | Problema | Solución |
|-------------|------------|----------|----------|
| **Skill-doc** | 200 líneas que son un wiki | La IA nunca termina de leer | Destilar a patrones críticos + ejemplos mínimos |
| **Trigger vago** | "Testing" sin especificar lenguaje | La IA carga la skill cuando no corresponde | "Go testing, table-driven tests, teatest, Bubbletea" |
| **Sin código** | Solo texto, ningún ejemplo | La IA no sabe cómo aplicar el patrón | Agregar ejemplos mínimos por patrón |
| **Sin comandos** | No dice qué ejecutar | La IA no sabe cómo verificar | Incluir `go test ./...`, `shellcheck scripts/*.sh`, etc. |
| **Over-engineering** | Skill para un patrón que pasa 1 vez al año | No justifica el effort | Crear reference doc en vez de skill |
| **Skill duplicada** | Misma skill en user y project level | Confusión, reglas contradictorias | Deduplicar: project-level gana |
| **Sin frontmatter** | SKILL.md sin `---` metadata | El sistema no puede parsear la skill | Siempre incluir name, description (con trigger), license |
| **Referencias web** | URLs externas en vez de paths locales | La URL puede morir, no hay offline | Descargar local o referenciar path local |
| **Ejemplos largos** | 50 líneas de ejemplo para un patrón simple | La IA se pierde en el ejemplo | Máximo 15 líneas por ejemplo, uno por concepto |
| **Keywords section** | `## Keywords: testing, go, golang` | No sirve — el frontmatter description es lo que se parsea | Poner keywords en el trigger del frontmatter |

## Checklist pre-creación

- [ ] La skill no existe en `skills/`
- [ ] El patrón es recurrente (no one-off)
- [ ] El nombre sigue las convenciones
- [ ] El frontmatter tiene: name, description (con trigger), license, author, version
- [ ] Los Critical Patterns son accionables (no teoría)
- [ ] Los code examples son mínimos (un problema por ejemplo)
- [ ] Los commands son copiables (incluyen flags si hacen falta)
- [ ] assets/ o references/ existen si corresponden
- [ ] La skill se registró en AGENTS.md
- [ ] Se corrió `skill-registry` para actualizar el registro

## Principios fundamentales

1. **El trigger es lo más importante.** Si la IA no sabe cuándo cargar la skill, la skill no existe.
2. **Destilá, no documentés.** Cada línea debe ser algo que la IA necesita SABER, no algo que está BUENO SABER.
3. **Menos es más.** Una skill de 50 líneas bien escritas vale más que una de 200 líneas que la IA nunca termina de leer.
4. **Ejemplos mínimos.** Un ejemplo por concepto, máximo 15 líneas. Mostrá el patrón, no el contexto.
5. **Sin duplicación.** Si la documentación ya existe y es clara, referenciala. No la reescribas como skill.

> _El mejor skill es el que la IA lee y dice "ah, claro, así se hace". No necesita leerlo dos veces. No necesita entender "por qué". Solo necesita saber exactamente qué hacer._
