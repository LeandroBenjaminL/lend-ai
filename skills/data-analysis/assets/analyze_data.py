# analyze_data.py

import pandas as pd


def analyze_data(filename):
    df = pd.read_csv(filename)
    print(f"Dataset con {df.shape[0]} filas y {df.shape[1]} columnas.")
    print("Tipos de datos:\n", df.dtypes)
    print("Valores nulos por columna:\n", df.isnull().sum())
    print("Estadísticas descriptivas:\n", df.describe())


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        analyze_data(sys.argv[1])
    else:
        print("Usar: python analyze_data.py <ruta_archivo_csv>")
