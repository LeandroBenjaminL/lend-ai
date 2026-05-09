# Patterns: Reporting Cheat Sheet

## Configuración inicial

```python
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
```

## 1. DataFrame estilizado para reportes

### Tabla Markdown (rápida, versionable)

```python
# Tabla simple con formato
print(df.head(10).to_markdown(index=False, tablefmt='pipe'))

# Con formato de columnas aplicado antes
display_df = df.copy()
display_df['monto'] = display_df['monto'].apply(lambda x: f'${x:,.2f}')
display_df['pct'] = display_df['pct'].apply(lambda x: f'{x:.1f}%')
print(display_df.to_markdown(index=False))
```

### Tabla HTML estilizada (presentable)

```python
def estilizar_tabla(df: pd.DataFrame, titulo: str = '') -> str:
    """Devuelve HTML de una tabla con estilo inline."""
    estilos = [
        {'selector': 'th', 'props': [
            ('background-color', '#2c3e50'),
            ('color', 'white'),
            ('font-weight', 'bold'),
            ('padding', '8px 12px'),
            ('text-align', 'left'),
        ]},
        {'selector': 'td', 'props': [
            ('padding', '6px 12px'),
            ('border-bottom', '1px solid #ddd'),
        ]},
        {'selector': 'tr:hover', 'props': [
            ('background-color', '#f5f5f5'),
        ]},
    ]
    styled = (df.style
        .set_table_styles(estilos)
        .format({'monto': '${:,.2f}', 'pct': '{:.1f}%'})
        .set_caption(titulo)
    )
    return styled.to_html()
```

### Exportar a Excel formateado

```python
with pd.ExcelWriter('reporte.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Resumen', index=False)
    df.describe().to_excel(writer, sheet_name='Estadísticas')
```

## 2. Plantilla de reporte Markdown con variables

```python
from datetime import datetime

def generar_reporte_md(
    titulo: str,
    resumen: str,
    hallazgos: list[dict],  # [{'titulo': str, 'desc': str, 'dato': str}]
    tabla: pd.DataFrame,
    recomendaciones: list[str],
    ruta: str,
) -> str:
    """Genera un reporte Markdown estructurado."""
    ahora = datetime.now().strftime('%d/%m/%Y %H:%M')
    md = f"""# {titulo}

**Generado**: {ahora}

---

## Resumen Ejecutivo

{resumen}

---

## Hallazgos Principales

"""
    for i, h in enumerate(hallazgos, 1):
        md += f"### {i}. {h['titulo']}\n\n{h['desc']}\n\n> **Dato clave**: {h['dato']}\n\n"

    md += f"---\n\n## Datos\n\n{tabla.head(10).to_markdown(index=False)}\n\n"
    md += f"---\n\n## Recomendaciones\n\n"
    for i, rec in enumerate(recomendaciones, 1):
        md += f"{i}. {rec}\n"
    md += f"\n---\n\n*Reporte generado automáticamente — {ahora}*"

    Path(ruta).write_text(md, encoding='utf-8')
    return ruta
```

## 3. Plantilla HTML con estilo inline (sin dependencias externas)

```python
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{titulo}</title>
<style>
  body {{ font-family: 'Segoe UI', system-ui, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; color: #333; }}
  h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
  h2 {{ color: #2c3e50; margin-top: 30px; }}
  .resumen {{ background: #eaf2f8; padding: 20px; border-left: 4px solid #3498db; border-radius: 4px; margin: 20px 0; }}
  .hallazgo {{ background: #f9f9f9; padding: 15px; margin: 15px 0; border-radius: 6px; }}
  .hallazgo h3 {{ margin-top: 0; color: #e74c3c; }}
  .dato-clave {{ background: #2c3e50; color: white; padding: 8px 15px; border-radius: 4px; display: inline-block; font-weight: bold; }}
  .recomendaciones li {{ margin: 10px 0; padding: 8px; }}
  .footer {{ color: #999; font-size: 0.9em; margin-top: 40px; border-top: 1px solid #ddd; padding-top: 15px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
  th {{ background: #2c3e50; color: white; padding: 8px 12px; text-align: left; }}
  td {{ padding: 6px 12px; border-bottom: 1px solid #ddd; }}
  tr:hover {{ background: #f5f5f5; }}
  img {{ max-width: 100%; height: auto; margin: 15px 0; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
</style>
</head>
<body>
{contenido}
<div class="footer">Reporte generado automáticamente — {fecha}</div>
</body>
</html>"""

def generar_reporte_html(titulo: str, contenido: str, ruta: str) -> str:
    """Envuelve contenido HTML en la plantilla estilizada."""
    from datetime import datetime
    html = HTML_TEMPLATE.format(
        titulo=titulo,
        contenido=contenido,
        fecha=datetime.now().strftime('%d/%m/%Y %H:%M'),
    )
    Path(ruta).write_text(html, encoding='utf-8')
    return ruta
```

## 4. Incrustar gráficos de Matplotlib en el reporte

```python
import base64
from io import BytesIO

def fig_a_base64(fig) -> str:
    """Convierte una figura de Matplotlib a base64 para incrustar en HTML."""
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    return f'<img src="data:image/png;base64,{b64}" alt="Gráfico">'

# Uso en reporte HTML:
# contenido += fig_a_base64(fig)  # incrusta el gráfico directamente
```

### Guardar gráfico como archivo y referenciar

```python
fig.savefig('graficos/ventas_por_region.png', dpi=300, bbox_inches='tight', facecolor='white')
# En HTML: <img src="graficos/ventas_por_region.png" alt="Ventas por región">
```

## 5. Conversión a PDF

### Desde HTML (recomendado)

```bash
pip install weasyprint

# Python
# from weasyprint import HTML
# HTML('reporte.html').write_pdf('reporte.pdf')
```

```bash
# CLI directo
weasyprint reporte.html reporte.pdf
```

### Desde Markdown

```bash
pip install grip  # preview
# O usar pandoc para conversión
pandoc reporte.md -o reporte.pdf --pdf-engine=weasyprint
pandoc reporte.md -o reporte.html --standalone --css=estilo.css
```

### Desde Jupyter Notebook

```bash
# HTML (mantiene gráficos interactivos)
jupyter nbconvert --to html analisis.ipynb --output reporte.html --no-input

# PDF (requiere LaTeX o webpdf)
jupyter nbconvert --to pdf analisis.ipynb
jupyter nbconvert --to webpdf analisis.ipynb  # no requiere LaTeX

# Ejecutar + exportar en un paso
jupyter nbconvert --to html --execute --no-input analisis.ipynb --output reporte_final.html
```

## 6. Reporte rápido con ydata-profiling

```python
from ydata_profiling import ProfileReport

# Generar reporte exploratorio automático
profile = ProfileReport(df, title="Reporte de Calidad de Datos", explorative=True)
profile.to_file("reporte_calidad.html")

# Versión mínima (más rápida)
profile = ProfileReport(df, minimal=True)
profile.to_file("reporte_minimo.html")
```

## 7. Formateo rápido de números para reportes

```python
# Moneda
f"${valor:,.2f}"           # $1,234,567.89   → Python
lambda x: f"${x:,.2f}"     # en DataFrame .apply()

# Porcentajes
f"{pct:.1f}%"              # 23.5%

# Fechas en español
from locale import setlocale, LC_TIME
setlocale(LC_TIME, 'es_AR.UTF-8')  # o 'es_ES.UTF-8'
fecha.strftime('%d de %B de %Y')   # 15 de marzo de 2024

# Miles y decimales
f"{n:,.0f}"                # 1234567 → 1,234,567
f"{n:,.2f}"                # 1234567.89 → 1,234,567.89
```

## Reglas de oro del reporting

1. **Resumen ejecutivo PRIMERO.** Si el lector solo lee eso, ya tiene que saber qué pasa y qué hacer.
2. **Una historia, no una colección de datos.** Cada sección construye sobre la anterior. "Y por eso..." es la frase que conecta hallazgos con recomendaciones.
3. **Números en contexto.** "Las ventas subieron 15%" no dice nada. "Las ventas subieron 15% interanual, el mejor Q1 desde 2019" cuenta una historia.
4. **Cada gráfico responde UNA pregunta.** Si responde más de una, partilo. Si no responde ninguna, borralo.
5. **Formato humano.** Fechas: "15 mar 2024", no "2024-03-15T00:00:00Z". Montos: "$1.2M", no "1234567.8912". Porcentajes: "23.5%", no "0.234567".
6. **Menos es más.** Si un reporte de 20 páginas se puede contar en 5, la versión de 5 es mejor. La síntesis es generosidad con el tiempo del lector.
