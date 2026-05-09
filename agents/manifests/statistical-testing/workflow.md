# Statistical Testing — Workflow

## Flujo de trabajo

Cada análisis sigue este proceso. No se saltea pasos. No se elige el test "porque es el que conozco".

---

### 1. Definir hipótesis (ANTES de mirar los datos)

- **H₀ (hipótesis nula):** "No hay diferencia" / "No hay asociación" / "No hay efecto". Es lo que intentamos refutar.
- **H₁ (hipótesis alternativa):** Lo que sospechamos que es verdad. Puede ser bilateral ("hay diferencia") o unilateral ("A > B").
- **α (nivel de significancia):** Típicamente 0.05, pero debe definirse explícitamente.
- **Potencia deseada:** Idealmente ≥ 0.80. Determina el tamaño muestral necesario.

⚠️ Si miraste los datos antes de definir H₀ y H₁, ya estás en territorio de p-hacking. No lo hagas.

---

### 2. Elegir el test según tipo de datos y pregunta

Usá la **tabla de decisión** (abajo) para seleccionar el test correcto. Las preguntas clave:

| Pregunta | Opciones |
|----------|----------|
| ¿Cuántos grupos? | 1 grupo / 2 grupos / 3+ grupos |
| ¿Tipo de variable? | Numérica continua / Categórica / Ordinal |
| ¿Grupos independientes o pareados? | Independientes / Pareados (misma unidad medida dos veces) |
| ¿Objetivo? | Comparar medias / Comparar distribuciones / Asociación / Correlación |

---

### 3. Verificar supuestos del test

Todo test paramétrico tiene supuestos. Verificarlos **no es opcional**.

| Supuesto | Test para verificarlo | Qué hacer si falla |
|----------|----------------------|---------------------|
| **Normalidad** | Shapiro-Wilk (`shapiro`) | Usar test no paramétrico (Mann-Whitney, Kruskal-Wallis, Spearman) |
| **Homocedasticidad** (varianzas iguales) | Levene (`levene`) | Usar `ttest_ind` con `equal_var=False` (Welch) o no paramétrico |
| **Independencia** | Diseño experimental | Si hay dependencia no modelada → modelos mixtos o GEE |
| **Esfericidad** (ANOVA medidas repetidas) | Mauchly | Corrección Greenhouse-Geisser |

Regla práctica: si n ≥ 30 por grupo, el teorema central del límite ayuda con la normalidad de las medias, pero **siempre** conviene verificarlo.

---

### 4. Ejecutar el test

```python
from scipy import stats

# Ejemplo: t-test para grupos independientes
stat, p_valor = stats.ttest_ind(grupo_a, grupo_b)
print(f"Estadístico: {stat:.4f}, p-valor: {p_valor:.4f}")
```

---

### 5. Interpretar resultados

**No alcanza con decir "p < 0.05".** Reportar siempre:

| Qué reportar | Por qué |
|-------------|---------|
| **p-value** | Probabilidad de observar los datos (o algo más extremo) si H₀ fuera verdadera. No es la probabilidad de que H₀ sea falsa. |
| **Tamaño de efecto** | Magnitud práctica de la diferencia. Un p-value chico con efecto minúsculo es irrelevante. |
| **Intervalo de confianza** | Rango plausible para el efecto real. Más informativo que un p-value binario. |
| **Potencia del test** | Probabilidad de detectar un efecto si existe. Si no hubo significancia, ¿fue por falta de efecto o por falta de potencia? |

**Tamaños de efecto por test:**

| Test | Tamaño de efecto | Pequeño | Mediano | Grande |
|------|-----------------|---------|---------|--------|
| t-test | Cohen's d | 0.2 | 0.5 | 0.8 |
| ANOVA | η² (eta-squared) | 0.01 | 0.06 | 0.14 |
| Chi-cuadrado | V de Cramer | 0.1 | 0.3 | 0.5 |
| Correlación | r (ya es tamaño de efecto) | 0.1 | 0.3 | 0.5 |
| Mann-Whitney | r = Z / √N | 0.1 | 0.3 | 0.5 |

---

### 6. Conclusión en lenguaje de negocio

Traducir el resultado a algo accionable:

- ❌ **Mal:** "El p-value fue 0.032, se rechaza H₀."
- ✅ **Bien:** "Hay evidencia de que el tratamiento A reduce el tiempo de carga en promedio 2.3 segundos respecto al control (p = 0.032, d de Cohen = 0.62). Es una diferencia moderada y estadísticamente significativa."

Si el resultado **no es significativo**:
- No digas "no hay diferencia". Decí: "No encontramos evidencia suficiente para rechazar que no hay diferencia."
- Reportá la potencia: ¿teníamos suficientes datos para detectar el efecto esperado?

---

## Tabla de decisión: ¿Qué test usar?

### Comparar grupos — Variable numérica

| Grupos | Tipo | Supuestos OK | Supuestos NO OK |
|--------|------|-------------|-----------------|
| 2 grupos | Independientes | `ttest_ind` (Student) | `mannwhitneyu` |
| 2 grupos | Independientes, varianzas desiguales | `ttest_ind(equal_var=False)` (Welch) | `mannwhitneyu` |
| 2 grupos | Pareados | `ttest_rel` | `wilcoxon` |
| 3+ grupos | Independientes | `f_oneway` (ANOVA) | `kruskal` (Kruskal-Wallis) |
| 3+ grupos | Pareados (medidas repetidas) | `f_oneway` repeated / `friedmanchisquare` | `friedmanchisquare` |

### Comparar proporciones / Tablas de contingencia

| Objetivo | Test |
|----------|------|
| Asociación entre 2 variables categóricas | `chi2_contingency` |
| Tabla 2×2 con frecuencias bajas (< 5) | `fisher_exact` |
| Proporción observada vs esperada (una muestra) | `chisquare` (goodness-of-fit) |
| Comparar 2 proporciones | `proportions_ztest` (statsmodels) |

### Correlación / Asociación

| Tipo de variables | Test |
|-------------------|------|
| Ambas numéricas, relación lineal | `pearsonr` |
| Ambas numéricas, relación monótona | `spearmanr` |
| Una o ambas ordinales | `spearmanr` o `kendalltau` |
| Una categórica y una numérica | `f_oneway` o `kruskal` |
| Ambas binarias | `chi2_contingency` |

### Comparar distribuciones

| Objetivo | Test |
|----------|------|
| Distribución observada vs teórica | `kstest` (Kolmogorov-Smirnov) |
| Distribución observada vs teórica (discreta) | `chisquare` |
| Comparar 2 distribuciones | `ks_2samp` |

### Post-hoc (tras ANOVA significativo)

| Objetivo | Test |
|----------|------|
| Comparar todos los pares | `pairwise_tukeyhsd` (Tukey HSD) |
| Control más robusto | Bonferroni (manual: α / n_comparaciones) |
| Menos conservador | `holm` (método step-down) |

---

## Checklist de rigor

Antes de dar un resultado por válido, verificá:

- [ ] H₀ y H₁ definidas ANTES del análisis.
- [ ] α definido explícitamente.
- [ ] Supuestos del test verificados (normalidad, homocedasticidad).
- [ ] Si los supuestos fallan, se usó la alternativa no paramétrica.
- [ ] Se reportó el tamaño de efecto.
- [ ] Se reportó el intervalo de confianza (cuando aplica).
- [ ] Si hubo múltiples comparaciones, se aplicó corrección.
- [ ] La conclusión está en lenguaje de negocio, no en jerga estadística.
- [ ] Si el resultado no fue significativo, se discutió la potencia del test.
