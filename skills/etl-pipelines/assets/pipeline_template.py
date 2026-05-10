"""
Pipeline ETL template — extraer, transformar, cargar.
USO: python pipeline.py [origen] [destino]
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
    handlers=[logging.FileHandler("pipeline.log"), logging.StreamHandler()],
)
log = logging.getLogger(__name__)


def extraer(ruta: str) -> pd.DataFrame:
    """E — Extracción de datos"""
    log.info(f"Extrayendo de {ruta}")
    df = pd.read_csv(ruta, low_memory=False)
    log.info(f"  → {len(df):,} registros")
    return df


def transformar(df: pd.DataFrame) -> pd.DataFrame:
    """T — Transformaciones"""
    log.info("Transformando...")
    df = df.copy()

    # --- Personalizar transformaciones acá ---
    # df['fecha'] = pd.to_datetime(df['fecha'])
    # df = df.drop_duplicates(subset=['id'])
    # df = df.dropna(subset=['columna_requerida'])

    log.info(f"  → {len(df):,} registros limpios")
    return df


def cargar(df: pd.DataFrame, destino: str) -> None:
    """L — Carga"""
    log.info(f"Cargando en {destino}")
    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(destino, index=False)
    log.info(f"  → {len(df):,} registros guardados")


def pipeline(origen: str, destino: str) -> None:
    inicio = datetime.now()
    df = extraer(origen)
    df = transformar(df)
    cargar(df, destino)
    delta = (datetime.now() - inicio).total_seconds()
    log.info(f"Pipeline completado en {delta:.1f}s")


if __name__ == "__main__":
    origen = sys.argv[1] if len(sys.argv) > 1 else "data/raw/datos.csv"
    destino = sys.argv[2] if len(sys.argv) > 2 else "data/processed/datos.parquet"
    pipeline(origen, destino)
