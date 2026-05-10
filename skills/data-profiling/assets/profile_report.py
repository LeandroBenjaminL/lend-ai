"""
Perfil automático de dataset — genera reporte HTML de calidad.
USO: python profile_report.py datos.csv
"""

import sys

import numpy as np
import pandas as pd


def perfil_rapido(ruta: str) -> list:
    df = pd.read_csv(ruta, low_memory=False)
    print(f"📐 Shape: {df.shape[0]:,} × {df.shape[1]}")
    print(f"💾 Memoria: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")

    problemas = []
    for col in df.columns:
        pct_nulo = df[col].isnull().mean()
        if pct_nulo > 0.5:
            problemas.append(f"🔴 {col}: {pct_nulo:.0%} nulos — eliminar?")
        elif pct_nulo > 0.2:
            problemas.append(f"🟡 {col}: {pct_nulo:.0%} nulos — imputar")

    for col in df.select_dtypes(include=[np.number]).columns:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        outliers = ((df[col] < q1 - 3 * iqr) | (df[col] > q3 + 3 * iqr)).sum()
        if outliers:
            problemas.append(f"📍 {col}: {outliers} outliers extremos")

    if problemas:
        print(f"\n⚠️  Alertas ({len(problemas)}):")
        for p in problemas:
            print(f"  {p}")
    else:
        print("\n✅ Sin problemas detectados")

    return problemas


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else input("Ruta del CSV: ")
    perfil_rapido(ruta)
