---
name: statistical-testing
description: >
  Tests estadísticos con SciPy y Statsmodels: t-test, chi-cuadrado, ANOVA, correlaciones y más.
  Trigger: Cuando necesitás hacer tests de hipótesis, validar significancia estadística, o comparar grupos.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "1.1"
  model_tier: T3-balanced
---

# Skill: statistical-testing

Tests de hipótesis y estadística inferencial. Para responder preguntas como "¿esta diferencia es real o es ruido?"

## Trigger

Cargá esta skill cuando:
- Necesitás comparar grupos: ¿hay diferencia significativa entre A y B?
- Querés validar hipótesis sobre tus datos
- Buscás p-values, intervalos de confianza o tamaños del efecto
- Hacés análisis de correlación entre variables

## Por qué el test correcto importa

Usar el test equivocado es la forma más fácil de llegar a conclusiones erróneas con alta confianza estadística. Un t-test en datos no normales te da p-values incorrectos. Un chi-cuadrado en variables continuas no tiene sentido. Elegir bien no es opcional.

## Tabla de tests según objetivo

| Objetivo | Test | Función SciPy | Supuestos clave |
|----------|------|---------------|-----------------|
| Comparar 2 grupos independientes | t-test Student | `ttest_ind(a, b)` | Normalidad + varianzas iguales |
| Comparar 2 grupos apareados | t-test pareado | `ttest_rel(a, b)` | Diferencias normales |
| Comparar 3+ grupos | ANOVA one-way | `f_oneway(a, b, c)` | Normalidad + homogeneidad |
| Asociación entre categóricas | Chi-cuadrado | `chi2_contingency(tabla)` | Frecuencias esperadas > 5 |
| Correlación lineal | Pearson | `pearsonr(x, y)` | Relación lineal, normalidad |
| Correlación ordinal | Spearman | `spearmanr(x, y)` | Monotonicidad (no supone normalidad) |
| Alternativa no paramétrica (2 grupos) | Mann-Whitney U | `mannwhitneyu(a, b)` | No supone distribución |

## Flujo estándar

```python
from scipy import stats

# 1. Verificar supuestos primero
stat, p_normal = stats.shapiro(grupo)       # Normalidad
stat, p_var = stats.levene(grupo_a, grupo_b)  # Homogeneidad varianzas

# 2. Elegir test según supuestos
if p_normal > 0.05 and p_var > 0.05:
    stat, p_val = stats.ttest_ind(grupo_a, grupo_b)
else:
    stat, p_val = stats.mannwhitneyu(grupo_a, grupo_b)

print(f'p-valor={p_val:.4f} {"Significativo" if p_val < 0.05 else "No significativo"}')
```

**Por qué Mann-Whitney como plan B**: es la alternativa no paramétrica al t-test. No asume normalidad, funciona con muestras chicas, y es casi tan potente como el t-test cuando los supuestos se cumplen.

## ANOVA + post-hoc

```python
from statsmodels.stats.multicomp import pairwise_tukeyhsd

f_stat, p_val = stats.f_oneway(grupo1, grupo2, grupo3)
print(f'ANOVA F={f_stat:.3f}, p={p_val:.4f}')

if p_val < 0.05:
    tukey = pairwise_tukeyhsd(todos_los_datos, grupos, alpha=0.05)
    print(tukey)
```

**Por qué post-hoc después de ANOVA**: ANOVA te dice "al menos un grupo es diferente", pero no cuál. Tukey HSD compara todos los pares ajustando por comparaciones múltiples.

## Interpretación de p-value

```python
def interpretar_p(p_valor):
    if p_valor < 0.001: return '*** Altamente significativo'
    if p_valor < 0.01:  return '** Muy significativo'
    if p_valor < 0.05:  return '* Significativo'
    return 'ns No significativo'
```

## Anti-patrones

- ❌ **p-hacking**: hacer mil tests y reportar solo los significativos. No. Corregí por comparaciones múltiples (Bonferroni, FDR).
- ❌ **Confundir significancia estadística con importancia práctica**: un efecto tiny puede ser significativo con n grande. Calculá tamaño del efecto (Cohen's d, eta-cuadrado).
- ❌ **No verificar supuestos**: t-test en datos no normales da p-values incorrectos.
- ❌ **Olvidar que p > 0.05 no significa "no hay efecto"**: significa "no hay evidencia suficiente para rechazar la nula". Son cosas distintas.
- ❌ **Tests apareados como si fueran independientes**: perdés potencia estadística. Si son los mismos sujetos antes/después, usá `ttest_rel`.

## Alternativas

- **SciPy**: el estándar, cubre la mayoría de los casos.
- **Statsmodels**: más completo para modelos (ANOVA factorial, regresión logística, mixed models).
- **Pingouin**: wrapper amigable que incluye tamaños del efecto y reportes bonitos.
- **R + rpy2**: si necesitás tests muy específicos, R sigue teniendo más variedad.

## Tools relevantes

- `scipy.stats` — tests clásicos (t-test, ANOVA, chi-cuadrado, correlaciones)
- `statsmodels` — modelos más complejos y post-hoc
- `pingouin` — interfaz simple con tamaños del efecto incluidos
- `scikit-learn` — correlaciones y features selection para ML
