# Statistical Testing — Patterns Cheat Sheet

## Catálogo rápido de funciones

Cada patrón incluye: **qué hace**, **cuándo usarlo**, **precondiciones**, y **cómo interpretarlo**.

---

## Tests paramétricos

### `ttest_ind` — t-test para grupos independientes

```python
from scipy import stats
stat, p = stats.ttest_ind(grupo_a, grupo_b)
# Con varianzas desiguales (Welch):
stat, p = stats.ttest_ind(grupo_a, grupo_b, equal_var=False)
```

| Aspecto | Detalle |
|---------|---------|
| ¿Cuándo? | Comparar media de 2 grupos independientes con variable numérica |
| H₀ | μ₁ = μ₂ (las medias son iguales) |
| H₁ | μ₁ ≠ μ₂ (bilateral, por defecto) |
| Supuestos | Normalidad en cada grupo (o n ≥ 30), independencia |
| Versión robusta | `equal_var=False` (Welch) si Levene da p < 0.05 |
| Tamaño de efecto | Cohen's d = (μ₁ − μ₂) / s_pooled |
| Si fallan supuestos | Usar `mannwhitneyu` |

---

### `ttest_rel` — t-test pareado

```python
stat, p = stats.ttest_rel(antes, despues)
```

| Aspecto | Detalle |
|---------|---------|
| ¿Cuándo? | Misma unidad medida dos veces (antes/después, gemelos, pares apareados) |
| H₀ | μ_dif = 0 (la diferencia promedio es cero) |
| H₁ | μ_dif ≠ 0 |
| Supuestos | Las diferencias son normales, independencia entre pares |
| Tamaño de efecto | Cohen's d = μ_dif / s_dif |
| Si fallan supuestos | Usar `wilcoxon` |

---

### `f_oneway` — ANOVA de una vía

```python
stat, p = stats.f_oneway(grupo_1, grupo_2, grupo_3)
```

| Aspecto | Detalle |
|---------|---------|
| ¿Cuándo? | Comparar medias de 3+ grupos independientes |
| H₀ | μ₁ = μ₂ = μ₃ = ... (todas las medias iguales) |
| H₁ | Al menos una media difiere |
| Supuestos | Normalidad en cada grupo, homocedasticidad (Levene), independencia |
| Tamaño de efecto | η² (eta-squared) = SS_between / SS_total |
| Post-hoc | Si p < 0.05, hacer `pairwise_tukeyhsd` para ver qué grupos difieren |
| Si fallan supuestos | Usar `kruskal` |

---

## Tests no paramétricos

### `mannwhitneyu` — Mann-Whitney U

```python
stat, p = stats.mannwhitneyu(grupo_a, grupo_b, alternative='two-sided')
```

| Aspecto | Detalle |
|---------|---------|
| ¿Cuándo? | Alternativa no paramétrica al `ttest_ind`. No asume normalidad. |
| H₀ | Las distribuciones de ambos grupos son iguales (misma mediana) |
| H₁ | Las distribuciones difieren |
| Supuestos | Independencia, misma forma de distribución (para comparar medianas) |
| Tamaño de efecto | r = Z / √N |
| Ojo | Compara rangos, no medias. Si las distribuciones tienen forma distinta, interpretar con cuidado. |

---

### `wilcoxon` — Wilcoxon signed-rank

```python
stat, p = stats.wilcoxon(antes, despues)
```

| Aspecto | Detalle |
|---------|---------|
| ¿Cuándo? | Alternativa no paramétrica al `ttest_rel` |
| H₀ | La mediana de las diferencias es cero |
| Supuestos | Las diferencias son simétricas |

---

### `kruskal` — Kruskal-Wallis

```python
stat, p = stats.kruskal(grupo_1, grupo_2, grupo_3)
```

| Aspecto | Detalle |
|---------|---------|
| ¿Cuándo? | Alternativa no paramétrica al ANOVA de una vía |
| H₀ | Todas las medianas son iguales |
| Post-hoc | Dunn's test (requiere `scikit-posthocs`) |

---

## Tablas de contingencia

### `chi2_contingency` — Chi-cuadrado de independencia

```python
from scipy import stats
chi2, p, dof, expected = stats.chi2_contingency(tabla_contingencia)
```

| Aspecto | Detalle |
|---------|---------|
| ¿Cuándo? | Asociación entre 2 variables categóricas |
| H₀ | Las variables son independientes |
| H₁ | Hay asociación entre las variables |
| Precondición | Frecuencias esperadas ≥ 5 en ≥ 80% de celdas |
| Si no cumple | Usar `fisher_exact` (solo 2×2) |
| Tamaño de efecto | V de Cramer = √(χ² / (N × min(filas−1, columnas−1))) |

---

### `fisher_exact` — Test exacto de Fisher

```python
odds_ratio, p = stats.fisher_exact(tabla_2x2)
```

| Aspecto | Detalle |
|---------|---------|
| ¿Cuándo? | Tabla 2×2 con frecuencias esperadas < 5 |

---

## Correlaciones

### `pearsonr` — Correlación de Pearson

```python
r, p = stats.pearsonr(x, y)
```

| Aspecto | Detalle |
|---------|---------|
| ¿Cuándo? | Relación lineal entre 2 variables numéricas continuas |
| H₀ | ρ = 0 (no hay correlación lineal) |
| H₁ | ρ ≠ 0 |
| Supuestos | Ambas variables normales, relación lineal, sin outliers extremos |
| Interpretación de r | 0.1 pequeño, 0.3 mediano, 0.5 grande. r ya ES tamaño de efecto. |
| Si fallan supuestos | Usar `spearmanr` |

---

### `spearmanr` — Correlación de Spearman

```python
rho, p = stats.spearmanr(x, y)
```

| Aspecto | Detalle |
|---------|---------|
| ¿Cuándo? | Relación monótona (no necesariamente lineal), variables ordinales, o cuando falla normalidad |
| H₀ | ρ_s = 0 (no hay correlación monótona) |
| Ventaja | Robusto a outliers, no asume normalidad |
| Limitación | Solo detecta relaciones monótonas (si la relación tiene forma de U, ρ ≈ 0 aunque exista relación) |

---

### `kendalltau` — Tau de Kendall

```python
tau, p = stats.kendalltau(x, y)
```

| Aspecto | Detalle |
|---------|---------|
| ¿Cuándo? | Alternativa a Spearman, mejor con muchos empates o muestras chicas |
| Interpretación | Más conservador que Spearman, converge más lento |

---

## Verificación de supuestos

### `shapiro` — Test de normalidad de Shapiro-Wilk

```python
stat, p = stats.shapiro(datos)
```

| Aspecto | Detalle |
|---------|---------|
| ¿Cuándo? | Verificar si una muestra proviene de una distribución normal |
| H₀ | Los datos son normales |
| Interpretación | Si p > 0.05, no rechazamos normalidad (podemos usar test paramétrico) |
| Ojo | Con muestras grandes (n > 5000), casi siempre rechaza. Usar Q-Q plot o asimetría/curtosis. |
| Alternativas | `normaltest` (D'Agostino-Pearson, más sensible a asimetría y curtosis) |

---

### `levene` — Test de homogeneidad de varianzas

```python
stat, p = stats.levene(grupo_a, grupo_b, grupo_c)
```

| Aspecto | Detalle |
|---------|---------|
| ¿Cuándo? | Verificar si 2+ grupos tienen varianzas iguales |
| H₀ | Las varianzas son iguales |
| Interpretación | Si p < 0.05, usar test con corrección (Welch) o no paramétrico |
| Alternativa | `bartlett` (más sensible a no-normalidad) |

---

## Patrón completo: flujo de decisión automático

```python
from scipy import stats
import numpy as np

def elegir_y_ejecutar_test(grupo_a, grupo_b, pareado=False, alpha=0.05):
    """
    Selecciona y ejecuta el test apropiado según supuestos.
    Retorna: (nombre_test, estadístico, p_valor, tamaño_efecto, interpretación)
    """
    if pareado:
        # Verificar normalidad de las diferencias
        dif = np.array(grupo_a) - np.array(grupo_b)
        _, p_norm = stats.shapiro(dif)

        if p_norm > alpha:
            stat, p = stats.ttest_rel(grupo_a, grupo_b)
            d = np.mean(dif) / np.std(dif, ddof=1)  # Cohen's d
            return "t-test pareado", stat, p, d, "paramétrico"
        else:
            stat, p = stats.wilcoxon(grupo_a, grupo_b)
            n = len(dif)
            r = stat / np.sqrt(n) if n > 0 else 0
            return "Wilcoxon", stat, p, r, "no paramétrico"
    else:
        # Verificar normalidad en cada grupo
        _, p_norm_a = stats.shapiro(grupo_a)
        _, p_norm_b = stats.shapiro(grupo_b)
        normales = (p_norm_a > alpha) and (p_norm_b > alpha)

        # Verificar homocedasticidad
        _, p_var = stats.levene(grupo_a, grupo_b)
        var_iguales = p_var > alpha

        if normales and var_iguales:
            stat, p = stats.ttest_ind(grupo_a, grupo_b)
            # Cohen's d
            n1, n2 = len(grupo_a), len(grupo_b)
            s1, s2 = np.std(grupo_a, ddof=1), np.std(grupo_b, ddof=1)
            s_pooled = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2))
            d = (np.mean(grupo_a) - np.mean(grupo_b)) / s_pooled
            return "t-test Student", stat, p, d, "paramétrico"
        elif normales and not var_iguales:
            stat, p = stats.ttest_ind(grupo_a, grupo_b, equal_var=False)
            return "t-test Welch", stat, p, None, "paramétrico (Welch)"
        else:
            stat, p = stats.mannwhitneyu(grupo_a, grupo_b, alternative='two-sided')
            n = len(grupo_a) + len(grupo_b)
            r = stat / (n * np.sqrt(n)) if n > 0 else 0
            return "Mann-Whitney U", stat, p, r, "no paramétrico"
```

---

## Reglas nemotécnicas

| Si tenés... | ...y querés... | ...usá |
|-------------|---------------|--------|
| 2 grupos, numérico, independientes | comparar medias | `ttest_ind` → si no normal: `mannwhitneyu` |
| 2 grupos, numérico, pareados | comparar medias | `ttest_rel` → si no normal: `wilcoxon` |
| 3+ grupos, numérico, independientes | comparar medias | `f_oneway` → si no normal: `kruskal` |
| 2 categóricas | ver asociación | `chi2_contingency` |
| 2 numéricas | ver correlación lineal | `pearsonr` |
| 2 numéricas | ver correlación monótona | `spearmanr` |
| 1 numérica | verificar normalidad | `shapiro` |
| 2+ grupos numéricos | verificar varianzas iguales | `levene` |
| ANOVA significativo | encontrar qué grupos difieren | `pairwise_tukeyhsd` |
