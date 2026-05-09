---
name: skill-creator
description: >
  Crea nuevas skills para agentes siguiendo el estándar Agent Skills.
  Trigger: Cuando querés crear una skill nueva, agregar instrucciones
  para la IA, o documentar patrones.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.1"
  model_tier: T3-balanced
  allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Skill: skill-creator

Crear skills que los agentes puedan entender y aplicar sin ambigüedad.

## Trigger

- Un patrón se repite y el agente necesita guía para no equivocarse.
- El proyecto tiene convenciones propias que difieren de las prácticas genéricas.
- Un workflow complejo necesita pasos detallados.
- Un árbol de decisión ayuda al agente a elegir el approach correcto.

**No crees una skill cuando**: ya existe documentación (creá un reference mejor),
el patrón es trivial o autoevidente, o es una tarea de una sola vez.

## Por qué existe

Los agentes sin skills escriben código genérico. Con skills, escriben código
que respeta las convenciones del proyecto, los patrones del equipo y las
decisiones de arquitectura. Una skill bien escrita ahorra horas de correcciones.

## Workflow

```
1. Verificá que no exista ya (buscá en skills/ y en AGENTS.md)
2. Elegí un nombre corto con guiones ({tecnologia}, {proyecto}-{componente})
3. Creá la carpeta: skills/{skill-name}/
4. Escribí SKILL.md con el template de abajo
5. Si necesitás templates o schemas, ponelos en assets/
6. Si necesitás referenciar docs existentes, poné links en references/
7. Registrala en AGENTS.md
```

## Estructura de carpetas

```
skills/{skill-name}/
├── SKILL.md              # Obligatorio
├── assets/               # Opcional: templates, schemas, ejemplos
└── references/           # Opcional: links a docs locales (NO web URLs)
```

## Template de SKILL.md

```markdown
---
name: {skill-name}
description: >
  {Una línea: qué hace esta skill}.
  Trigger: {Cuándo cargarla}.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

# Skill: {skill-name}

{Descripción corta: para qué sirve, qué problema resuelve.}

## Trigger

{Casos concretos: cuándo cargar esta skill.}

## Por qué existe

{Breve explicación de por qué este enfoque, no solo el qué.}

## Workflow

{Pasos detallados para implementar lo que la skill enseña.}

## Patrones

{Lo que el agente DEBE hacer siempre.}

## Anti-patrones

{Lo que el agente NO DEBE hacer nunca.}
```

## Patrones

- **Arrancá con los patrones críticos**: el agente necesita saber primero lo
  que no puede violar.
- **Tablas para decisiones**: si hay opciones, tabla. Si hay pasos, checklist.
- **Ejemplos mínimos**: 2-3 líneas que ilustren el punto. Nada de 50 líneas de código.
- **Menos es más**: 80-150 líneas total. Si necesitás más, la skill es muy amplia.
- **Frontmatter completo**: `name`, `description` (con trigger), `license`,
  `metadata.author`, `metadata.version`.

## Anti-patrones

- Skills de 300+ líneas que nadie va a leer — partilas en skills más chicas.
- Repetir información que ya está en la documentación del proyecto — referenciá, no dupliques.
- Secciones de Keywords o Troubleshooting — el agente busca por frontmatter y patrones.
- URLs web en references/ — usá paths locales.
- Instrucciones contradictorias entre skills — si pasa, unificá.
