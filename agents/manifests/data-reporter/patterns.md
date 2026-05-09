# Patterns: Data Reporter Cheat Sheet

## Tabla de decisión de gráficos

### Por tipo de comparación

| Objetivo | Variables | Gráfico recomendado | Alternativa |
|---|---|---|---|
| Comparar valores entre categorías | 1 categórica + 1 numérica | Bar chart (vertical) | Horizontal si las etiquetas son largas |
| Comparar valores entre muchas categorías (>10) | 1 categórica + 1 numérica | Bar chart horizontal ordenado | Lollipop chart |
| Comparar a través del tiempo | 1 temporal + 1 numérica | Line chart | Área chart (si es acumulativo) |
| Comparar múltiples series temporales | 1 temporal + N numéricas | Multi-line chart con colores | Small multiples (mejor para >5 series) |
| Mostrar ranking | 1 categórica ordenada | Bar chart descendente | Dot plot (si hay pocos valores) |

### Por tipo de distribución

| Objetivo | Variables | Gráfico recomendado | Alternativa |
|---|---|---|---|
| Distribución de 1 variable | 1 numérica | Histograma (definir bins) | Density plot (suavizado) |
| Distribución de 1 variable, comparando grupos | 1 numérica + 1 categórica | Boxplot | Violin plot (si hay suficiente data) |
| Distribución de 2 variables | 2 numéricas | Scatter plot | Hexbin (si hay overplotting) |
| Distribución de 3+ variables | 3+ numéricas | Pairplot (scatter matrix) | Parallel coordinates |
| Outliers en 1 variable | 1 numérica | Boxplot o strip plot | — |

### Por tipo de composición

| Objetivo | Variables | Gráfico recomendado | Alternativa |
|---|---|---|---|
| Parte de un total (≤5 categorías) | 1 categórica + 1 numérica | Stacked bar horizontal | Donut chart (solo si son 2-3 partes) |
| Parte de un total (>5 categorías) | 1 categórica + 1 numérica | Bar chart + "Otros" agrupando small slices | Treemap |
| Cambio en composición en el tiempo | 1 temporal + 1 categórica + 1 numérica | Stacked area chart | Stacked bar chart por período |
| Proporciones anidadas | 2 categóricas jerárquicas | Treemap | Sunburst |

### Por tipo de relación

| Objetivo | Variables | Gráfico recomendado | Alternativa |
|---|---|---|---|
| Correlación entre 2 variables | 2 numéricas | Scatter plot + trend line | Hexbin |
| Correlación entre muchas variables | N numéricas | Heatmap de correlación | Scatter matrix |
| Relación con 3 variables | 3 numéricas | Bubble chart (tamaño = 3ra variable) | Scatter + color mapping |
| Flujo de una etapa a otra | 2+ categóricas + magnitud | Sankey diagram | Alluvial plot |
| Relación jerárquica | Jerarquía, valor | Treemap | Icicle plot |

## Anti-patrones (lo que NUNCA hacés)

| Anti-patrón | Qué es | Por qué evitarlo | Alternativa |
|---|---|---|---|
| **Gráficos 3D** | Chart con perspectiva 3D sin datos en Z | Distorsiona percepción, oculta datos, agrega ruido visual | Siempre 2D. Si hay 3ra variable, usá color/tamaño/ facetas |
| **Chartjunk** | Decoraciones gratuitas: sombras, gradientes, texturas, iconos decorativos | Aumenta carga cognitiva sin aportar información | Minimalismo: cada pixel debe comunicar un dato |
| **Escalas rotas** | Eje Y que no arranca en 0 en bar charts | Exagera diferencias, engaña al lector | Siempre 0 en barras. En líneas permitido con break explícito |
| **Pie charts con muchas categorías** | Pie chart con >5 slices | Dificilísimo comparar ángulos y áreas | Bar chart horizontal (ordenado) o treemap |
| **Dual axes conflictivos** | Dos ejes Y con escalas distintas en mismo chart | Confunde correlación con causalidad. Difícil de leer | Small multiples o dos charts separados |
| **Rainbow colormap** | Paletas que pasan por todo el espectro | No es perceptual-uniforme, confunde valores bajos con altos | Viridis, Plasma, o paletas secuenciales mono |
| **Overplotting ignorado** | Miles de puntos sobreimpresos sin transparencia | Oculta densidad real, parece haber menos datos | Alpha=0.3, hexbin, sampling, o density contours |
| **Sparklines sin contexto** | Minigráfico sin ejes ni escala | No se puede interpretar el valor absoluto | Sparkline + número clave al final |
| **Heatmap sin orden** | Filas/columnas sin clustereo | Patrones no se ven, parece ruido | Ordenar por dendrograma o por media/value |
| **Datos oceánicos** | Mostrar TODOS los decimales en tooltips/labels | Ruido mental, el lector no sabe qué número importa | Redondear a 2 dígitos significativos o al entero según contexto |

## Checklist de accesibilidad

Antes de entregar, verificás:

### Color
- [ ] Paleta testeada con simulador de daltonismo (Coblis o Color Oracle)
- [ ] No usás rojo/verde como único diferenciador
- [ ] Contraste mínimo 4.5:1 entre texto y fondo (WCAG AA)
- [ ] Información NO depende solo del color — usás patrones, etiquetas, grosores de línea

### Texto
- [ ] Tamaño mínimo 10px (12px ideal) para etiquetas de eje
- [ ] Título en negrita, 14px+, descriptivo del hallazgo
- [ ] Leyenda colocada óptimamente: dentro del gráfico si no tapa datos, fuera si es grande
- [ ] Labels directos sobre puntos/líneas en vez de leyenda separada

### Interactivo (Plotly / web)
- [ ] Tooltips con nombre de serie, valor exacto, y unidad
- [ ] Elementos clickeables tienen cursor: pointer
- [ ] Tamaño mínimo de hit area: 24px
- [ ] Navegación por teclado: tabindex ordenado
- [ ] Alt-text o aria-label descriptivo en el contenedor

### General
- [ ] Fuente: sans-serif, sin compresión de tracking (letter-spacing)
- [ ] Gridlines: gris (#ccc o más claro), 0.5px, dashed. O nada
- [ ] Fondo: blanco o transparente, nunca gris oscuro a menos que sea dashboard corporativo
- [ ] Proporción: no estirás ni comprimís el aspecto ratio — cuadrados para scatter, 16:9 o 4:3 para temporal
- [ ] Export: 300dpi si es print, mínimo 1200px de ancho si es web

## Paletas recomendadas

| Tipo | Paleta | Librería / Código |
|---|---|---|
| Categórica (discreta) | Set2, Pastel1, Tableau 10 | `seaborn.color_palette("Set2")` |
| Secuencial (0→N) | Blues, Greens, Viridis | `sns.color_palette("viridis", 9)` |
| Divergente (-N→0→+N) | RdYlBu, coolwarm, PiYG | `sns.color_palette("coolwarm", 11)` |
| Daltónica segura | IBM Carbon (categorical), Wong palette | `palette = ['#0072B2', '#E69F00', '#009E73', '#F0E442', '#56B4E9']` |
| Monocromática | Single hue + lightness | `sns.light_palette("blue", 9)` |

## Código boilerplate

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Estilo consistente
sns.set_theme(
    style="whitegrid",
    palette="Set2",
    font="sans-serif",
    font_scale=1.1,
    rc={
        "figure.figsize": (10, 6),
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "grid.alpha": 0.3,
        "grid.linestyle": "--",
    },
)

def styled_bar(df, x, y, title, palette="Set2"):
    ax = sns.barplot(data=df, x=x, y=y, palette=palette)
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel("")
    ax.bar_label(ax.containers[0], fmt="{:.0f}", fontsize=9)
    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    return ax
```
