# Skill: sdd-archive

## Qué es

Cierra el ciclo SDD: sincroniza los specs delta a los specs principales (fuente de verdad) y mueve el cambio al archivo.

**El principio**: el archive no es "tirar cosas", es consolidar. Los specs ahora describen el nuevo comportamiento. El cambio pasa a ser el audit trail.

## Trigger

El orquestador te llama después de verify exitoso (o con warnings aceptados). Nunca archivar un cambio con issues CRITICAL abiertos.

## Workflow

### 1. Leé todos los artifacts del cambio
Necesitás: proposal, spec, design, tasks, verify-report.

### 2. Sincronizá delta specs → main specs (solo openspec/hybrid)

Por cada delta spec en `changes/{change-name}/specs/`:

**Si el main spec existe** (`specs/{domain}/spec.md`):
```
POR CADA sección en el delta spec:
├── ADDED → append a la sección Requirements del main spec
├── MODIFIED → reemplazá el requirement matching por nombre
└── REMOVED → borrá el requirement del main spec
```

**Si el main spec NO existe**: el delta es un spec completo → copialo directo.

**Cuidado**: preservá todos los requirements que NO están en el delta. Match por nombre (### Requirement: X).

### 3. Mové a archive
```
openspec/changes/{change-name}/
  → openspec/changes/archive/YYYY-MM-DD-{change-name}/
```

### 4. Verificá el archive (openspec/hybrid)
- [ ] Main specs actualizados
- [ ] Change folder movido a archive
- [ ] Active changes ya no tiene este cambio

### 5. Persistí archive report
- artifact: `archive-report`, topic_key: `sdd/{change-name}/archive-report`

### 6. Devolvé summary

```markdown
## Change Archived
**Change**: {name}
**Archived**: openspec/changes/archive/YYYY-MM-DD-{name}/

### Specs Synced
| Domain | Action | Details |
|--------|--------|---------|
| {domain} | Created/Updated | {N added, M modified, K removed} |

### SDD Cycle Complete
explore → propose → spec → design → tasks → apply → verify → archive
```

## Ejemplos

1. **Archive de "add-rate-limiting"**: Tenés 2 deltas specs (rate-limiting, user-auth). Actualizás ambos main specs. El cambio se mueve a `archive/2026-05-08-add-rate-limiting/`.

2. **Archive con destructive merge**: Un delta REMOVED borra medio spec. WARN al orquestador: "Se van a borrar 8 requirements — ¿confirmás?".

3. **Archive en modo engram**: No hay filesystem. El archive report en Engram con todos los observation IDs es el audit trail.

## Reglas

- **NUNCA** archivés un cambio con issues CRITICAL en verify
- Sincronizá specs ANTES de mover a archive
- Preservá requirements que no están en el delta
- Formato ISO para prefijo del archive folder
- Si el merge es destructivo (remueve mucho), WARN y pedí confirmación
- El archive es AUDIT TRAIL — no borrés ni modifiqués cambios archivados

## Anti-patrones

- ❌ **Archivar sin verificar**: Si verify no pasó, no se archiva
- ❌ **Sincronización parcial**: Copiás solo un delta spec y perdés los otros
- ❌ **Machacar el main spec**: Reemplazás todo el archivo en vez de mergear solo los cambios
- ❌ **Borrar el change folder sin archivar**: Perdés el audit trail
