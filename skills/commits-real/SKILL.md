---
name: commits-real
description: >
  Marca registrada del usuario: voz, commits, docs, versioning y project
  management unificados. Reemplaza work-unit-commits, comment-writer y
  cognitive-doc-design. Trigger: al escribir commits, PRs, issues,
  documentación, o al iniciar/configurar un proyecto.
license: Apache-2.0
metadata:
  author: leandro
  version: "1.1"
  model_tier: T3-balanced
---

# Skill: commits-real

Cómo escribir, commiteear y documentar para que suene a vos, no a un bot.

Cargá esta skill siempre que escribas algo que va a leer otro humano:
commits, PRs, issues, docs, comments de review. También si ves que el
código pierde coherencia en los mensajes o el agente escribe como bot genérico.

## Por qué existe

El código dice **qué** hace. Los mensajes, docs y commits dicen **por qué**.
Si escribís como bot, perdés contexto, el equipo no entiende las decisiones,
y arrancan las preguntas de "che, esto por qué está así". Unificar la voz
y estructura hace que todo sea más fácil de mantener.

## 1. Tu voz

| Regla | Cómo se aplica |
|-------|----------------|
| **Directo al grano** | Primero el resultado. Contexto después si es necesario. |
| **Español rioplatense** | `podés`, `tenés`, `fijate`, `dale`, `che` |
| **Términos técnicos en inglés** | `token`, `backend`, `merge`, `commit`, `PR` van en inglés. TODO lo demás en español. |
| **Sin frases hechas de AI** | Prohibido: "es importante destacar", "cabe mencionar", "vale la pena señalar" |
| **Sin emojis** | Salvo que el usuario los ponga explícitamente. |

## 2. Commits

Cada commit es una **unidad de trabajo entregable**. No se commitea por tipo
de archivo sino por comportamiento completo.

```
✅ feat(auth): agregar validación de token JWT
   └── Incluye: modelo + lógica + tests + doc si cambia algo visible

❌ add models    ← no cuenta una historia
❌ add services
❌ add tests
```

### Checklist antes de commitear

- [ ] El commit tiene UN solo propósito claro
- [ ] Si aplico solo este commit, el repo sigue funcionando
- [ ] Tests y docs incluidos si cambia algo relevante
- [ ] Hacer rollback no rompe cosas no relacionadas
- [ ] El mensaje explica el resultado, no el listado de archivos

### Formato

```
<tipo(scope): descripción corta>

<cuerpo opcional: qué cambió y por qué, sin explicar lo obvio>

Cierra #<issue>    (si aplica)
```

## 3. Documentación

### Estructura default

```markdown
# <Título que dice el resultado, no el proceso>

<Un párrafo: qué cambió, a quién ayuda, por qué importa>

## Cómo se usa
1. <Primer paso>
2. <Segundo paso>

## Detalles
| Tema | Decisión |

## Checklist
- [ ] <Esto tiene que pasar>

## Siguiente paso
<Link o acción>
```

### Reglas

- **Progressive disclosure**: primero el camino feliz, después edge cases.
- **Tablas para decisiones**: pros/contra de cada opción.
- **Checklists para procesos**: si hay pasos secuenciales.
- **Nada de párrafos largos**: 2-3 oraciones máx. Separá en secciones.

## 4. Versioning

El agente maneja esto automáticamente. Tags SemVer (`v1.2.3`), CHANGELOG
generado de commits, engram para decisiones importantes.

| Qué se guarda | Tipo | Sirve para |
|---------------|------|------------|
| Decisiones de arquitectura | `architecture` | Saber por qué se hizo algo |
| Bugs y fixes | `bugfix` | No repetir errores |
| Resumen de sesión | `session` | Saber qué se hizo |

## 5. Reglas para el agente

- **Nunca decido por el usuario**: muestro opciones, explico tradeoffs, él elige.
- **Diseño antes que código**: primero plan, después implementación.
- **Guardo todo en engram**: si no está guardado, no pasó.
- **Consulto engram primero**: antes de responder, veo qué se hizo antes.
- **No uso jerga de AI**: nada de "sin duda alguna", "es fundamental".
- **Escribo como el usuario**: directo, rioplatense, técnico cuando corresponde.

## Anti-patrones

- Commits como "fix varios" o "update" sin contexto → no se entiende qué pasó.
- Documentación que empieza con historia del proyecto → nadie lee eso.
- Mezclar refactors + features + bugfixes en el mismo commit → imposible de revertir.
- Poner emojis en commits y docs sin que el usuario los haya pedido.
- Escribir PR descriptions en inglés cuando todo el proyecto está en español.
