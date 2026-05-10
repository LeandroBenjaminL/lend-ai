---
name: gitops-engineer
description: >
  Git workflows, branching strategies, release management, versionado
  semántico, conventional commits y automatización git.
  Trigger: Cuando necesitás diseñar branching strategy, automatizar releases, configurar hooks o gestionar versionado.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# Skill: gitops-engineer

GitOps. Git es la fuente de verdad de todo.

## Trigger

- Diseñar branching strategy para un proyecto
- Automatizar releases y changelogs
- Configurar hooks de git (pre-commit, pre-push)
- Definir versionado semántico y conventional commits
- Resolver conflictos de merge o problemas de historial

## Workflow LEND

1. ANALIZAR
   ├── Stack: GitHub, GitLab, Gitea, Azure DevOps
   ├── Equipo: ¿solo, 2-5, 5+ personas?
   ├── Estrategia actual: ¿trunk-based, GitHub Flow, Git Flow?
   └── Releases: ¿manual, automático, semver?

2. OFRECER (Menú del Senior)
   ├── A) Trunk-based — commits directos a main, feature flags, ideal para CI/CD
   ├── B) GitHub Flow — branches por feature, PRs a main, simple y efectivo
   └── C) Git Flow — develop/main, release branches, hotfixes, para proyectos con ciclos largos

3. ELEGIR → confirmación

4. HACER
   ├── Branch protection: requerir PRs, approvals, status checks, linear history
   ├── Hooks: pre-commit (lint + format + secrets), commit-msg (conventional)
   ├── Release: etiquetas semver, changelog automático (git-cliff o semantic-release)
   ├── Conventional commits: feat, fix, chore, docs, refactor, test, style
   ├── Merge strategies: squash (trunk-based), merge commit (Git Flow), rebase (historia limpia)
   └── Automatización: GitHub Actions para validar commits y PRs

5. VERIFICAR
   ├── Las reglas de branch protection están activas
   ├── Los hooks corren sin errores
   └── Una release de prueba genera el changelog correctamente
