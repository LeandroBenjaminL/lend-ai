# Skill: sdd-explore

## Qué es

Investiga el código y el dominio del problema ANTES de proponer un cambio. La fase más barata de todo el ciclo SDD: zero commitment.

**El principio**: explorar = entender antes de actuar. No escribas código ni tomes decisiones hasta no tener claro el terreno.

## Trigger

El orquestador te llama para investigar una idea, feature, bug o área del código antes de decidir si amerita un cambio formal.

## Workflow

### 1. Entendé el pedido
- ¿Es feature nueva, bugfix, refactor, deuda técnica?
- ¿Qué domains toca? ¿Específico o vago?

### 2. Investigá el codebase
```
LEER:
├── Entry points y módulos relevantes
├── Funcionalidad relacionada (grep por keywords)
├── Tests existentes (qué se testea, qué no)
├── Patrones en uso (cómo se hacen cosas similares)
└── Dependencias y acoplamiento
```

### 3. Analizá opciones
Si hay múltiples approach, compáralos en tabla:

| Approach | Pros | Contras | Complejidad |
|----------|------|---------|-------------|
| A | ... | ... | Baja/Media/Alta |
| B | ... | ... | Baja/Media/Alta |

### 4. Persistí el resultado
- Con change name: `sdd/{change-name}/explore`
- Sin change name (standalone): `sdd/explore/{topic-slug}`
- Modo `openspec`: creá `exploration.md` adentro del change folder

### 5. Devolvé el análisis estructurado

```markdown
## Exploration: {topic}

### Current State
{Cómo funciona hoy el sistema en esta área}

### Affected Areas
- `path/to/file` — {por qué}

### Approaches
1. **{Nombre}** — {descripción}
   - Pros: {lista}
   - Contras: {lista}
   - Effort: Baja/Media/Alta

### Recommendation
{approach recomendado y por qué}

### Risks
- {riesgo}

### Ready for Proposal
{Sí/No}
```

## Ejemplos

1. **Explorar feature de caché**: Leés el código de la API, ves que no hay capa de caché, encontrás un middleware pattern existente, recomendás usar Redis con una lib ya en el proyecto.

2. **Explorar bug de auth**: Investigás el flujo de login, encontrás que el token JWT no expira, recomendás agregar `exp` claim sin cambiar la lib de auth.

3. **Explorar refactor de reporting**: Leés los reportes actuales (generan HTML inline), encontrás que ya hay una dependencia de templates sin usar, recomendás migrar a templates.

## Reglas

- **NO modifiques código ni archivos** — solo investigás y reportás
- Leé código REAL, no adivinés
- Si te falta info, decilo claramente
- Si el pedido es muy vago, decí qué necesitás para clarificarlo
- Mantené el análisis CONCISO — el orquestador necesita un resumen, no una novela

## Anti-patrones

- ❌ **Arrancar a codear sin explorar**: Vas a implementar algo que no entendés bien
- ❌ **Dar un approach único sin alternativas**: Siempre mostrá opciones con pros/cons
- ❌ **Recomendar sin leer el código real**: No es exploración, es especulación
- ❌ **Hacer un análisis de 50 páginas**: Sé conciso, el resto está en el codebase
