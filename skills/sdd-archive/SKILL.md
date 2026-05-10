---
name: sdd-archive
description: >
  Cierra el ciclo SDD: sincroniza specs delta a specs principales y mueve
  el cambio al archivo. Consolidar, no tirar cosas.
  Trigger: Después de verify exitoso. Nunca archivar con issues CRITICAL abiertos.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "2.0"
---

# Skill: sdd-archive

Archivo SDD. Consolidar el cambio y cerrar el ciclo.

## Trigger

- La verificación fue exitosa
- Todos los issues CRITICAL están resueltos
- El cambio está listo para mergear

## Workflow LEND

1. ANALIZAR
   ├── Estado: ¿todos los escenarios PASS? ¿hay warnings?
   ├── Specs delta: ¿qué cambió respecto a los specs originales?
   ├── Issues: ¿hay issues abiertos? ¿cuáles son aceptables?
   └── Merge: ¿está listo para mergear a main?

2. OFRECER (Menú del Senior)
   ├── A) Archive simple — mergear + marcar cambio como completado
   ├── B) Archive con sync — actualizar specs principales con delta + merge
   └── C) Archive completo — sync specs + merge + engram + changelog

3. ELEGIR → confirmación

4. HACER
   ├── Sincronizar specs delta a specs principales
   ├── Mergear cambio a la branch principal
   ├── Actualizar CHANGELOG si aplica
   ├── Guardar en engram: qué cambió, por qué, resultados
   └── Cerrar issues relacionados

5. VERIFICAR
   ├── El merge se completó sin conflictos
   ├── Los specs principales reflejan el nuevo comportamiento
   └── Engram tiene registro del cambio
