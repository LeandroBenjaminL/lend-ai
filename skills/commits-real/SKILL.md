---
name: commits-real
description: >
  Commits, documentación y versioning unificados — conventional commits,
  changelog, versionado semántico y mensajes que no son una vergüenza.
  Trigger: Al escribir commits, PRs, issues, documentación, o al iniciar/configurar un proyecto.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T3-balanced
---

# Skill: commits-real

Commits que cuentan una historia. No mensajes pedorros.

## Trigger

- Vas a escribir un commit
- Creás un PR o un issue en GitHub
- Necesitás generar o actualizar un CHANGELOG
- Configurás versionado semántico para un proyecto

## Workflow LEND

1. ANALIZAR
   ├── ¿Qué cambió? archivos, funcionalidad, bug fix, refactor?
   ├── Scope: ¿qué módulo/componente? (api, ui, data, infra)
   ├── Breaking: ¿rompe compatibilidad hacia atrás?
   └── ¿Hay issues/PRs relacionados?

2. OFRECER (Menú del Senior)
   ├── A) Conventional Commit simple — feat/fix/chore/docs/refactor + mensaje corto
   ├── B) Commit con cuerpo — conventional commit + descripción + issue link
   └── C) Estructura completa — conventional commit + breaking change + changelog update

3. ELEGIR → confirmación

4. HACER
   ├── Formato: `tipo(scope): mensaje` (feat, fix, chore, docs, refactor, test, style)
   ├── Mensaje: imperativo, presente, < 50 chars título, < 72 cuerpo
   ├── Breaking: `feat(api): eliminar endpoint obsoleto\n\nBREAKING CHANGE: ...`
   ├── Commits atómicos: un cambio por commit, no "varios fixes"
   ├── Issues: `Closes #123` o `Refs #456` en el cuerpo
   └── Versionado: semver (major.minor.patch) según conventional commits

5. VERIFICAR
   ├── El mensaje sigue el formato conventional commit
   ├── No hay archivos no relacionados en el commit
   └── Si es breaking, está documentado
