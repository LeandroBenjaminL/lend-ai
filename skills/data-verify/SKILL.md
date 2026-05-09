---
name: data-verify
description: >
  Verificar que los resultados del análisis sean correctos, consistentes y respondan la pregunta original.
  Trigger: Cuando el análisis está terminado y necesitás revisarlo antes de presentarlo.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "2.0"
  model_tier: T2-fast
---

# Skill: data-verify

Verificar no es lo mismo que validar. **Validación** es chequeo de calidad de los datos de entrada. **Verificación** es asegurarte de que el análisis que hiciste tiene sentido, responde la pregunta original y no tiene errores lógicos. Es el paso que separa un análisis sólido de uno que parece correcto pero no lo es.

## Trigger

- Terminaste un análisis y vas a presentarlo — no saltees este paso
- Los resultados se ven "demasiado buenos" para ser verdad (probablemente hay un bug)
- Te están por pedir conclusiones y necesitás estar seguro
- Antes de archivar o commitear un proyecto

## Workflow de verificación

### 1. Revisión lógica — el análisis cuenta una historia coherente
Sentate y leé los resultados como si fueran de otra persona. Preguntate: ¿las conclusiones se desprenden naturalmente de los datos, o las estás forzando?

### 2. Revisión técnica — chequeo de bugs comunes
Repetí los cálculos clave de forma independiente. Si calculaste un promedio, verificalo con una cuenta rápida aparte. Si filtraste datos, asegurate de que el filtro no eliminó lo que no debía.

### 3. Revisión de supuestos — los tests estadísticos vinieron con condiciones
Si hiciste un test t, checkeá normalidad. Si hiciste regresión lineal, checkeá homocedasticidad. Cada método estadístico tiene supuestos que si no se cumplen, invalidan tus conclusiones.

### 4. Revisión de visualizaciones — los ejes no mienten
Asegurate de que los ejes Y no arranquen en un valor que exagere diferencias, que las escalas sean consistentes y que los colores no confundan.

## Patrones y ejemplos

### Checkeos automáticos de consistencia

```python
def verificar_analisis(df_original, df_resultado):
    """Corre checkeos básicos de consistencia"""
    problemas = []

    # 1. Check de integridad: no perdimos filas de más
    if len(df_resultado) > len(df_original):
        problemas.append("⚠️ El resultado tiene MÁS filas que el original — revisá joins duplicados")

    # 2. Rangos razonables
    for col in df_resultado.select_dtypes('number').columns:
        if df_resultado[col].max() > df_original[col].max() * 10:
            problemas.append(f"⚠️ {col}: valor máximo inusualmente alto ({df_resultado[col].max():,.0f})")

    # 3. Nulos inesperados
    nulos_nuevos = df_resultado.isna().sum() - df_original.isna().sum()
    cols_con_nulos = nulos_nuevos[nulos_nuevos > 0].index.tolist()
    if cols_con_nulos:
        problemas.append(f"⚠️ Columnas con nulos nuevos post-análisis: {cols_con_nulos}")

    return problemas
```

### Checklist de verificación (para pegar en cada proyecto)

```markdown
- [ ] **¿Los resultados responden la pregunta original?** — si responden otra cosa, el análisis está fuera de foco
- [ ] **¿Las conclusiones están sustentadas por los datos?** — o son suposiciones disfrazadas de hallazgos
- [ ] **¿Se consideraron variables de confusión?** — ej: correlación no implica causalidad
- [ ] **¿Los supuestos estadísticos se cumplen?** — normalidad, homocedasticidad, independencia
- [ ] **¿Hay errores de datos?** — outliers no tratados, nulos ignorados, joins mal hechos
- [ ] **¿El código es reproducible?** — si lo corro de nuevo, da el mismo resultado
- [ ] **¿Las visualizaciones son claras?** — ejes etiquetados, escalas honestas, colores accesibles
```

## Alternativas

| Enfoque | Cuándo usarlo |
|---------|---------------|
| **Peer review** | Pedile a un colega que revise — atrapa errores que vos no ves |
| **Test unitarios** | Para pipelines que se ejecutan seguido; escribí tests como en software |
| **Reproducción ciega** | Rehacé el análisis sin mirar el código original — si da distinto, algo está mal |
| **Validación cruzada** | Partí los datos en K folds y verificá que los resultados sean estables |

**Recomendación**: para análisis exploratorios alcanza con peer review + checklist. Para ML o pipelines productivos, necesitás tests automatizados.

## Anti-patrones

- ❌ **Confíar en el resultado porque "se ve bien"** — los errores más peligrosos son los que se ven razonables
- ❌ **Verificar solo los números que apoyan tu hipótesis** — eso es sesgo de confirmación
- ❌ **No documentar los pasos** — si no podés reproducir el análisis, no podés verificar los resultados
- ❌ **Saltear la verificación cuando tenés poco tiempo** — es exactamente cuando más errores hay
