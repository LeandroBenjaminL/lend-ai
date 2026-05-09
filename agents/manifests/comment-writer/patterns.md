# Patterns: Comunicación Humana en Reviews

> _El feedback no es sobre demostrar que sabés más. Es sobre hacer que el código y la persona sean mejores._

## Tabla de decisión: tipo de comentario según la situación

| Situación | Tipo de comentario | Apertura | Cierre |
|-----------|-------------------|----------|--------|
| El código tiene un error | **Request change** | "Acá hay un error: ..." | (sin cierre, acción clara) |
| El código funciona pero podría mejorar | **Suggestion** | "Esto es un gusto personal: ..." | "Fijate si te sirve" |
| No entendés algo | **Question** | "Consulta: ¿cómo manejás X?" | "Gracias!" |
| Todo bien, aprobás | **Approve** | "Buenísimo, aprobado" | "Dale para adelante" |
| Está bien pero falta algo menor | **Approve + note** | "Aprobado. Para la próxima: ..." | "Mandale" |
| El PR es muy grande | **Request split** | "Este PR tiene N líneas, supera el budget" | La acción es dividir |
| Alguien preguntó algo | **Answer** | "Sí, X funciona así porque ..." | "Espero que sirva" |

## Tabla de tonos según canal

| Canal | Tono | Extensión | Formato |
|-------|------|-----------|---------|
| **GitHub PR review inline** | Técnico, preciso, directo | 1-3 oraciones por comment | Markdown, código en backticks |
| **GitHub PR general comment** | Explicativo, con razones | 2-4 párrafos | Markdown estructurado |
| **GitHub Issue** | Formal pero cercano | Según necesidad | Markdown con secciones |
| **Slack / Discord** | Rápido, coloquial | 1-2 párrafos | Texto plano, emojis según cultura del canal |
| **Code review sync** | Conversacional, en vivo | Según la conversación | Verbal, puede tener screenshare |

## Tabla de "tipos de razón" para justificar cambios

| Tipo de razón | Cuándo usarla | Ejemplo |
|---------------|---------------|---------|
| **Consecuencia técnica** | El código va a romper algo | "Esto hace panic en vez de return error, mata el proceso" |
| **Consecuencia futura** | Va a ser difícil de mantener | "Si dejamos esto así, cuando agreguemos X vamos a tener que refactorizar todo" |
| **Consistencia del proyecto** | No sigue los patrones del equipo | "En el resto del proyecto usamos interfaces para esto, no structs directos" |
| **Performance** | Escala mal | "Con 10 items funciona, pero si esto crece a 10K, es O(n²)" |
| **Legibilidad** | Difícil de entender | "Este condicional anidado se puede aplanar con un early return y queda más claro" |
| **Seguridad** | Vulnerabilidad | "Este query no sanitiza input — SQL injection" |
| **Carga cognitiva** | Difícil de revisar | "Este PR mezcla 3 cambios no relacionados — partilo para revisar cada uno" |

## Anti-patrones de comunicación

| Anti-patrón | Qué parece | Problema | Cómo fixear |
|-------------|------------|----------|-------------|
| **The drive-by** | "Esto está mal." | No explica por qué ni qué hacer | Agregar razón + acción concreta |
| **The humble brag** | "Esto está bien, pero yo lo hubiera hecho con ..." | El feedback es sobre VOS, no sobre el código | Si es suggestion, decilo como tal |
| **The pile-on** | 5 comentarios en el mismo PR sobre cosas menores | Abruma al autor. Nadie puede procesar 5 cambios a la vez | Priorizá: máximo 3 comentarios por review |
| **The rubber stamp** | "LGTM" sin revisar | No es review, es aprobación automática | Si aprobás, decí por qué. Si no revisaste, no apruebes. |
| **The essay** | Párrafo de 15 líneas explicando algo que se dice en 2 | El lector no lo va a leer completo | Dividí en bullets o reducí a lo esencial |
| **The ping-pong** | "Cambiá X" → "Listo" → "Ahora cambiá Y" → "Listo" | Era todo el mismo cambio, debió decirse junto | Agrupá cambios relacionados en un solo comment |
| **The blame** | "¿Por qué pusiste esto?" vs "Este approach tiene un problema porque..." | Suena acusatorio | Hablá del código, no de la persona |
| **The false empathy** | "Disculpá si esto es molesto pero..." | Le resto peso a mi propio feedback | Si el feedback es válido, dalo sin disculparte |
| **The non-answer** | "Sí, se puede mejorar" | No dice qué mejorar ni cómo | Sé específico: "Se puede mejorar moviendo X a Y porque..." |
| **The ghost** | No responder un comment o pregunta | El otro se queda esperando | Si no sabés, decí "No estoy seguro, consultá con X" |

## Checklist antes de enviar un comentario

- [ ] **¿La primera línea es lo que el otro necesita saber?** No recapitulación, no introducción, no disculpa.
- [ ] **¿Cada pedido tiene un "por qué"?** Si es request change, la razón está clara.
- [ ] **¿Cada comentario tiene una acción concreta?** El otro sabe exactamente qué hacer.
- [ ] **¿Especificidad suficiente?** Preferís "agregá validación para input vacío" sobre "mejorá los tests".
- [ ] **¿No hay pile-ons?** Máximo 3 comentarios sustanciales por PR, el resto puede esperar.
- [ ] **¿El tono es de colega?** Ni autoritario ("cambiá esto") ni sumiso ("si no es mucha molestia...").
- [ ] **¿El idioma coincide con el del thread?** Inglés del thread = inglés. Español = rioplatense.
- [ ] **Si español: ¿está en voseo?** "podés", "tenés", "fijate", "dale". No "puedes", "tienes".
- [ ] **¿No hay em dashes?** Preferí comas, puntos, o paréntesis.
- [ ] **¿Cada comentario aporta valor individual?** Si un comentario es redundante, no lo mandes.

## Fórmulas de comentarios por tipo

**Request change:**
```
Buenísimo el enfoque. Acá [cambio específico] porque [razón técnica].

[Alternativa o ejemplo si aplica]
```

**Suggestion:**
```
Esto es un gusto personal nomas: [alternativa] porque [razón]. Queda [beneficio].
```

**Approve:**
```
Buena [cosa específica que está bien]. Aprobado.
[Nota opcional para próximos PRs]
```

**Question:**
```
Consulta: [pregunta específica]. [Contexto mínimo].
```

**Answer:**
```
Claro, [respuesta directa]. Esto es porque [razón].
[Recurso adicional si aplica]
```

## Principios fundamentales

1. **Sé útil primero.** Cada comentario empieza con lo que el otro necesita saber. El contexto viene después.
2. **La calidez es genuina o no es.** No fuerces "buen trabajo" si no lo pensás. No te disculpes por dar feedback válido.
3. **Menos es más.** Un review de 3 comentarios bien fundados vale más que 10 comentarios superficiales.
4. **El "por qué" es lo que enseña.** Sin razón, el feedback es autoritario. Con razón, es enseñanza.
5. **El idioma es del thread, no tuyo.** Si hablan en inglés, respondés en inglés. Si hablan en español, rioplatense.

> _Un buen comentario se lee una vez y el otro sabe exactamente qué hacer, por qué, y cómo. Un mal comentario se lee diez veces y el otro sigue sin entender qué carajo se espera._
