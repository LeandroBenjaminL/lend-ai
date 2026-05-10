# ADR-002: Sistema de tiers para modelos (T1-T5)

**Estado**: Aceptado

## Contexto

El ecosistema necesita usar distintos modelos de IA según la complejidad de la tarea. Tareas mecánicas (formateo, linting) no requieren un modelo potente, mientras que diseño de arquitectura o ML complejo sí.

Alternativas consideradas:
- Usar un solo modelo para todo (caro y lento para tareas simples)
- OpenRouter/LiteLLM como proxy externo
- **Elegido**: Sistema propio de tiers mapeado a modelos concretos

## Decisión

Definir 5 tiers (T1-T5) con capacidad creciente:

| Tier | Uso |
|------|-----|
| T1 | Tareas mecánicas (limpieza, formateo) |
| T2 | Reportes simples, validaciones |
| T3 | EDA, análisis general (default) |
| T4 | Arquitectura, ML complejo |
| T5 | Problemas muy difíciles |

El mapping de tier a modelo concreto se configura en `model-routing.config.json`. Un script (`model-commands.py`) permite listar y cambiar modelos sin tocar código.

## Consecuencias

- **Positivas**: Flexibilidad total para swap de modelos sin cambios de código. Costo optimizado (tareas baratas → modelos baratos). Claridad para el agente sobre qué nivel de capacidad usar.
- **Negativas**: Complejidad operativa adicional (routing, config). Dependencia de `model-router.py` y scripts asociados.
- **Neutras**: Permite migrar suavemente entre proveedores (Minimax ↔ DeepSeek ↔ otros).
