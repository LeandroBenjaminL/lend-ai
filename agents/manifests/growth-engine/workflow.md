# Growth Engine — Workflow

## Ciclo automático (después de cada sesión o interacción significativa)

```
1. ESCANEAR
   ├── mem_context → ¿qué pasó en esta sesión?
   ├── git log --oneline → ¿qué commits se hicieron?
   ├── Leer CHANGELOG → ¿qué versión se alcanzó?
   └── Leer Archivos modificados → ¿qué áreas se tocaron?

2. DETECTAR PATRONES
   ├── ¿Hay bugs recurrentes? → tipo, área, frecuencia
   ├── ¿Hay tareas que costaron más de lo esperado? → ¿por qué?
   ├── ¿Hay gaps de herramientas? → ¿qué skill falta?
   ├── ¿Hay desconexiones YAML/persona/skills? → inconsistency report
   └── ¿Hay patrones que emergen? → candidate for new skill

3. GUARDAR APRENDIZAJES
   ├── mem_save cada aprendizaje con:
   │   ├── type: "learning" o "discovery" o "pattern"
   │   ├── topic_key: "learning/{area}" para que evolucione
   │   ├── content: What/Why/Where/Learned
   │   └── scope: "project"
   ├── Si es recurrente (3+ veces):
   │   └── type: "pattern" + proponer acción
   └── Si es un gap de herramienta:
       └── type: "discovery" + sugerir nueva skill

4. MEJORAR (si aplica)
   ├── ¿Detectaste un gap que una nueva skill resolvería?
   │   └── Proponer al usuario: "Che, Míster. Esto ya pasó X veces.
   │       ¿Creo una skill '{nombre}' para manejarlo?"
   ├── ¿Hay entradas de Engram desorganizadas?
   │   └── Consolidar, re-clasificar, agregar topic_keys
   └── ¿El AGENTS.md o README están desactualizados?
       └── Actualizar sin preguntar (es documentación, no código)

5. REPORTAR
   └── Resumen corto al usuario: qué aprendimos, qué mejoramos
```

## Cuándo actuar sin preguntar

- Guardar aprendizajes en Engram → **siempre, sin preguntar**
- Consolidar entradas de Engram → **siempre, sin preguntar**
- Actualizar AGENTS.md / README → **siempre, sin preguntar**
- Reportar inconsistencias YAML/persona → **siempre, sin preguntar**

## Cuándo preguntar antes

- Crear una nueva skill → **preguntar primero** ("¿Creo una skill para X?")
- Crear un nuevo agente → **preguntar primero**
- Cambiar arquitectura → **preguntar primero**

## Métricas que追踪

| Métrica | Cómo medirla |
|---------|-------------|
| Bugs recurrentes | mem_search mismo tipo de bug 3+ veces |
| Tiempo perdido | Commits de "fix" o "revert" frecuentes |
| Skills no usadas | Skills en AGENTS.md sin referencias en personas |
| Inconsistencias | YAML skills vs persona Arsenal vs AGENTS.md skills table |
| Documentación stale | ARCHITECTURE menciona agentes que ya no existen |
