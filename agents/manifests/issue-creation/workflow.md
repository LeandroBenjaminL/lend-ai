# Workflow: Issue Creation

## Flujo principal

```
Orchestrator → [1. Buscar duplicados] → [2. Clasificar tipo] → [3. Elegir template] → [4. Completar campos] → [5. Verificar pre-flight] → [6. Crear issue] → Orchestrator
```

## Paso a paso

### 1. Buscar issues duplicados

Antes de crear NADA, buscás si ya existe un issue similar.

```bash
gh issue list --search "keyword" --state all
```

- **Buscás por palabras clave** del problema o feature que querés reportar.
- **Revisás issues cerrados también** — a veces el mismo bug ya se reportó y se cerró como duplicado o wontfix.
- **Si existe un duplicado:** no creás uno nuevo. Comentás en el existente con info adicional si tenés.
- **Si hay uno similar pero no igual:** mencionás la relación en el nuevo issue: "Relacionado con #42 pero este es un caso distinto porque..."

_"Crear un issue duplicado es el equivalente a mandar un email sin revisar si ya te respondieron. Le robás tiempo al maintainer."_

### 2. Clasificar el tipo de issue

Usás el árbol de decisión:

```
¿Es un bug?
├── Sí → Bug Report template
├── ¿Es una feature nueva o mejora?
│   ├── Sí → Feature Request template
│   └── No → ¿Es una pregunta?
│       ├── Sí → Discussions, NO issues
│       └── No → ¿Es un duplicado? → Linkear y cerrar
└── No → (ninguno de los anteriores) → Evaluar si realmente es un issue
```

**Bug** = algo que funciona distinto a lo esperado. Se rompió, da error, comportamiento incorrecto.

**Feature request** = algo que no existe y debería existir, o algo que existe y podría funcionar mejor.

**Pregunta** = "¿cómo hago X?", "¿esto soporta Y?" → va a Discussions, no a Issues.

**Duda** = si no estás seguro de si es bug o feature, preguntá primero en Discussions.

_"Si es una pregunta, no es un issue. Los issues son para trabajo pendiente, no para consultas."_

### 3. Elegir el template correcto

Cada template tiene campos distintos. Elegís el que corresponde:

**Bug Report (`.github/ISSUE_TEMPLATE/bug_report.yml`):**
- Auto-labels: `bug`, `status:needs-review`
- Requiere: descripción del bug, pasos para reproducir, expected vs actual behavior, OS, Agent/Client, Shell

**Feature Request (`.github/ISSUE_TEMPLATE/feature_request.yml`):**
- Auto-labels: `enhancement`, `status:needs-review`
- Requiere: descripción del problema, solución propuesta, área afectada

No existen otros templates. Si no matchea con ninguno, no es un issue.

### 4. Completar todos los campos obligatorios

**Bug Report — campos requeridos:**

| Campo | Qué poner |
|-------|-----------|
| **Pre-flight Checks** | Marcar AMBOS: no es duplicado + entiendo el workflow de approval |
| **Bug Description** | Descripción clara del bug. Qué está pasando. |
| **Steps to Reproduce** | Pasos numerados. Desde el estado inicial hasta el error. |
| **Expected Behavior** | Qué debería pasar si funcionara bien. |
| **Actual Behavior** | Qué pasa en realidad. Incluir errores, logs, screenshots. |
| **Operating System** | Seleccionar del dropdown: macOS, Linux, Windows, WSL |
| **Agent / Client** | Seleccionar: Claude Code, OpenCode, Gemini CLI, Cursor, Windsurf, Codex, Other |
| **Shell** | Seleccionar: bash, zsh, fish, Other |

**Feature Request — campos requeridos:**

| Campo | Qué poner |
|-------|-----------|
| **Pre-flight Checks** | Marcar AMBOS |
| **Problem Description** | El dolor o limitación actual. Por qué esto es necesario. |
| **Proposed Solution** | Cómo debería funcionar desde la perspectiva del usuario. |
| **Affected Area** | Seleccionar: Scripts, Skills, Examples, Documentation, CI/Workflows, Other |

**Reglas de escritura del body:**

- **Título del issue:** `tipo(scope): descripción` — `fix(scripts): setup fails on zsh`, `feat(auth): add token refresh`
- **Pasos para reproducir:** numerados, desde un estado limpio. Asumí que el maintainer no tiene contexto.
- **Expected vs Actual:** no seas vago. "La página debería cargar" vs "La página tira error 500".
- **Logs:** incluilos en bloque de código. No screenshots de logs.
- **Screenshots:** solo si agregan valor que el texto no captura.

### 5. Verificar pre-flight checks antes de enviar

Antes de crear el issue, verificás:

- [ ] No es un duplicado (buscaste con `gh issue list --search`)
- [ ] No es una pregunta (va a Discussions)
- [ ] Llenaste TODOS los campos requeridos del template
- [ ] Los pasos para reproducir son accionables desde un estado limpio
- [ ] El expected behavior está claramente definido
- [ ] El actual behavior incluye evidencia (logs, errores)
- [ ] El título sigue el formato `tipo(scope): descripción`
- [ ] Entendés que el issue arranca con `status:needs-review` y necesita approval para PR

### 6. Crear el issue

```bash
# Bug report
gh issue create --template "bug_report.yml" \
  --title "fix(scripts): setup.sh fails on zsh with glob error" \
  --body-file body.md

# Feature request
gh issue create --template "feature_request.yml" \
  --title "feat(scripts): add Codex support to setup.sh" \
  --body-file body.md
```

**Después de crear:**
- El issue se crea automáticamente con `status:needs-review` y la label de tipo (`bug` o `enhancement`).
- Esperás a que un maintainer agregue `status:approved` antes de abrir cualquier PR.
- Si el maintainer pide cambios, los hacés en el mismo issue (editando el body o comentando).

### Output final

Tu entregable al orchestrator es:

1. **URL del issue creado** (`gh issue view <number>`)
2. **Labels asignadas** automáticamente
3. **Status actual** (siempre `status:needs-review` al inicio)
4. **Próximo paso esperado** (esperar `status:approved` del maintainer)

_"Un issue bien escrito es un caso de negocios. El maintainer tiene que poder leerlo y decidir en 2 minutos si vale la pena implementarlo. Si necesita pedir más info, el issue está incompleto."_
