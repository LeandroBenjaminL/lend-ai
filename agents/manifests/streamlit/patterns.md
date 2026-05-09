# Patterns: Streamlit Cheat Sheet

## Configuración inicial — siempre al principio del script

```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Mi Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
```

## Estructura de layout

```python
st.title("📊 Dashboard de Ventas")
st.markdown("_Datos actualizados al 2024-01-15_")

# Sidebar: filtros
with st.sidebar:
    st.header("🔍 Filtros")
    categoria = st.selectbox("Categoría", df["categoria"].unique())
    rango = st.slider("Precio máximo", 0, 5000, 1000)

# Main: KPIs en columnas
col1, col2, col3 = st.columns(3)
col1.metric("Total Ventas", "$1.2M", delta="+12%")
col2.metric("Clientes", "843", delta="+5%")
col3.metric("Ticket Promedio", "$142", delta="-3%", delta_color="inverse")

# Tabs para secciones
tab1, tab2 = st.tabs(["📈 Gráficos", "📋 Datos"])
with tab1:
    fig = px.bar(df, x="producto", y="ventas")
    st.plotly_chart(fig, use_container_width=True)
with tab2:
    st.dataframe(df, use_container_width=True, hide_index=True)
```

## Caching — la diferencia entre rápido y abandonado

```python
# Cache para carga de datos (serializable)
@st.cache_data(ttl=3600)
def cargar_datos():
    return pd.read_csv("ventas.csv")

# Cache para recursos no serializables (DB, modelos)
@st.cache_resource
def conectar_db():
    return sqlite3.connect("database.db")

# Cache para resultados de filtros pesados
@st.cache_data
def filtrar_y_agregar(df, categoria, rango):
    return df[(df["cat"] == categoria) & (df["precio"] <= rango)].groupby("producto").sum()

# Limpiar cache manualmente
if st.button("🔄 Refrescar datos"):
    st.cache_data.clear()
    st.rerun()
```

## Widgets interactivos

```python
# Selectores
st.selectbox("Elegí una opción", opciones, key="select_1")
st.multiselect("Múltiples", opciones, default=[opciones[0]])
st.radio("Modo", ["Diario", "Semanal", "Mensual"], horizontal=True)

# Numéricos y fechas
st.slider("Rango de precios", 0, 10000, (1000, 5000))
st.number_input("Cantidad", min_value=1, max_value=100, value=10)
st.date_input("Fecha", value=pd.Timestamp.today())
st.date_input("Rango", value=[], key="date_range")  # retorna tupla si hay 2

# Acciones
st.button("Ejecutar análisis", key="btn_run")
st.download_button("⬇️ Descargar CSV", csv_data, "archivo.csv", "text/csv")
st.file_uploader("Subí tu archivo", type=["csv", "xlsx"], key="uploader")
```

## Visualización — lo que va en el main

```python
# Métricas (KPIs)
st.metric("Revenue", "$1.5M", delta="15%", delta_color="normal")
# delta_color: "normal" (verde=positivo), "inverse" (rojo=positivo), "off"

# Plotly — el estándar
fig = px.bar(df, x="mes", y="ventas", color="region", barmode="group")
st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(df, x="precio", y="cantidad", color="cat",
                  size="poblacion", hover_data=["nombre"],
                  trendline="ols")
st.plotly_chart(fig, use_container_width=True)

# Dataframe con formato
st.dataframe(
    df_filtrado.style.highlight_max(subset=["ventas"], color="lightgreen"),
    use_container_width=True,
    hide_index=True,
    height=400,
)

# Expander para contenido secundario
with st.expander("📊 Ver estadísticas descriptivas"):
    st.dataframe(df.describe())

# Mapas simples
st.map(df[["lat", "lon"]].dropna())  # requiere columnas lat/lon
```

## Session State — persistencia entre reruns

```python
# Inicializar
if "contador" not in st.session_state:
    st.session_state.contador = 0

# Leer y modificar
if st.button("Incrementar"):
    st.session_state.contador += 1

st.write(f"Valor: {st.session_state.contador}")

# Callback con widget
def on_select():
    st.session_state.filtro_aplicado = True

st.selectbox("Categoría", cats, key="cat_select", on_change=on_select)

# Borrar state
if st.button("Reset"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()
```

## File uploader — flujo completo

```python
archivo = st.file_uploader("📂 Subí tu CSV", type=["csv", "xlsx"])

if archivo is not None:
    ext = archivo.name.split(".")[-1]
    if ext == "csv":
        df = pd.read_csv(archivo)
    else:
        df = pd.read_excel(archivo)

    st.success(f"✅ Cargado: {archivo.name} — {len(df):,} filas × {len(df.columns)} columnas")

    # Mostrar preview
    st.dataframe(df.head(100), use_container_width=True)

    # Descarga del original procesado
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Descargar procesado", csv, "datos_procesados.csv", "text/csv")
```

## Despliegue — Dockerfile mínimo

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```toml
# .streamlit/config.toml
[server]
port = 8501
maxUploadSize = 200
enableCORS = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
font = "sans serif"
```

## Comandos rápidos

```bash
streamlit run app.py                    # ejecutar
streamlit run app.py --server.port 8080 # puerto custom
streamlit cache clear                   # limpiar todo el cache
streamlit hello                         # demo app
```

## Elección de elemento según necesidad

| Querés mostrar... | Usá |
|---|---|
| KPIs resumidos | `st.metric()` |
| Tabla interactiva | `st.dataframe()` |
| Gráfico interactivo | `st.plotly_chart()` |
| Gráfico estático | `st.pyplot()` |
| Mapa de puntos | `st.map()` |
| Texto formateado | `st.markdown()` |
| Progreso de operación | `st.progress()` / `st.spinner()` |
| Feedback al usuario | `st.success()` / `st.warning()` / `st.error()` / `st.info()` |
| Contenido secundario | `st.expander()` |
| Secciones separadas | `st.tabs()` |
| Confirmación | `st.checkbox()` / `st.button()` |

## Reglas de oro

1. **`st.cache_data` para toda carga de datos.** Sin excepción. Si los datos pesan más de 10MB, cacheá sí o sí.
2. **Sidebar = filtros. Main = contenido.** No mezcles. El usuario tiene que saber dónde buscar.
3. **Plotly + `use_container_width=True` siempre.** Matplotlib solo si necesitás publicar en papel.
4. **`key=` explícito en todo widget.** Si no lo ponés, Streamlit asigna por orden y se rompe al refactorizar.
5. **Spinner en operaciones lentas.** `with st.spinner("Cargando..."):` le da al usuario la certeza de que algo está pasando.
6. **Menos es más.** Si tu app tiene 15 filtros y 8 gráficos, probablemente estás haciendo 3 apps distintas.
7. **Probá en mobile.** `layout="wide"` no es excusa para ignorar pantallas chicas. `use_container_width=True` ayuda.
8. **Secrets a `.streamlit/secrets.toml`.** Nunca hardcodees API keys, contraseñas ni tokens.
