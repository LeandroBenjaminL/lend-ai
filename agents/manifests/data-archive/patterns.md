# Patterns: Data Archive Playbook

## Template: README de cierre

```markdown
# {Nombre del proyecto}

> **Cerrado:** {YYYY-MM-DD} | **Autor:** {nombre} | **Commit final:** `{hash}`

## ¿Qué queríamos descubrir?

{Una frase. La pregunta de negocio en lenguaje humano. Nada de jerga técnica.}

## Datos

| Campo | Detalle |
|-------|---------|
| Fuente | {API, CSV, BD, scrape...} |
| Tamaño | {N filas × M columnas} |
| Período | {YYYY-MM a YYYY-MM} |
| Método de acceso | {ruta relativa, query SQL, URL} |

## Enfoque

{2-3 párrafos contando qué hiciste y por qué. Nada de código — explicación conceptual.}

## Resultado principal

{El hallazgo más importante. Una frase contundente. Si hay métricas, van acá.}

## Estructura del proyecto

```
.
├── README.md              ← estás acá
├── requirements.txt       ← dependencias exactas
├── data/
│   ├── raw/               ← datos originales (nunca tocar)
│   └── processed/         ← datos limpios y transformados
├── notebooks/
│   ├── 01_eda.ipynb       ← exploración inicial
│   └── 02_modelado.ipynb  ← modelo final
├── src/                   ← código reutilizable
├── reports/               ← gráficos, reportes, dashboards
└── models/                ← modelos entrenados (.pkl, .joblib)
```

## Cómo reproducir

```bash
# 1. Clonar el repo
git clone {url}

# 2. Crear entorno
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 3. Ejecutar notebooks en orden
jupyter notebook notebooks/
# Abrir 01_eda.ipynb primero, después 02_modelado.ipynb
```

## Limitaciones

- {Lo que no pudimos hacer y por qué}
- {Sesgos conocidos en los datos}
- {Condiciones bajo las que el modelo deja de ser válido}

## Aprendizajes

- {Qué harías distinto la próxima}
- {Lecciones no obvias que descubriste en el camino}
```

## Estructura de archivos canónica

La estructura sagrada que todo proyecto de datos debería respetar:

```
{proyecto}/
├── README.md
├── requirements.txt
├── .gitignore              ← incluye data/raw/, .env, *.pyc
│
├── data/
│   ├── raw/                ← datos crudos. NUNCA se tocan, solo se leen.
│   └── processed/          ← datos transformados. Output de limpieza/feature engineering.
│
├── notebooks/              ← exploración y prototipado
│   ├── 01_{tarea}.ipynb
│   └── 02_{tarea}.ipynb
│
├── src/                    ← código Python reutilizable (funciones, clases)
│   ├── __init__.py
│   ├── data_loader.py
│   └── utils.py
│
├── reports/                ← gráficos, HTML, PDFs, dashboards exportados
│   └── fig/
│
├── models/                 ← artefactos de modelo (.pkl, .joblib, .h5, .onnx)
│
└── tests/                  ← tests unitarios (si los hay)
    └── test_utils.py
```

**Variaciones aceptables:**
- Proyectos chicos: podés omitir `src/` y `tests/` si todo está en notebooks.
- Proyectos orientados a pipeline: `data/` puede subdividirse en `raw/`, `interim/`, `processed/`.
- Proyectos con múltiples fuentes: meté subcarpetas descriptivas tipo `data/raw/sales/` y `data/raw/marketing/`.

## Checklist de archivo

Antes de dar el proyecto por cerrado, confirmás cada punto:

- [ ] `requirements.txt` o `environment.yml` actualizado y funcional
- [ ] Notebooks sin outputs (`nbstripout` pasado)
- [ ] `.gitignore` cubre: `data/raw/`, `.env`, `__pycache__/`, `*.pyc`, datasets grandes, `venv/`
- [ ] Datasets procesados guardados en Parquet (no CSV salvo que sea necesario)
- [ ] Ningún archivo temporal o de debug en el repo
- [ ] Ninguna API key, token o contraseña hardcodeada
- [ ] README de cierre escrito con el template de arriba
- [ ] Notebooks ejecutables de principio a fin (restart & run all sin errores)
- [ ] Commit final con mensaje descriptivo (qué se hizo, resultado clave)
- [ ] Push al remoto confirmado
- [ ] Hallazgos clave documentados en Engram

## Qué guardar y qué no

### Guardar

| Guardar | Formato | Razón |
|---------|---------|-------|
| Código fuente | `.py`, `.ipynb` | Reproducibilidad |
| Dependencias | `requirements.txt` | Entorno replicable |
| Datos procesados | `.parquet` | Eficiente, preserva tipos |
| Modelos entrenados | `.pkl`, `.joblib` | Evitar reentrenar |
| Reportes finales | `.html`, `.pdf` | Output de valor |
| Configuración | `.yaml`, `.toml` | Parámetros del proyecto |

### No guardar

| No guardar | Razón |
|------------|-------|
| Datos crudos en git | Pesan, no cambian, mejor storage externo |
| Notebooks con outputs | Hinchan diffs, no son código |
| Archivos temporales | `*.tmp`, `*.bak`, `*_v2_final_FINAL.csv` — basura pura |
| Datasets intermedios de prueba | Si no es el final, no va |
| Virtualenvs | `venv/`, `.conda/` — se regeneran con requirements.txt |
| API keys / secrets | Riesgo de seguridad |

## Metadata del proyecto

Para Engram, guardás este bloque de metadata:

```yaml
proyecto: {nombre}
fecha_cierre: {YYYY-MM-DD}
pregunta: {qué queríamos descubrir}
fuente_datos: {origen}
tamaño_dataset: {filas × columnas}
enfoque: {EDA | modelo ML | pipeline ETL | dashboard | reporte}
resultado_principal: {hallazgo en una frase}
repo: {url o path}
commit_final: {hash}
limitaciones: [{lista}]
aprendizajes: [{lista}]
estado: archivado
```

Este bloque lo usás para `mem_save` en Engram al finalizar el archivo.
