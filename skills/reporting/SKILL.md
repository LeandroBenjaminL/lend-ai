---
name: reporting
description: >
  Generación de reportes automáticos de datos: HTML, PDF, Markdown y reportes estilizados con Pandas.
  Trigger: Cuando necesitás generar un reporte de análisis, exportar resultados a un formato presentable, o automatizar la producción de informes.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "2.0"
  model_tier: T2-fast
---

# Skill: reporting

Los reportes automáticos son el equivalente a **tener un asistente que arma el informe mientras vos dormís**. La idea es que el análisis se genera una vez (el script) y se ejecuta N veces (cada vez que necesitás el reporte). Sin copypaste, sin errores humanos, sin "me olvidé de actualizar la fecha".

Pero ojo: un mal reporte es peor que no tener reporte. Si tiene números inconsistentes, tablas que no se entienden, o métricas sin contexto, genera más confusión que claridad.

## Trigger

- Tenés que mandar un reporte periódico (diario, semanal, mensual) a alguien
- Querés compartir resultados de análisis con stakeholders no técnicos
- Necesitás exportar tablas estilizadas para una presentación o documento
- Querés automatizar algo que hoy hacés a mano en Excel cada semana

## Workflow

### 1. Definí la audiencia
¿Quién va a leer esto? Un ejecutivo quiere métricas clave y tendencias. Un equipo técnico quiere tablas detalladas y distribuciones. Un cliente quiere lo que pactaron, ni más ni menos.

### 2. Elegí el formato según el canal
- **Markdown**: para adjuntar en Slack/email, fácil de leer, se renderiza solo
- **HTML**: para reportes ricos con estilo, gráficos embebidos, interactivo
- **Excel**: para que el receptor pueda filtrar, ordenar y hacer sus propios cálculos
- **PDF**: para entregas formales, regulatorias o impresas

### 3. Diseñá la estructura
Título, fecha de generación, resumen ejecutivo, tabla principal, gráfico clave, apéndice con metodología. La misma estructura siempre, para que el lector sepa dónde encontrar cada cosa.

### 4. Automatizá la generación
Un script que lea los datos, genere el reporte y lo distribuya (email, Drive, Slack) sin intervención humana.

## Patrones y ejemplos

### 1. DataFrame estilizado — presentable para compartir

```python
def estilizar_resumen(df: pd.DataFrame) -> pd.io.formats.style.Styler:
    """Aplica formato profesional a un DataFrame de resumen"""
    return (df.style
        .format({
            'monto': '${:,.2f}',          # formato monetario
            'porcentaje': '{:.1f}%',       # porcentaje con 1 decimal
            'fecha': lambda x: x.strftime('%d/%m/%Y')
        })
        .background_gradient(subset=['monto'], cmap='YlOrRd')  # heatmap visual
        .bar(subset=['variacion'], color=['#FF4444', '#44BB44'])  # barras in-cell
        .set_caption('Resumen de Ventas — Q1 2024')
        .hide(axis='index')
    )

# Exportar a Excel con estilo (ideal para mandar al negocio)
estilo = estilizar_resumen(df_resumen)
estilo.to_excel('reporte_ventas.xlsx', engine='openpyxl', index=False)

# Exportar a HTML (ideal para adjuntar en email o subir a intranet)
with open('reporte.html', 'w', encoding='utf-8') as f:
    f.write(estilo.tohtml())
```

**¿Por qué Styler?**: Pandas Styler te da formato condicional, colores y barras sin instalar nada extra. Se exporta a Excel con openpyxl y a HTML tal cual. No necesitás una biblioteca de reporting aparte.

### 2. Reporte Markdown automático — para Slack/email

```python
def generar_reporte_md(df: pd.DataFrame, titulo: str, ruta: str):
    """Genera reporte Markdown con tabla principal y estadísticas"""
    lines = [
        f"# {titulo}",
        f"\n**Generado**: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}",
        f"\n## Resumen\n",
        f"- **Registros**: {len(df):,}",
        f"- **Período**: {df['fecha'].min().date()} → {df['fecha'].max().date()}",
        f"- **Total**: ${df['monto'].sum():,.0f}",
        f"\n## Top 10\n",
        df.head(10).to_markdown(index=False),
        f"\n## Estadísticas\n",
        df.describe().round(2).to_markdown(),
    ]
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
```

**¿Por qué Markdown?**: Se lee bien en crudo, se renderiza en GitHub/GitLab/Slack, y con `to_markdown()` generás tablas limpias en una línea. No necesita HTML engine ni template.

### 3. Exportar notebook a HTML/PDF

```bash
# HTML — recomendado, mantiene gráficos interactivos
jupyter nbconvert --to html analisis.ipynb --output reporte.html

# PDF — necesita LaTeX instalado (más lento, más formal)
jupyter nbconvert --to pdf analisis.ipynb

# Ejecutar y exportar en un solo paso (ideal para automatizar)
jupyter nbconvert --to html --execute analisis.ipynb --output reporte_$(date +%Y%m%d).html
```

### 4. Reporte automático recurrente — el santo grial

```python
def generar_reporte_periodico(df, frecuencia: str = "semanal"):
    """Genera nombre de archivo con timestamp y exporta"""
    fecha = pd.Timestamp.now().strftime('%Y%m%d')
    nombre = f"reporte_{frecuencia}_{fecha}.xlsx"

    with pd.ExcelWriter(nombre, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Resumen', index=False)
        df.describe().to_excel(writer, sheet_name='Estadísticas')
        # Podés agregar más sheets con gráficos, tablas pivot, etc.

    # Ideal: acoplar envío por email, upload a Drive o post a Slack
    print(f"✅ Reporte {nombre} generado")
    return nombre
```

## Alternativas

| Herramienta | Formato | Cuándo conviene |
|-------------|--------|-----------------|
| **Pandas Styler** | HTML / Excel | Reportes ad-hoc con formato condicional liviano |
| **nbconvert** | HTML / PDF | Cuando el reporte es un notebook (código + gráficos + texto) |
| **Quarto** | HTML / PDF / DOCX | Reportes técnicos reproducibles con Markdown + código |
| **Jinja2 + HTML** | HTML | Reportes web con templates custom, máximo control |
| **ReportLab** | PDF | PDFs desde cero con control pixel-perfect |
| **Streamlit** | Web app | Cuando necesitás interactividad, no un reporte estático |

**Recomendación**: para el 80% de los casos, Pandas Styler + Excel o Markdown alcanzan. nbconvert para notebooks. Quarto para documentación técnica larga.

## Anti-patrones

- ❌ **Reportes sin fecha ni contexto** — "ventas.csv" sin indicar si es de hoy o del mes pasado
- ❌ **Demasiados números sin interpretación** — tablas enormes que el lector no sabe leer
- ❌ **Gráficos sin etiquetas ni unidades** — un eje Y sin "$" o "%" no sirve de nada
- ❌ **Formato único para toda audiencia** — el mismo reporte para el CEO y para el equipo técnico casi nunca funciona
- ❌ **Script de reporte con paths hardcodeados** — cuando cambia la carpeta, todo se rompe
- ❌ **No versionar el script del reporte** — si el reporte cambia, no sabés qué versión se usó cuándo
