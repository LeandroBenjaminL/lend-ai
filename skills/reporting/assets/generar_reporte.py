"""
Genera reporte markdown automático a partir de un CSV.
USO: python generar_reporte.py datos.csv [output.md]
"""

import sys
from datetime import datetime

import pandas as pd


def generar_reporte(ruta_csv: str, ruta_out: str = "reporte.md") -> str:
    df = pd.read_csv(ruta_csv, low_memory=False)
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    lines = [
        "# Reporte de Análisis",
        f"\n**Fecha**: {fecha}",
        f"**Dataset**: {ruta_csv}",
        "\n## Resumen",
        f"\n- **Registros**: {len(df):,}",
        f"- **Columnas**: {df.shape[1]}",
        f"- **Nulos totales**: {df.isnull().sum().sum():,}",
        f"- **Duplicados**: {df.duplicated().sum():,}",
        "\n## Columnas",
        "\n| Columna | Tipo | No nulos | Únicos |",
        "|---------|------|----------|--------|",
    ]

    for col in df.columns:
        lines.append(
            f"| {col} | {df[col].dtype} | {df[col].notna().sum():,} | {df[col].nunique():,} |"
        )

    numericas = df.select_dtypes(include="number").columns.tolist()
    if numericas:
        lines.append("\n## Estadísticas numéricas\n")
        lines.append(df[numericas].describe().round(2).to_markdown())

    with open(ruta_out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Reporte guardado en {ruta_out}")
    return ruta_out


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else input("CSV: ")
    out = sys.argv[2] if len(sys.argv) > 2 else "reporte.md"
    generar_reporte(ruta, out)
