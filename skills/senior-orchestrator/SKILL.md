---
name: senior-orchestrator
description: >
  Orquestación profesional del ecosistema — modelo routing, delegación
  de agentes, arquitectura y decisiones técnicas.
  Trigger: Cuando necesitás decidir qué modelo/tier usar, diseñar arquitectura, orquestar entre data/frontend/devops.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
---

# Skill: senior-orchestrator

Orquestación del ecosistema. Decidí qué agente, qué modelo, qué camino.

## Trigger

- Decidir qué modelo/tier usar para una tarea
- Diseñar arquitectura del ecosistema
- Delegar entre data-analyst, frontend-senior y devops
- Planear estrategia de modelos (local vs cloud)
- Configurar CI/CD, seguridad o infraestructura

## Workflow LEND

1. ANALIZAR
   ├── Tipo de tarea: data, frontend, devops, o transversal
   ├── Complejidad: mecánica, estándar, compleja, crítica
   ├── Contexto: consultar Engram por decisiones previas
   └── Presupuesto: ¿usar modelos gratis o pagos?

2. OFRECER (Menú del Senior)
   ├── A) Delegar a data-analyst — análisis, ML, reportes, ETL
   ├── B) Delegar a frontend-senior — React, CSS, testing, UX
   ├── C) Delegar a devops — infra, CI/CD, cloud, seguridad
   └── Si es transversal: commits-real, lend-ai-testing, lend-ai-docs, engram-memory-system

3. ELEGIR → el usuario confirma

4. HACER
   ├── Cargar skill del agente correspondiente
   ├── Configurar tier según modelo-routing.config.json
   ├── Diagnóstico de MCPs antes de usar (si fallan, post-mortem)
   ├── Cada cambio arquitectónico → ADR (Architecture Decision Record)
   └── Registrar en Engram toda decisión técnica

5. VERIFICAR
   ├── La tarea se completó en el agente correcto
   ├── Los MCPs funcionaron
   └── Engram tiene registro de la decisión

## Patrones

- **Siempre preguntar antes de decidir**: mostrar 2+ opciones con pros/contras
- **Nunca cambiar model-routing.config.json sin registrar en Engram**
- **Cada cambio arquitectónico requiere ADR**
- **MCPs se diagnostican antes de usar**
- **Engram siempre**: toda decisión técnica se persiste

## Anti-patrones

- ❌ Delegar sin consultar Engram primero — perdés contexto de decisiones previas
- ❌ Cambiar tiers sin registrar — nadie sabe por qué se usó T5 en una tarea simple
- ❌ No diagnosticar MCPs antes de usarlos — "esto no funciona" a mitad de camino
- ❌ Ignorar al usuario cuando es vago — preguntá hasta tener especificaciones claras
