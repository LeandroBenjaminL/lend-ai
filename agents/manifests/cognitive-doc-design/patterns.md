# Patterns: Documentación de Baja Carga Cognitiva

> _La documentación no se lee. Se escanea. Si tu documento no se puede escanear, no existe para el lector._

## Tabla de decisión: estructura según tipo de documento

| Tipo de doc | Audiencia | Estructura recomendada | Énfasis |
|-------------|-----------|----------------------|---------|
| **PR description** | Reviewer técnico | Outcome → Changes → Checklist → Chain context | Escaneabilidad, acción |
| **README** | Usuario nuevo | Qué hace → Quickstart → Comandos → Contribuir | Onboarding rápido |
| **Guía de onboarding** | Junior / nuevo en el equipo | Quickstart → Conceptos → Tutorial → Referencia | Progresión gradual |
| **RFC / Architecture** | Equipo técnico | Resumen ejecutivo → Decisión → Tradeoffs → Diagrama | Justificación de decisiones |
| **Guía de migración** | Usuarios afectados | Quiénes afecta → Timeline → Paso a paso → Rollback | Acción clara |
| **API reference** | Desarrollador integrando | Endpoint → Request → Response → Errores | Precisión técnica |
| **How-to / Tutorial** | Usuario con tarea específica | Resultado esperado → Prerequisitos → Pasos → Verificación | Resultado medible |
| **Release notes** | Todos los usuarios | Breaking → Features → Fixes → Deprecations | Cambios relevantes |

## Tabla de técnicas de reducción de carga cognitiva

| Técnica | Qué hace | Cómo se aplica | Impacto |
|---------|----------|----------------|---------|
| **Progressive disclosure** | Muestra info en capas según necesidad | Outcome primero, detalles después, edge cases al final | Alto |
| **Chunking** | Agrupa info relacionada en bloques de 3-7 items | Una sección = un tema. Listas de max 7 items | Alto |
| **Signposting** | Señaliza visualmente para que el lector se oriente | H1/H2/H3 claros, bold estratégico, callouts | Alto |
| **Recognition over recall** | Muestra info en vez de requerir memorizarla | Tablas, checklists, ejemplos, templates | Alto |
| **Inverted pyramid** | Lo más importante primero | Primer párrafo = outcome. Después contexto. | Medio |
| **Consistent formatting** | Mismos elementos = mismo significado visual | Mismo estilo para warnings, tips, ejemplos, código | Medio |
| **Short paragraphs** | Reduce densidad visual | Máximo 3-4 oraciones por párrafo | Medio |
| **Bullet over prose** | Facilita escaneo | Items en lista vs párrafo continuo | Medio |

## Anti-patrones de documentación

| Anti-patrón | Qué es | En qué se convierte | Cómo fixear |
|-------------|--------|-------------------|-------------|
| **Wall of text** | Párrafos de 10+ líneas sin breaks | El lector saltea el 90% | Partir en párrafos cortos, agregar H2/H3 |
| **Context-first** | "Antes de entender la solución, tenés que saber..." | El lector se pierde antes de llegar al punto | Empezar con el outcome, contexto después |
| **Ambiguous verbs** | "Mejorar", "optimizar", "revisar" | Nadie sabe qué acción tomar | "Ejecutar X", "Verificar que Y", "Correr Z" |
| **Hidden requirements** | Prerequisitos enterrados en el medio del texto | El lector llega al paso 5 y descubre que necesita algo que no tiene | Checklist de prerequisitos al principio |
| **Trademark voice** | "En caso de que se presentara la eventualidad de..." | Suena a robot, nadie confía | "Si pasa X, hace Y" |
| **Info dumping** | Todo junto, sin jerarquía | El lector no sabe qué es importante | Progressive disclosure: capa 1, 2, 3 |
| **Missing TOC** | Documento largo sin índice | El lector no sabe qué hay ni dónde está | Agregar `[toc]` al inicio |
| **Dead links** | Referencias a URLs que ya no existen | El lector confía y después se frustra | Verificar links antes de publicar |
| **Assumed context** | "Como sabemos..." (y el lector no sabe) | El lector se siente excluido | Explicar el contexto o linkear a la fuente |
| **Gratuitous bold** | Bold en TODO | Nada es importante porque todo lo es | Bold SOLO en keywords, decisiones, resultados |

## Checklist de verificación pre-entrega

- [ ] **Escanibilidad:** ¿El primer párrafo dice lo que NECESITÁS saber? (no lo que "está bueno saber")
- [ ] **Progresión:** ¿Cada capa es autosuficiente? (no necesitás leer capa 3 para entender capa 1)
- [ ] **Chunking:** ¿Cada sección cubre UN tema? ¿Ninguna lista supera 7 items?
- [ ] **Reconocimiento:** ¿Podrías reemplazar algún párrafo por una tabla o checklist?
- [ ] **TOC:** Si el documento tiene más de 3 secciones, ¿tiene tabla de contenidos?
- [ ] **Callouts:** ¿Los warnings están señalizados con `[!WARNING]` o `[!NOTE]`?
- [ ] **Bold:** ¿El bold está en las palabras clave, no en frases enteras?
- [ ] **Enlaces:** ¿Los enlaces son descriptivos ("guía de migración a v2") en vez de genéricos ("acá")?
- [ ] **Consistencia:** ¿Mismo tipo de contenido usa mismo formato visual en todo el documento?
- [ ] **Verificabilidad:** ¿Cada item de checklist o instrucción es verificable con una acción concreta?
- [ ] **Sin jerga interna:** ¿Alguien nuevo en el proyecto entiende los términos?
- [ ] **Longitud:** ¿El documento es lo más corto posible sin perder información necesaria?

## Tabla de decisiones de formato

| Situación | Formato | Ejemplo |
|-----------|---------|---------|
| Comparar opciones | Tabla | `\| Feature \| Opción A \| Opción B \|` |
| Lista de acciones | Checklist | `- [ ] Ejecutar comando X` |
| Lista simple | Bullets | `- Item 1` |
| Pasos secuenciales | Lista numerada | `1. Hacer X` |
| Código | Code block con lenguaje | ` ```python ` |
| Advertencia | Callout | `> [!WARNING]` |
| Nota informativa | Callout | `> [!NOTE]` |
| Información importante | Callout | `> [!IMPORTANT]` |
| Resultado concreto | Bold | **El output es un archivo JSON en `/tmp/`** |
| Concepto nuevo | Link + definición breve | "Un [middleware](../../docs/auth/middleware.md) intercepta requests antes de llegar al handler" |

## Principios fundamentales

1. **La documentación no existe para el autor.** Existe para el lector. Si el lector no entiende, la culpa es del documento.
2. **Un buen documento se puede escanear en 10 segundos y entender lo básico.** Si requiere lectura lineal completa, está mal estructurado.
3. **El formato ES contenido.** Una tabla no es "linda" — es más fácil de procesar que un párrafo. Un checklist no es "pedante" — es más verificable que una lista de bullets.
4. **La brevedad no es faltar información.** Es no incluir información que el lector no necesita AHORA.
5. **El peor documento es el que el lector abre, no entiende, y cierra.** Eso es tiempo perdido para todos.

> _La carga cognitiva no se "reduce". Se DISEÑA. Cada bold, cada salto de línea, cada tabla, cada callout es una decisión de diseño que acerca o aleja al lector de su objetivo._
