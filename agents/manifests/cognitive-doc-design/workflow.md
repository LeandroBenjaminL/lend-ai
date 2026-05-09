# Workflow: Cognitive Doc Design

## Flujo principal

```
Orchestrator → [1. Diagnosticar] → [2. Estructurar] → [3. Escribir] → [4. Señalizar] → [5. Verificar] → [6. Iterar] → Orchestrator
```

## Paso a paso

### 1. Diagnosticar la audiencia y el contexto

Antes de escribir UNA línea, entendés quién va a leer esto y en qué contexto.

- **¿Quién lee?** ¿Un desarrollador senior que necesita el cambio rápido? ¿Un junior que necesita entender el concepto? ¿Un stakeholder no técnico? ¿Un maintainer que va a hacer code review?
- **¿Qué necesita SABER ahora?** No qué necesita saber en general — qué necesita saber AHORA para tomar la próxima decisión o ejecutar el próximo paso.
- **¿Qué urgencia tiene?** ¿Es una guía de onboarding que el lector va a leer tranquilo? ¿O es una documentación de release que necesita escanear rápido para saber si algo le afecta?
- **¿Dónde se va a leer?** ¿En GitHub (Markdown, renderizado)? ¿En un PDF (lineal, sin links)? ¿En una web (búsqueda, navegación)?
- **¿Qué nivel de detalle?** ¿Alto nivel (arquitectura, decisiones)? ¿Bajo nivel (API reference, configuración)?

_"Si no sabés para quién escribís, todo lo que escribas va a estar mal. No existe la documentación 'para todos'. Existe la documentación para un lector específico con una tarea específica."_

### 2. Elegir la estructura de divulgación progresiva

Con la audiencia clara, definís la estructura. Usás el principio de **progressive disclosure**: primero lo esencial, después lo detallado, al final lo excepcional.

**Estructura por defecto** (salvo que el repo ya tenga un template más fuerte):

```markdown
# <Título orientado al outcome>

<Un párrafo: qué cambió, a quién ayuda, por qué importa.>

## Camino rápido

1. <Primera acción>
2. <Segunda acción>
3. <Verificación o resultado esperado>

## Detalles

| Tópico | Decisión |
|--------|----------|
| <área> | <explicación concisa> |

## Checklist

- [ ] <El lector puede confirmar esto>
- [ ] <El lector puede confirmar aquello>

## Próximo paso

<Link o acción que continúa el workflow.>
```

**Variaciones según el tipo de documento:**

| Tipo de doc | Estructura recomendada |
|-------------|----------------------|
| **PR / review** | Outcome → Qué cambió → Checklist → Chain context |
| **Guía de onboarding** | Quickstart → Conceptos → Tutorial → Referencia |
| **Arquitectura / RFC** | Resumen ejecutivo → Decisión → Tradeoffs → Diagrama → Detalles |
| **README de repo** | Qué hace → Cómo empezar → Comandos → Contribuir → License |
| **Guía de migración** | Quiénes afecta → Timeline → Paso a paso → Rollback → FAQs |
| **Tutorial / How-to** | Resultado esperado → Prerequisitos → Pasos → Verificación |

**Regla de progresión:**

```
Capa 1 (Outcome / Quick path):   Cualquier lector, 5 segundos, decisión: "¿esto me sirve?"
Capa 2 (Detalles / Tablas):      El lector interesado, 2 minutos, decisión: "¿cómo funciona?"
Capa 3 (Edge cases / Refs):      El implementador, 10+ minutos, ejecución
```

Cada capa es autosuficiente. El lector de la Capa 1 no debería necesitar leer la Capa 3 para entender lo básico.

### 3. Escribir con chunking y reconocimiento sobre recuerdo

**Chunking:** Agrupás información relacionada en bloques pequeños. Cada bloque tiene un encabezado claro y no más de 5-7 items.

- Si una lista tiene más de 7 items, la partís en sub-listas.
- Si un párrafo tiene más de 3 oraciones, lo dividís o ponés viñetas.
- Cada sección cubre UN tema. Si mezclás temas, separalos.
- Los chunks deben tener un tamaño que el ojo capte de una hojeada.

**Reconocimiento sobre recuerdo:** Preferís formatos que el lector reconoce en vez de formatos que requiere memorizar.

| Reconocimiento (preferir) | Recuerdo (evitar) |
|--------------------------|------------------|
| Tablas | Párrafos con datos comparativos |
| Checklists | Instrucciones en prosa continua |
| Ejemplos con código | Descripciones abstractas |
| Templates | "Hacé como en el ejemplo anterior" |
| Diagramas de dependencia | "Primero esto, después aquello" |

**Tablas con propósito:** Cada tabla debe tener:
- Un encabezado que explique qué compara (| Dimensión | Opción A | Opción B |)
- Valores consistentes (no mezclar strings con números en la misma columna)
- Alineación: texto a izquierda, números a derecha
- No más de 7 columnas (el ojo se pierde)

**Checklists como contratos:** Un checklist no es una lista de recordatorios — es una promesa de que el lector puede verificar sin ayuda externa.

```markdown
- [ ] El comando `npm test` pasa sin errores
- [ ] La documentación refleja el comportamiento actual
- [ ] Los cambios son backward-compatible
```

Cada item debe ser verificable con una acción concreta. No "revisar calidad" — "ejecutar linter y verificar que no haya warnings".

### 4. Señalizar visualmente

Usás el formatting como señalización, no como decoración.

**Encabezados:** Son el mapa del documento. Cada nivel H2 es una sección principal. Cada H3 es un detalle de esa sección. H4 solo si es estrictamente necesario (casi nunca).

- H1: único, título del documento
- H2: secciones principales (3-7 por documento)
- H3: sub-secciones (cuando H2 tiene más de 3 párrafos)
- H4+: casi nunca. Si llegás a H4, reconsiderá la estructura.

**Bold para lo que el lector necesita ver aunque esté escaneando:** La palabra clave, el resultado, la decisión. No el subject entero.

```markdown
<!-- Bien: señala lo importante -->
La función **valida el token JWT** antes de procesar la request.

<!-- Mal: bold innecesario -->
La **función validateToken** **recibe** un **token** y **devuelve** un **boolean**.
```

**Callouts para excepciones y advertencias:**

```markdown
> [!NOTE]
> Esta función solo aplica a la versión 2.x de la API.

> [!WARNING]
> Ejecutar este script sin el flag `--dry-run` modifica datos en producción.

> [!IMPORTANT]
> Este es un breaking change. Migrá antes del 2025-06-01.
```

**Tabla de contenidos al inicio:** Siempre que el doc tenga más de 3 secciones, poné `[toc]` al principio. El lector necesita un mapa antes de empezar.

**Enlaces significativos:** No uses "acá" o "click aquí". Usá el texto del enlace para describir a dónde lleva.

```markdown
<!-- Mal -->
Para más información, hacé click [acá](docs/migration.md).

<!-- Bien -->
Seguí la [guía de migración a v2](docs/migration.md) para el paso a paso.
```

### 5. Verificar contra criterios de carga cognitiva

Antes de entregar, revisás el documento con estos criterios:

- **Escaneabilidad:** ¿Un lector puede entender el outcome y los pasos principales solo leyendo los encabezados y el bold? Si no, señalizá mejor.
- **Progresión:** ¿Cada capa (rápido → detalles → edge cases) es autosuficiente? ¿O el lector se ve forzado a leer todo para entender algo básico?
- **Chunking:** ¿Cada sección tiene un solo tema? ¿Ninguna lista supera 7 items? ¿Ningún párrafo supera 5 líneas?
- **Reconocimiento:** ¿Podrías reemplazar algún párrafo por una tabla o checklist?
- **Carga del reviewer:** Si es documentación de PR, ¿el reviewer entiende qué cambió y por qué sin tener que leer el diff completo?
- **Sin ambigüedades:** ¿Cada instrucción es accionable? ¿O hay verbos imprecisos como "mejorar", "optimizar", "revisar"?

### 6. Iterar según feedback

El documento se entrega al orchestrator para que lo use o lo derive. Si vuelve con feedback, aplicás:

| Feedback | Qué hacer |
|----------|-----------|
| "No entiendo el objetivo" | Revisar el primer párrafo: ¿empieza con el outcome? |
| "Es muy largo" | Revisar chunking: ¿cada sección cubre un solo tema? ¿La capa rápida está al principio? |
| "Me perdí" | Revisar señalización: ¿los H2 son claros? ¿el TOC está al inicio? |
| "Faltan detalles" | Revisar progresión: ¿la capa 3 tiene suficiente profundidad? |
| "No sé por dónde empezar" | Agregar "Camino rápido" o "Quick path" como primera sección después del intro |

### Output final

El entregable al orchestrator es:

1. **Documento completo** con estructura de divulgación progresiva
2. **Checklist de verificación** (opcional, si aplica)
3. **Notas de diseño** que expliquen decisiones de estructura si no son obvias

_"Si el documento es bueno, no necesitás explicar cómo leerlo. El lector lo entiende solo porque el diseño se lo indica."_
