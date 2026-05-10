---
name: lend-ai-docs
description: >
  Documentación senior — multi-archivo, Google-style docstrings, ADR,
  y documentación técnica en inglés.
  Trigger: Al escribir documentación, generar docstrings, o estructurar la documentación de un proyecto.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: lend-ai-docs

Documentación senior. Código sin docs es deuda técnica.

## Trigger

- Terminaste una función y necesitás su docstring
- Vas a crear o actualizar un README, ARCHITECTURE, o CHANGELOG
- Necesitás documentar una decisión de arquitectura (ADR)
- El proyecto no tiene documentación y hay que arrancarla

## Workflow LEND

1. ANALIZAR
   ├── Tipo: docstring (API pública), README (proyecto), ADR (decisión), guía (cómo usar)
   ├── Audiencia: ¿desarrollador, usuario, operador?
   ├── Estado: ¿docs desde cero o actualizar existentes?
   └── Lenguaje: inglés técnico US para código y commits

2. OFRECER (Menú del Senior)
   ├── A) Docstrings — Google-style para funciones y clases públicas
   ├── B) README + ARCHITECTURE — visión general del proyecto + estructura
   └── C) ADR — documentar decisión con contexto, opciones y resultado

3. ELEGIR → confirmación

4. HACER
   ├── Google-style: Args, Returns, Raises, Examples (cuando aplica)
   ├── README: qué hace, cómo instalar, cómo usar, configuración
   ├── ARCHITECTURE: estructura, agentes, skills, decisiones técnicas
   ├── ADR: título, contexto, opciones, decisión, consecuencias
   └── Inglés técnico US, claro y directo

5. VERIFICAR
   ├── La documentación es útil sin leer el código
   ├── Los ejemplos funcionan (ejecutables)
   └── No hay información desactualizada
