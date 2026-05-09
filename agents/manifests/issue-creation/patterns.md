# Patterns: Issue Creation

> _Un issue no es una queja. Es un caso de negocios. Si no tiene toda la data, no se puede aprobar._

## Tabla de decisión: bug, feature, o pregunta

| Situación | Tipo | Template | Labels automáticas |
|-----------|------|----------|-------------------|
| Algo funciona mal / da error / comportamiento incorrecto | **Bug** | Bug Report | `bug`, `status:needs-review` |
| Algo no existe y debería existir / se puede mejorar | **Feature Request** | Feature Request | `enhancement`, `status:needs-review` |
| "¿Cómo hago X?" / "¿Esto soporta Y?" | **Discussions** | NO es un issue | N/A |
| "No sé si es bug o feature" | **Discussions** primero | NO es un issue | N/A |

## Tabla de campos: Bug Report

| Campo | Requerido | Qué poner | Ejemplo |
|-------|-----------|-----------|---------|
| Pre-flight 1: no duplicate | ✅ | Checkbox marcado | ✅ |
| Pre-flight 2: entiendo workflow | ✅ | Checkbox marcado | ✅ |
| Bug Description | ✅ | Descripción clara del bug | "setup.sh falla con glob error en zsh" |
| Steps to Reproduce | ✅ | Pasos numerados desde estado limpio | "1. Clonar repo\n2. Correr ./scripts/setup.sh\n3. Ver error" |
| Expected Behavior | ✅ | Qué debería pasar | "El script debería instalar las skills" |
| Actual Behavior | ✅ | Qué pasa + evidencia | "Error: zsh: no matches found: skills/*" |
| Operating System | ✅ | Dropdown | macOS |
| Agent / Client | ✅ | Dropdown | Claude Code |
| Shell | ✅ | Dropdown | zsh |
| Relevant Logs | ❌ | Logs en bloque de código | (opcional pero muy útil) |
| Additional Context | ❌ | Screenshots, workarounds | (opcional) |

## Tabla de campos: Feature Request

| Campo | Requerido | Qué poner | Ejemplo |
|-------|-----------|-----------|---------|
| Pre-flight 1: no duplicate | ✅ | Checkbox marcado | ✅ |
| Pre-flight 2: entiendo workflow | ✅ | Checkbox marcado | ✅ |
| Problem Description | ✅ | El dolor o limitación actual | "Codex users tienen que copiar skills manualmente" |
| Proposed Solution | ✅ | Cómo debería funcionar | "Agregar --agent codex a setup.sh" |
| Affected Area | ✅ | Dropdown | Scripts |
| Alternatives Considered | ❌ | Otras approaches | "Instalación manual — no escala" |
| Additional Context | ❌ | Mockups, ejemplos de otros tools | "VSCode tiene un setup similar con --agent" |

## Tabla de labels y sus significados

| Label | Quién la asigna | Cuándo | Qué significa |
|-------|----------------|--------|---------------|
| `bug` | Automática (template) | Al crear bug report | Es un bug |
| `enhancement` | Automática (template) | Al crear feature request | Es una feature/mejora |
| `status:needs-review` | Automática (template) | Al crear issue | Necesita revisión del maintainer |
| `status:approved` | Maintainer | Después de review | Aprobado para implementar |
| `priority:high` | Maintainer | Si es crítico o urgente | Hay que implementarlo ya |
| `priority:medium` | Maintainer | Si es importante | Hay que implementarlo pronto |
| `priority:low` | Maintainer | Si es nice-to-have | Se implementa cuando se pueda |

## Anti-patrones de issues

| Anti-patrón | Cómo se ve | Problema | Solución |
|-------------|------------|----------|----------|
| **Issue sin template** | Cuerpo libre sin estructura | Falta información clave | Usar siempre Bug Report o Feature Request template |
| **Duplicate** | Mismo bug reportado 3 veces | Ruido, maintainer pierde tiempo | Buscar antes de crear |
| **Pregunta en issue** | "¿Cómo instalo esto?" | Issues no son para preguntas | Usar Discussions |
| **Título vago** | "No funciona" | No dice qué no funciona | `fix(scripts): setup.sh fails on zsh with glob error` |
| **Sin pasos para reproducir** | "Tira error" | El maintainer no puede reproducir | Pasos numerados desde estado limpio |
| **Expected vs Actual igual** | Expected: "que funcione". Actual: "no funciona" | No hay información útil | Sé específico: "debería mostrar menú" vs "tira exit code 1" |
| **Logs en screenshot** | Screenshot de terminal en vez de texto | No se puede copiar, no es searchable | Poner logs en bloque de código |
| **Unreproducible** | "A veces pasa" | Si no se puede reproducir, no se puede fixear | Dar condiciones exactas |
| **Feature sin problema** | "Agreguemos X" sin explicar por qué | No se justifica el esfuerzo | Explicar el problema que resuelve |
| **Issue con PR incluido** | Issue + PR en el mismo body | Bypass del flujo de approval | Issue primero, PR después del approval |

## Checklist antes de crear un issue

- [ ] **No es duplicado:** buscaste con `gh issue list --search "keyword"`
- [ ] **No es pregunta:** si es "¿cómo?", va a Discussions
- [ ] **Título semántico:** `tipo(scope): descripción` — `fix(scripts): setup fails on zsh`
- [ ] **Pre-flight checks:** ambos checkboxes marcados
- [ ] **Bug: steps to reproduce:** numerados, desde estado limpio, reproducibles por cualquiera
- [ ] **Bug: expected vs actual:** claramente diferenciados, con evidencia (logs, errores)
- [ ] **Bug: sistema:** OS, Agent/Client, Shell seleccionados
- [ ] **Feature: problem description:** el dolor actual está claramente explicado
- [ ] **Feature: proposed solution:** la solución está descrita desde la perspectiva del usuario
- [ ] **Feature: affected area:** seleccionada del dropdown
- [ ] **Sin información sensible:** no hay tokens, passwords, o datos personales

## Principios fundamentales

1. **Un issue no es un mensaje de Slack.** Es un contrato entre quien reporta y quien implementa. Debe ser completo, verificable y accionable.
2. **Los pasos para reproducir son lo más importante.** Si el maintainer no puede reproducir el bug, no lo va a fixear.
3. **Expected vs Actual no es opcional.** Es la definición misma del bug. Sin eso, no hay bug.
4. **Las preguntas van a Discussions.** Los issues son para trabajo pendiente, no para consultas.
5. **Primero el issue, después el PR.** No se escribe código hasta que el issue esté aprobado. No hay excepciones.

> _Un issue bien escrito es el 50% del trabajo de implementación ya hecho. El maintainer lo lee, lo entiende, lo aprueba, y el implementador sabe exactamente qué hacer. Un issue mal escrito es un ida y vuelta de comentarios que nadie tiene tiempo para mantener._
