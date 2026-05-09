---
description: Configura un pipeline ETL — extracción, limpieza, transformación y carga automatizada
agent: data-analyst
subtask: true
---

Creá un pipeline ETL automatizado para procesamiento de datos recurrente.

FLUJO:
1. Preguntá al usuario: fuente de datos, transformaciones, destino, frecuencia
2. Generá estructura de pipeline:
   - `pipeline.py` con funciones extract, transform, load
   - `config.yaml` con parámetros configurables
   - Script de ejecución programada
3. Incluí logging y manejo de errores
4. Mostrá el plan antes de escribir archivos

SKILLS A CARGAR:
- etl-pipelines
- python-environment

REGLAS:
- No sobrescribas archivos sin preguntar
- Usá logging, no prints
- Incluí type hints en las funciones
- Agregá un pequeño test de humo
