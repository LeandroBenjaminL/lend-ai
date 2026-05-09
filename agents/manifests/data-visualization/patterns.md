# Patterns: Visualización Cheat Sheet

## Configuración inicial

```python
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

sns.set_theme(style='whitegrid', palette='viridis', font_scale=1.1)
# Alternativa: plt.style.use('seaborn-v0_8-darkgrid')
```

## Elección de librería

| Librería | Para | Contra |
|---|---|---|
| Matplotlib | Control quirúrgico, publicación, subplots complejos | Defaults feos, verboso |
| Seaborn | Estadístico, lindo por defecto, `hue`/`size` | Menos personalizable, dependencia de pandas |
| Plotly Express | Interactivo, HTML, dashboards, hover rico | Más pesado, no publicable en papel |

## Catálogo de charts

### Bar plot
```python
# Seaborn — el más limpio
sns.barplot(data=df, x='cat', y='val', hue='grupo', palette='Set2')
plt.xticks(rotation=45, ha='right')

# Plotly — interactivo
px.bar(df, x='cat', y='val', color='grupo', barmode='group')
```

### Line plot
```python
# Datos en formato largo
sns.lineplot(data=df, x='fecha', y='val', hue='serie', marker='o')

# Plotly
px.line(df, x='fecha', y='val', color='serie', markers=True)
```

### Scatter plot con regresión
```python
# Con regresión lineal + intervalo de confianza
sns.regplot(data=df, x='x', y='y', scatter_kws={'alpha': 0.3}, line_kws={'color': 'red'})

# Scatter categórico con Plotly
px.scatter(df, x='x', y='y', color='cat', size='poblacion', hover_data=['nombre'],
           trendline='ols')
```

### Heatmap de correlación
```python
corr = df.corr(numeric_only=True)
mask = np.triu(np.ones_like(corr, dtype=bool))  # triangular superior

sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
            center=0, square=True, linewidths=0.5, cbar_kws={'shrink': 0.8})
```

### Boxplot por categoría
```python
sns.boxplot(data=df, x='cat', y='val', hue='grupo', palette='Set3',
            flierprops={'marker': 'o', 'alpha': 0.3})
# Alternativa superior: violin plot
sns.violinplot(data=df, x='cat', y='val', hue='grupo', split=True)
```

### Histograma + KDE
```python
sns.histplot(data=df, x='val', bins='auto', kde=True, hue='grupo',
             element='step', stat='density', common_norm=False)
```

### Pairplot (matriz de scatters)
```python
sns.pairplot(df, vars=['x', 'y', 'z'], hue='cat', diag_kind='kde',
             plot_kws={'alpha': 0.4}, corner=True)
```

## Múltiples subplots

```python
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(16, 10))

for ax, col in zip(axes.flat, columnas):
    sns.histplot(data=df, x=col, ax=ax, kde=True)
    ax.set_title(col, fontweight='bold')

fig.suptitle('Distribuciones por variable', fontsize=16, y=1.02)
plt.tight_layout()
```

## Customización esencial

```python
# Tamaño fijo
plt.figure(figsize=(12, 6))
sns.set_context('talk')  # 'paper', 'notebook', 'talk', 'poster'

# Anotaciones directas
ax.annotate('Pico acá', xy=(x, y), xytext=(x+1, y+10),
            arrowprops={'arrowstyle': '->', 'color': 'gray'})

# Exportación
plt.savefig('chart.png', dpi=300, bbox_inches='tight', transparent=False,
            facecolor='white')

# Plotly a archivo
fig.write_html('chart.html', include_plotlyjs='cdn')  # más liviano
fig.write_image('chart.png', scale=2)  # requiere kaleido
```

## Paletas accesibles (colorblind-friendly)

| Categóricas | Secuenciales | Divergentes |
|---|---|---|
| `'Set2'` | `'viridis'` | `'RdBu_r'` |
| `'tab10'` | `'cividis'` | `'coolwarm'` |
| `'Accent'` | `'rocket'` | `'Spectral_r'` |

```python
sns.set_palette('viridis')         # global
sns.color_palette('Set2', n_colors=5)  # ad-hoc
px.scatter(df, x='x', y='y', color_discrete_sequence=px.colors.qualitative.Set2)
```

## Reglas de oro visuales

1. **Un gráfico = un mensaje.** Si tenés dos historias, hacé dos gráficos.
2. **Ejes siempre etiquetados.** "Valor" no es una etiqueta útil.
3. **La escala del eje Y empieza en cero** para barras. Para líneas podés cortar — pero avisá.
4. **Overplotting > 10k puntos:** usá hexbin, contour, o alpha bajo (0.1-0.3).
5. **Colores:** menos es más. Si hacés un bar plot con 20 categorías, el color no es el canal visual correcto.
6. **Evitá el pie chart.** Siempre hay una opción mejor. La única excepción: 2-3 categorías con diferencia evidente.
7. **Nunca 3D sin justificación real.** Si la tercera dimensión no agrega datos, es ruido visual.
