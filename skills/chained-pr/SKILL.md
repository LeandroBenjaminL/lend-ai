---
name: chained-pr
description: >
  PRs encadenados para cambios grandes — dividí un PR de 1000 líneas en
  PRs más chicos que se revisan en secuencia.
  Trigger: Cuando un PR supera 400 líneas cambiadas, o al planificar PRs encadenados.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
  model_tier: T2-fast
---

# Skill: chained-pr

PRs grandes partidos en PRs chicos. 400 líneas o menos por PR.

## Trigger

- Un PR tiene más de 400 líneas
- Un cambio grande se puede dividir en pasos lógicos
- Necesitás coordinar múltiples PRs que dependen entre sí

## Workflow LEND

1. ANALIZAR
   ├── Total de cambios: ¿cuántas líneas? ¿cuántos archivos?
   ├── Dependencias: ¿los cambios se pueden aislar o dependen entre sí?
   ├── Orden lógico: ¿qué PR tiene que mergearse primero?
   └── Base: todos contra main o develop

2. OFRECER (Menú del Senior)
   ├── A) 2 PRs — PR1: refactor/cleanup, PR2: la feature nueva
   ├── B) 3 PRs — PR1: preparación, PR2: lógica central, PR3: integración
   └── C) N PRs — secuencia de PRs pequeños, cada uno < 400 líneas

3. ELEGIR → confirmación

4. HACER
   ├── PR1 base → main, PR2 base → PR1 (target branch = PR1)
   ├── Cada PR: < 400 líneas, enfocado en un solo cambio lógico
   ├── Descripción: link al PR anterior y siguiente en la cadena
   ├── Mergear en orden: PR1 → main, PR2 → main (después de PR1)
   └── Si PR1 cambia → PR2 necesita rebase

5. VERIFICAR
   ├── Cada PR tiene < 400 líneas
   ├── La cadena tiene sentido lógico
   └── No hay conflictos entre PRs de la cadena
