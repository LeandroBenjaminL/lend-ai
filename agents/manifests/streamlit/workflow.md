# Workflow: Streamlit App Development

## Flujo principal

```
Orchestrator → [1. Definir qué quiere ver el usuario] → [2. Estructurar la app] → [3. Cargar datos con cache] → [4. Agregar controles] → [5. Crear visualizaciones reactivas] → [6. Optimizar cache] → [7. Desplegar] → Orchestrator
```

## Paso a paso

### 1. Definir qué quiere ver el usuario
Leer el prompt completo. Identificar: ¿quién es el usuario (técnico, ejecutivo, operativo)? ¿Qué decisión tiene que tomar con estos datos? ¿KPIs principales, exploración libre, o reporte estructurado? Definir el objetivo en una frase. Si no podés resumirlo, no arranques a codear.

### 2. Estructurar la app (sidebar vs main)
- `st.set_page_config(page_title="...", layout="wide")` siempre al principio del script.
- Sidebar: filtros globales, selección de fechas, selectbox de categorías. Todo lo que el usuario ajusta para explorar.
- Main area: KPIs en `st.metrics` arriba, gráficos grandes debajo, tablas al final.
- Si la app tiene secciones lógicas, usá `st.tabs()` para no saturar el scroll.
- Layout con `st.columns()` para mostrar métricas lado a lado o gráficos complementarios.

### 3. Cargar datos con cache
```python
@st.cache_data(ttl=3600)  # TTL en segundos si los datos cambian periódicamente
def cargar_datos():
    return pd.read_csv('datos.csv')
```
- Elegir `st.cache_data` para DataFrames, listas, dicts. `st.cache_resource` para conexiones DB y modelos.
- Si el usuario sube archivo (`st.file_uploader`), no necesita cache porque ya está en memoria. Pero si procesás ese archivo con operaciones pesadas, cacheá el resultado.
- Mostrar un spinner mientras carga: `with st.spinner("Cargando datos..."):`.

### 4. Agregar controles (selectbox, slider, date picker)
- Agrupar controles en el sidebar con `with st.sidebar:`.
- `st.selectbox` para categorías, `st.multiselect` para filtros múltiples.
- `st.slider` para rangos numéricos o de fechas. Si es fecha, preferí `st.date_input`.
- Cada widget tiene un `key=` único para controlar su estado. Sin key, Streamlit asigna uno por posición y puede romperse si cambiás el orden.
- Los widgets retornan el valor seleccionado. Guardalo en variables y usalo para filtrar.

### 5. Crear visualizaciones reactivas
- Filtrar el DataFrame con los valores de los widgets. Este filtro se ejecuta en cada rerun.
- `st.metric(label, value, delta)` para KPIs. Si tenés más de 3, usá columns.
- `st.plotly_chart(fig, use_container_width=True)` para gráficos. Preferí Plotly sobre Matplotlib por interactividad.
- `st.dataframe(df, use_container_width=True, hide_index=True)` para tablas. Si son muchas filas, mostrá solo head y ofrecé descarga.
- Para mapas: `st.map()` si es simple, `st.pydeck_chart()` si necesitás capas complejas.

### 6. Optimizar con st.cache_data
- Identificar operaciones pesadas: filtros complejos, agregaciones, joins, transformaciones.
- Cachear resultados intermedios con `@st.cache_data`.
- Si la app es lenta: revisar que los datos no se recalculen en cada rerun. `st.cache_data` es tu primera herramienta.
- `st.session_state` para valores que deben persistir entre reruns sin recalcular (ej. estado de un formulario, paso actual de un wizard).
- Para apps con datos grandes, considerar `st.cache_data` con función de hash personalizada para invalidar solo cuando ciertas columnas cambian.

### 7. Desplegar
- Streamlit Cloud: `streamlit run app.py` local, pushear a GitHub, conectar repo.
- Docker: crear `Dockerfile` con `FROM python:3.11-slim`, `pip install streamlit`, `EXPOSE 8501`, `CMD ["streamlit", "run", "app.py"]`.
- Secrets: usar `st.secrets["db_password"]` en vez de hardcodear. En local va en `.streamlit/secrets.toml`, en Cloud se configura desde el dashboard.
- `.streamlit/config.toml` para configurar theme, puerto, CORS, max upload size.
