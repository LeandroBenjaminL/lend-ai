---
name: streamlit
description: >
  Creación de aplicaciones interactivas para análisis de datos con Streamlit.
  Trigger: Cuando necesitás crear dashboards, apps web interactivas, o visualizar datos con Streamlit.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "3.0"
  model_tier: T2-fast
---

# Skill: streamlit

Streamlit te permite convertir un script de Python en una app web interactiva **en minutos**. No necesitas saber HTML, CSS ni JavaScript. Es la herramienta ideal para compartir análisis con gente que no quiere (o no puede) correr un notebook.

La filosofía de Streamlit es "interactividad sin callbacks": cada vez que el usuario toca un widget, el script se ejecuta de arriba a abajo de nuevo. Eso puede sonar ineficiente, pero es lo que lo hace tan simple — no hay que manejar estado ni eventos.

## Trigger

- Querés compartir una visualización interactiva con alguien que no tiene Python
- Necesitás filtros, selectores y gráficos que el usuario pueda explorar
- Estás prototipando un dashboard que después podría pasar a producción
- Te cansaste de exportar PNGs y mandarlos por Slack

## Workflow

### 1. Estructura básica
Definí configuración de página, cargá datos con `@st.cache_data` y armá el layout. Streamlit ejecuta el script de arriba a abajo, así que el orden importa.

### 2. Agregá controles en la sidebar
Los filtros van en la sidebar (consistencia). Usá `with st.sidebar:` para agruparlos. El usuario sabe que siempre va a encontrar los controles ahí.

### 3. Layout con columnas y tabs
Distribuí KPIs, gráficos y tablas en columnas para pantalla ancha. Usá tabs para separar vistas (resumen, detalle, estadísticas).

### 4. Performance
Usá `@st.cache_data` para datos que no cambian entre interacciones. Para datasets grandes, mostrá solo `head()` y ofrecé descarga del CSV completo.

## Patrones y ejemplos

### 1. Estructura base con caché — performance desde el arranque

```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📊 Dashboard de Ventas")

@st.cache_data
def cargar_datos():
    # cache_data evita recargar el CSV en cada interacción
    return pd.read_csv('ventas.csv')

df = cargar_datos()
```

**¿Por qué `@st.cache_data`?**: Sin caché, cada vez que el usuario toca un slider Streamlit relee el archivo. Con caché, lo lee una vez y reusa. Es la diferencia entre una app que tarda 0.2s y una que tarda 5s por interacción.

### 2. Sidebar + filtros — interactividad limpia

```python
with st.sidebar:
    st.header("Filtros")
    categoria = st.selectbox("Categoría", df['categoria'].unique())
    rango_precio = st.slider("Precio máximo", 0, int(df['precio'].max()), 100)
    fecha_ini, fecha_fin = st.date_input("Rango de fechas", [])

# Filtrar el DataFrame según los controles
df_filtrado = df[
    (df['categoria'] == categoria) &
    (df['precio'] <= rango_precio)
]
# Los filtros se re-aplican en cada interacción — simple y directo
```

### 3. KPIs con métricas y layout en columnas

```python
col1, col2 = st.columns(2)

with col1:
    st.subheader("Métrica principal")
    st.metric("Total ventas", f"${df_filtrado['total'].sum():,.0f}", delta="+12%")

with col2:
    st.subheader("Promedio")
    st.metric("Ticket promedio", f"${df_filtrado['total'].mean():,.0f}")

# Tabs para organizar contenido sin scroll infinito
tab1, tab2, tab3 = st.tabs(["Gráfico", "Tabla", "Estadísticas"])
with tab1:
    fig = px.bar(df_filtrado, x='producto', y='total')
    st.plotly_chart(fig, use_container_width=True)
with tab2:
    st.dataframe(df_filtrado, use_container_width=True)
with tab3:
    st.dataframe(df_filtrado.describe(), use_container_width=True)
```

**¿Por qué `st.metric()`?**: Muestra valor + delta en un formato visual que comunica tendencia de un vistazo. Ideal para KPIs en la parte superior del dashboard.

### 4. App de análisis exploratorio — CSV genérico

```python
st.title("Analizador de Datos")

archivo = st.file_uploader("Subí tu CSV", type="csv")
if archivo:
    df = pd.read_csv(archivo)
    st.dataframe(df.head(100))

    col_num = df.select_dtypes('number').columns
    x = st.selectbox("Eje X", col_num)
    y = st.selectbox("Eje Y", col_num)
    color = st.selectbox("Color", ['None'] + list(df.columns))

    kwargs = dict(x=x, y=y)
    if color != 'None':
        kwargs['color'] = color

    fig = px.scatter(df, **kwargs)
    st.plotly_chart(fig, use_container_width=True)
```

Esta app sirve para cualquier CSV. El usuario sube sus datos y explora. Es el ejemplo perfecto de por qué Streamlit brilla: una herramienta genérica que se adapta al dataset del usuario.

## Alternativas

| Herramienta | Enfoque | Cuándo conviene |
|-------------|---------|----------------|
| **Streamlit** | Script → app, minimalista | Dashboards rápidos, prototipos, apps de datos |
| **Dash (Plotly)** | App con callbacks, más control | Apps complejas, producción, múltiples páginas |
| **Panel (Holoviz)** | Dashboards desde notebooks | Cuando ya tenés el análisis en Jupyter |
| **Gradio** | Demos de ML rápida | Prototipos de modelos, demos para stakeholders |
| **Voilà** | Notebook → dashboard | Cuando querés compartir notebooks como apps sin tocar código |

**Recomendación**: Streamlit para el 90% de los casos. Dash si necesitás una app compleja con múltiples páginas y estado compartido. Gradio si es un demo de modelo ML.

## Anti-patrones

- ❌ **No usar `@st.cache_data`** — cada interacción relee todo, la app se arrastra
- ❌ **Poner widgets en el cuerpo principal** — la sidebar es el lugar standard para controles
- ❌ **Gráficos sin `use_container_width=True`** — en pantallas grandes quedan chicos, en pantallas chicas se rompen
- ❌ **Mostrar 10k filas en `st.dataframe`** — el browser se cuelga. Mostrá `head()` u ofrecé descarga
- ❌ **Olvidar `st.stop()` o `return` cuando no hay datos** — la app sigue ejecutándose y tirando errores si el DataFrame está vacío
- ❌ **No separar la lógica de negocio de la UI** — mezclar todo en `app.py` hace imposible testear y mantener
