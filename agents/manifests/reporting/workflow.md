# Workflow: Reporting

## Flujo principal

```
Orchestrator → [1. Definir audiencia y objetivo] → [2. Seleccionar hallazgos] → [3. Estructurar narrativa] → [4. Elegir formato] → [5. Incluir gráficos y tablas] → [6. Exportar] → Orchestrator
```

## Paso a paso

### 1. Definir audiencia y objetivo
Leer el prompt e identificar: ¿quién va a leer este reporte? ¿Técnico, ejecutivo, operativo, público general? ¿Qué decisión tiene que tomar? ¿Cuánto tiempo tiene para leerlo? Definir el mensaje central en **una sola frase**. Si no podés, necesitás clarificar antes de seguir.

### 2. Seleccionar hallazgos clave (top 3-5)
Del análisis completo, elegir los 3 a 5 hallazgos más relevantes para la audiencia definida. Priorizar: impacto en el negocio > magnitud estadística > novedad. Cada hallazgo se presenta con: **qué pasó, por qué importa, qué hacer al respecto**. Lo que no entra en el top 5 va a una sección de "otros hallazgos" o se omite.

### 3. Estructurar la narrativa — pirámide invertida

Estructura canónica del reporte:

| Sección | Propósito | Extensión |
|---|---|---|
| **Resumen ejecutivo** | Lo indispensable en 3-4 líneas. La persona ocupada lee solo esto y ya sabe. | 4-6 líneas |
| **Hallazgos principales** | Top 3-5 hallazgos con datos, interpretación y acción sugerida. | 1 párrafo c/u + gráfico/tabla |
| **Detalle y metodología** | Para quien quiera profundizar: datos completos, segmentaciones, nota metodológica. | Variables, según necesidad |
| **Recomendaciones** | Acciones concretas priorizadas. Cada recomendación tiene dueño sugerido, esfuerzo estimado e impacto esperado. | 3-5 bullets |

Regla: si una persona lee solo el resumen ejecutivo y los bullets de recomendaciones, ya debería poder actuar.

### 4. Elegir formato según audiencia y contexto

| Formato | Cuándo usarlo | Pros | Contras |
|---|---|---|---|
| **Markdown** | Iteración rápida, compartir por chat/GitHub, documentación interna | Simple, versionable, convertible | Sin control de layout, feo si no se renderiza |
| **HTML** | Reporte presentable, dashboards estáticos, email interno | Estilizable con CSS, incrusta gráficos, interactivo posible | Más pesado, no imprime perfecto |
| **PDF** | Formal, directorio, cliente externo, impresión | Layout fijo, profesional, portable | Menos interactivo, requiere conversión extra |
| **Excel** | Solo si lo piden explícitamente | Datos manipulables | Sin narrativa, fácil de malinterpretar |

### 5. Incluir gráficos y tablas
- **Gráficos**: delegar a `data-visualization` si el análisis no los incluyó. Cada gráfico responde una pregunta concreta. Con título descriptivo (no "Gráfico 1" sino "Ventas por región — Q1 creció 12% en CABA").
- **Tablas**: usar `pandas` styling con formato de moneda, porcentajes, y highlighting condicional. Máximo 10 filas en el cuerpo del reporte — el resto a sección de detalle o anexo.

### 6. Exportar y verificar
- **Markdown**: escribir a archivo `.md` con `open()`. Verificar que renderiza bien en el visor destino (GitHub, Notion, Slack).
- **HTML**: template con CSS inline, `df.to_html()`, incrustar imágenes de gráficos como base64 o referencias locales.
- **PDF**: si el HTML está listo, convertir con `weasyprint` o `pdfkit`. Alternativa: `jupyter nbconvert --to pdf`.
- **Verificación final**: ¿el resumen ejecutivo cuenta la historia? ¿Los números clave son visibles en 10 segundos? ¿Las recomendaciones son accionables? ¿El formato de salida es el correcto?

## Reglas de decisión rápida

- **¿Incluir esta métrica?** → ¿Responde una pregunta de la audiencia? Si no, fuera.
- **¿Gráfico o tabla?** → ¿Importa la magnitud exacta? Tabla. ¿Importa la tendencia, comparación o distribución? Gráfico.
- **¿Cuánto detalle?** → Suficiente para que un escéptico confíe, no tanto para abrumar a un ejecutivo.
