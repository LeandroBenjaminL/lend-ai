# Patterns: Cheat Sheet de Verificación de Análisis

## 1. Sanity Check Checklist — Automatizable

Cada vez que recibís un análisis para verificar, corré este checklist mental (o en código) antes de mirar cualquier otra cosa:

```python
def sanity_check_rapido(df, metricas: dict):
    """Checks que todo análisis debería pasar antes de presentarse.

    Args:
        df: DataFrame con los datos usados en el análisis
        metricas: dict con métricas clave del análisis {'nombre': valor}
    """
    warnings = []

    # === Checks numéricos básicos ===
    # Nulos inesperados
    for col in df.columns:
        if df[col].isnull().mean() > 0.5:
            warnings.append(f"⚠️  {col}: {df[col].isnull().mean():.1%} nulos — ¿se trataron?")

    # Valores imposibles
    for col in df.select_dtypes(include='number').columns:
        if col.lower().startswith(('prob', 'pct', 'rate', 'ratio', 'tasa')):
            if df[col].max() > 1.0 and df[col].max() < 100:
                warnings.append(f"⚠️  {col}: rango [{df[col].min():.4f}, {df[col].max():.4f}] — ¿son proporciones o porcentajes?")
        if df[col].min() < 0 and 'count' not in col.lower() and 'delta' not in col.lower():
            warnings.append(f"⚠️  {col}: valores negativos encontrados — ¿tienen sentido?")

    # Consistencia de agregaciones
    if 'total' in metricas and 'segmentos' in metricas:
        suma_segmentos = sum(metricas['segmentos'].values())
        if abs(suma_segmentos - metricas['total']) / metricas['total'] > 0.01:
            warnings.append(f"❌ Segmentos suman {suma_segmentos:.2f} pero total es {metricas['total']:.2f}")

    # Duplicados
    dups = df.duplicated().sum()
    if dups > 0:
        warnings.append(f"🔁 {dups} filas duplicadas ({dups/len(df):.1%}) — ¿se deduplicó?")

    return warnings
```

---

## 2. Verificación de Supuestos Estadísticos

Cada test estadístico tiene supuestos. Verificá los del análisis que estás revisando:

| Test | Supuestos | Cómo verificar |
|---|---|---|
| t-test | Normalidad, homocedasticidad, independencia | Shapiro-Wilk, Levene, diseño experimental |
| ANOVA | Normalidad, homocedasticidad, independencia | Shapiro-Wilk por grupo, Levene/Bartlett |
| Chi-cuadrado | Frecuencias esperadas ≥ 5, independencia | Tabla de contingencia con expected |
| Regresión lineal | Linealidad, independencia, homocedasticidad, normalidad de residuos, no multicolinealidad | Residual plots, VIF, Durbin-Watson |
| Regresión logística | Linealidad del logit, no multicolinealidad, independencia | Box-Tidwell test, VIF |

```python
from scipy import stats
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm

def verificar_supuestos_regresion(X, y, modelo):
    """Check de supuestos para regresión lineal."""
    resultados = {}
    residuos = modelo.resid
    fitted = modelo.fittedvalues

    # Normalidad de residuos (Shapiro-Wilk)
    stat, p = stats.shapiro(residuos)
    resultados['normalidad_residuos'] = {'p_value': p, 'ok': p > 0.05}

    # Homocedasticidad (Breusch-Pagan)
    bp_test = het_breuschpagan(residuos, X)
    resultados['homocedasticidad'] = {'p_value': bp_test[1], 'ok': bp_test[1] > 0.05}

    # Multicolinealidad (VIF)
    vif_data = pd.DataFrame({'feature': X.columns, 'VIF': [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]})
    alto_vif = vif_data[vif_data['VIF'] > 10]
    resultados['multicolinealidad'] = {'vif_alto': len(alto_vif) > 0, 'detalle': alto_vif.to_dict() if len(alto_vif) > 0 else 'OK'}

    # Independencia (Durbin-Watson) — solo válido si datos ordenados temporalmente
    dw = sm.stats.durbin_watson(residuos)
    resultados['independencia_dw'] = {'dw': dw, 'ok': 1.5 < dw < 2.5}

    return resultados
```

---

## 3. Validación Cruzada de Métricas

Nunca confíes en una sola forma de calcular una métrica. Verificá por dos caminos distintos:

```python
def validacion_cruzada_metricas(df):
    """Compará métricas calculadas de formas distintas."""

    checks = []

    # Ejemplo: ingresos totales = sum(precio * cantidad) = sum(ingreso_por_fila)
    if all(c in df.columns for c in ['precio', 'cantidad', 'ingreso']):
        metodo1 = (df['precio'] * df['cantidad']).sum()
        metodo2 = df['ingreso'].sum()
        diff_pct = abs(metodo1 - metodo2) / max(metodo1, metodo2) * 100
        if diff_pct > 1:
            checks.append(f"❌ Ingreso: método1={metodo1:.2f}, método2={metodo2:.2f}, diff={diff_pct:.1f}%")

    # Ejemplo: media general = promedio de medias por grupo (solo si tamaños iguales)
    if 'grupo' in df.columns and 'metrica' in df.columns:
        media_general = df['metrica'].mean()
        media_por_grupo = df.groupby('grupo')['metrica'].mean().mean()
        # No deberían ser iguales si los grupos tienen distinto tamaño, pero verificamos
        checks.append(f"📊 Media general: {media_general:.4f} | Media de medias: {media_por_grupo:.4f}")

    # Ejemplo: suma de proporciones dentro de cada grupo = 1
    if 'grupo' in df.columns and 'categoria' in df.columns:
        props = df.groupby('grupo').size() / len(df)
        if abs(props.sum() - 1.0) > 0.01:
            checks.append(f"❌ Proporciones de grupos no suman 1: {props.sum():.4f}")

    return checks
```

---

## 4. Contra-Ejemplos

Para cada conclusión, buscá activamente ejemplos que la contradigan:

```python
def buscar_contraejemplos(df, conclusion, condicion, metrica, grupo_control=None):
    """Buscá casos donde la conclusión no se cumple.

    Args:
        conclusion: string describiendo la conclusión (ej: "Grupo A > Grupo B")
        condicion: expresión booleana que define la conclusión
        metrica: columna con la métrica a comparar
        grupo_control: segmento donde testear (None = todo el dataset)
    """
    data = df if grupo_control is None else df.query(grupo_control)
    contraejemplos = data[~condicion]

    if len(contraejemplos) > 0:
        pct = len(contraejemplos) / len(data) * 100
        return {
            'conclusion': conclusion,
            'contraejemplos': len(contraejemplos),
            'pct': pct,
            'severidad': 'crítico' if pct > 20 else 'moderado' if pct > 5 else 'menor',
            'ejemplo': contraejemplos.head(3).to_dict()
        }
    return None
```

---

## 5. Detección de Paradoja de Simpson

La paradoja de Simpson ocurre cuando una tendencia que aparece en varios grupos desaparece o se invierte al combinarlos. Es uno de los errores más comunes y peligrosos en análisis de datos.

```python
def detectar_simpson(df, grupo, metrica, variable_agrupadora):
    """Detectá posible paradoja de Simpson.

    Args:
        grupo: columna que define los grupos a comparar (ej: 'tratamiento')
        metrica: métrica de resultado (ej: 'conversion')
        variable_agrupadora: columna que podría ocultar la paradoja (ej: 'plataforma', 'pais')
    """
    # Tendencia global
    global_agg = df.groupby(grupo)[metrica].mean()
    tendencia_global = 'A > B' if global_agg.iloc[0] > global_agg.iloc[1] else 'B > A'

    # Tendencia dentro de cada nivel de la variable agrupadora
    inversiones = 0
    total_niveles = 0
    for nivel, subset in df.groupby(variable_agrupadora):
        if subset[grupo].nunique() < 2:
            continue
        total_niveles += 1
        agg = subset.groupby(grupo)[metrica].mean()
        tendencia_local = 'A > B' if agg.iloc[0] > agg.iloc[1] else 'B > A'
        if tendencia_local != tendencia_global:
            inversiones += 1

    if inversiones > 0:
        return {
            'paradoja_detectada': True,
            'tendencia_global': tendencia_global,
            'niveles_con_inversion': inversiones,
            'total_niveles': total_niveles,
            'severidad': 'crítico' if inversiones == total_niveles else 'posible' if inversiones > total_niveles/2 else 'leve'
        }

    return {'paradoja_detectada': False}
```

---

## 6. Reglas de Oro para Verificar Análisis

Estas 10 reglas destilan años de errores encontrados. Memorizalas:

1. **Nunca confíes en promedios sin ver la distribución.** Dos distribuciones completamente distintas pueden tener la misma media. Siempre pedí histogramas, boxplots, y percentiles.

2. **Ratio de dos métricas ruidosas = ruido al cuadrado.** Si dividís dos métricas con alta varianza, el cociente amplifica el ruido. Verificá con intervalos de confianza, no con puntuales.

3. **Si no tiene intervalo de confianza, no es una conclusión, es una anécdota.** Toda afirmación sobre diferencia o cambio debe venir con su IC o p-value. "Subió 5%" sin IC es wishful thinking.

4. **Correlación sin scatter plot es propaganda.** La correlación de Pearson es engañosa sin ver la nube de puntos. Buscá relaciones no lineales, outliers que la inflan artificialmente, y clusters ocultos.

5. **El tamaño de efecto importa más que el p-value.** Un p < 0.001 con Cohen's d de 0.05 es estadísticamente significativo pero prácticamente irrelevante. Preguntá: ¿este efecto es lo suficientemente grande para que al negocio le importe?

6. **Siempre testeá contra un baseline naïve.** Si tu modelo sofisticado tiene 85% de accuracy y un `df['target'].mode()` te da 83%, tu modelo no está aportando casi nada.

7. **Sobremuestreo es peligroso si no se hace bien.** SMOTE y variantes aplicados ANTES del split train/test generan data leakage. El split va primero, el resampling después.

8. **Si los resultados cambian drásticamente al cambiar una semilla, el modelo es inestable.** Corré el análisis con 5 seeds distintas. Si las conclusiones cambian, el método no es robusto.

9. **Toda segmentación es una hipótesis, no un hallazgo.** Si segmentás por la misma métrica que estás analizando, vas a encontrar diferencias por definición. La segmentación debe basarse en variables independientes del outcome.

10. **El mejor sanity check: ¿se lo explicarías a alguien que no es técnico y te creería?** Si necesitás 10 minutos de justificaciones estadísticas para defender una conclusión, probablemente la conclusión no es tan sólida como parece.

---

## 7. Template de Reporte de Verificación

```markdown
# Reporte de Verificación: [Nombre del Análisis]

**Fecha:** [fecha]
**Auditor:** data-verify
**Pregunta original:** "[transcribir textual]"

---

## Veredicto Global

[✅ Sólido / ⚠️ Aceptable con caveats / ❌ Requiere revisión]

[2-4 líneas justificando el veredicto]

---

## Hallazgos Críticos

### H1: [Título descriptivo]
- **Qué:** [descripción concreta del problema]
- **Impacto:** [cómo afecta las conclusiones]
- **Evidencia:** [números, contra-ejemplos, test estadístico]
- **Recomendación:** [acción concreta para corregir]

---

## Warnings

### W1: [Título descriptivo]
- **Qué:** [descripción]
- **Riesgo:** [qué podría salir mal si no se corrige]
- **Sugerencia:** [cómo resolverlo]

---

## Lo Que Está Bien

- [Checkpoint positivo 1]
- [Checkpoint positivo 2]

---

## Recomendaciones Priorizadas

1. [Acción urgente — necesario antes de presentar]
2. [Acción importante — mejora solidez]
3. [Acción deseable — documentación o mejora futura]
```
