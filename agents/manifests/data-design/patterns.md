# Patterns: Decisiones de Diseño Analítico

> _Esto no es código. Es criterio. Acá no se elige una library — se elige un camino._

## Tabla de decisión: qué enfoque según el tipo de problema

| Tipo de problema | Pregunta típica | Enfoque | Método sugerido | Herramienta base |
|-----------------|----------------|---------|----------------|-----------------|
| "¿Qué pasó?" | Caída de ventas, picos de tráfico | **Descriptivo** | Agregaciones, distribuciones, visualizaciones | Pandas + Seaborn |
| "¿Por qué pasó?" | Atribución de churn, root cause de errores | **Diagnóstico** | Segmentación, correlaciones, test de hipótesis | Pandas + SciPy |
| "¿Qué va a pasar?" | Forecast de demanda, riesgo de default | **Predictivo** | Regresión, clasificación, time series | Scikit-learn / Prophet |
| "¿Qué deberíamos hacer?" | Optimización de precios, asignación de recursos | **Prescriptivo** | Optimización, simulación, what-if | SciPy + Streamlit |
| "¿Cómo está la calidad?" | Auditoría de datos, linaje, gobierno | **Descriptivo** | Profiling, reglas de validación | data-profiling + data-validation |
| "¿Qué mirar primero?" | Datos nuevos, exploración inicial | **Descriptivo** | ydata-profiling, Sweetviz | data-profiling |
| "¿Es A mejor que B?" | A/B test, comparación de treatments | **Diagnóstico** | t-test, chi-cuadrado, bootstrap | SciPy + statsmodels |
| "¿Qué pasa en el tiempo?" | Tendencias, estacionalidad, anomalías | **Descriptivo → Predictivo** | Descomposición, forecasting, detección de anomalías | statsmodels / Prophet |
| "¿Se parecen estos grupos?" | Segmentación de clientes, clustering | **Descriptivo** | K-means, DBSCAN, PCA | Scikit-learn + Seaborn |

**Principio fundamental:** Si podés responder la pregunta con una tabla y un gráfico, no modeles. Si podés modelar con regresión lineal, no uses XGBoost. Si XGBoost alcanza, no toques deep learning.

## Comparativa de herramientas

### Procesamiento de datos

| Dimensión | Pandas | Polars | SQL | Spark |
|-----------|--------|--------|-----|-------|
| Volumen máximo cómodo | ~1M filas | ~50M filas | ~100M filas | TBs |
| Curva de aprendizaje | Baja | Media | Media | Alta |
| Velocidad en datos chicos | Media | Alta | Alta | Muy baja (overhead) |
| Velocidad en datos grandes | Lenta (OOM) | Buena | Excelente | Excelente |
| Ecosistema | Enorme | Creciente | Universal | Grande |
| Debugging | Fácil (notebook) | Medio | Medio | Difícil |
| Setup | `pip install pandas` | `pip install polars` | Un servidor | Un cluster |
| Mejor para | Prototipado, exploración | Pipelines rápidos, lazy eval | Agregaciones, joins, ETL | Datos masivos, ETL distribuido |

### Machine Learning

| Dimensión | Scikit-learn | LightGBM / XGBoost | TensorFlow / PyTorch | Prophet |
|-----------|-------------|---------------------|----------------------|---------|
| Tipo de datos | Tabulares | Tabulares | Imágenes, texto, audio | Series temporales |
| Volumen ideal | <1M filas | <10M filas | >100K muestras | >100 puntos |
| Explicabilidad | Alta (coeficientes) | Media (SHAP) | Baja (black box) | Media (componentes) |
| Tiempo de entrenamiento | Segundos | Minutos | Horas/días | Segundos |
| Hiperparámetros | Pocos | Muchos | Infinitos | Pocos |
| Mejor para | Baseline, inferencia | Competir, producción | Dominios especializados | Forecast con estacionalidad |

### Visualización

| Dimensión | Matplotlib | Seaborn | Plotly | Streamlit |
|-----------|-----------|---------|--------|-----------|
| Tipo | Estático | Estático | Interactivo | Dashboard |
| Curva | Alta | Baja | Media | Baja |
| Customización | Total | Limitada | Alta | Limitada |
| Sharing | Imagen | Imagen | HTML | Web app |
| Mejor para | Paper, reporte | EDA rápido | Data apps | Demos, stakeholders |

## Tradeoffs: la matriz de decisiones

### Simplicidad vs Precisión

| Elegí SIMPLICIDAD cuando... | Elegí PRECISIÓN cuando... |
|---------------------------|--------------------------|
| El stakeholder necesita entender el modelo | 1% de accuracy extra vale millones |
| El modelo va a ser mantenido por un equipo junior | Estás compitiendo (Kaggle, licitación) |
| Los datos cambian rápido y reentrenás seguido | El modelo corre offline sin intervención humana |
| Estás en fase de prototipado / MVP | Ya pasaste la fase de validación de concepto |

**Regla:** Empezá siempre por el modelo más simple que responda la pregunta. Agregá complejidad solo cuando el modelo simple **demostrablemente** no alcanza.

### Velocidad vs Robustez

| Elegí VELOCIDAD cuando... | Elegí ROBUSTEZ cuando... |
|-------------------------|------------------------|
| El stakeholder necesita una respuesta en horas | El análisis va a producción |
| Es un análisis ad-hoc que no se repite | Se corre semanalmente y alimenta decisiones |
| Estás validando una hipótesis antes de invertir más tiempo | Hay compliance o regulaciones de por medio |
| Los datos son estables y de calidad conocida | Los datos vienen de fuentes inestables |

**Estrategia híbrida común:** Iteración rápida con muestra del 10% → validar hipótesis → si funciona, correr sobre dataset completo.

### Flexibilidad vs Mantenibilidad

| Elegí FLEXIBILIDAD cuando... | Elegí MANTENIBILIDAD cuando... |
|----------------------------|------------------------------|
| Es un análisis exploratorio | El pipeline va a correr por meses/años |
| El dominio del problema es nuevo para el equipo | Hay un equipo estable que mantiene el código |
| Los requerimientos cambian semana a semana | Hay SLAs de disponibilidad |
| Una sola persona ejecuta el análisis | Varias personas tocan el mismo pipeline |

**Regla:** Si el análisis se corre una vez y se tira, priorizá velocidad y flexibilidad. Si se corre todos los meses para un reporte que ve el directorio, priorizá robustez y mantenibilidad.

### Explicabilidad vs Performance

| Elegí EXPLICABILIDAD cuando... | Elegí PERFORMANCE cuando... |
|------------------------------|---------------------------|
| Decisiones reguladas (crédito, salud, RRHH) | Recomendaciones de contenido |
| El usuario final necesita confiar en el output | El output es interno y automatizado |
| Estás diagnosticando, no prediciendo | Predicción masiva en batch |
| Puede haber sesgo y necesitás auditarlo | El costo de un error es bajo |

**Principio:** Si el modelo decide sobre personas (crédito, contratación, salud), la explicabilidad NO es negociable.

## Checklist pre-implementación

Antes de pasarle el plan al orchestrator para que delegue a los agentes técnicos, verificás:

- [ ] El enfoque (descriptivo/diagnóstico/predictivo/prescriptivo) está justificado por escrito
- [ ] Evalué al menos 3 alternativas de método/herramienta y documenté por qué elegí esta
- [ ] La herramienta elegida es adecuada para el volumen real de datos (validado con data-profiling)
- [ ] La arquitectura del pipeline está completa: cada etapa tiene input, transformación, output y validación
- [ ] La estrategia de validación es adecuada al tipo de análisis (no usás cross-validation para series temporales)
- [ ] El plan de implementación tiene pasos atómicos con criterios de éxito medibles
- [ ] Los riesgos de alto impacto tienen plan de contingencia
- [ ] Las opciones descartadas están documentadas con su razón de descarte
- [ ] El output final está alineado con el nivel técnico de quien lo consume
- [ ] El stakeholder puede tomar una decisión concreta con los resultados de este análisis

## Anti-patrones: lo que NUNCA hacés

- **No elegís herramienta por moda.** _"Porque todo el mundo usa Spark"_ no es una razón. Justificá con volumen, latencia, o ecosistema.
- **No asumís que más complejo = mejor.** Un 87% de accuracy con un modelo que nadie entiende es peor que un 85% con uno que todo el equipo puede explicar.
- **No diseñás sin saber qué datos hay.** Si data-profiling no corrió todavía, no diseñás. Punto.
- **No delegás la decisión de método al que implementa.** "El que modele que elija" es abdicar de tu responsabilidad. Vos elegís el camino, ellos lo ejecutan.
- **No ocultás los tradeoffs.** Si elegiste simplicidad sobre precisión, lo decís explícitamente y explicás por qué.
- **No sobre-diseñás.** Para un análisis ad-hoc de 500 filas, no necesitás un pipeline con CI/CD. Pandas en un notebook alcanza.
- **No ignorás al stakeholder.** Si el diseño es técnicamente perfecto pero el output es un notebook y el stakeholder solo mira PDFs, el diseño falló.

## Métricas de éxito del diseño

Un buen diseño se mide antes de escribir una línea de código:

| Métrica | Buen diseño | Mal diseño |
|---------|------------|-----------|
| Claridad | Cualquier persona del equipo puede leerlo y entender qué se va a hacer | Solo el que lo escribió lo entiende |
| Justificación | Cada decisión tiene un "por qué" documentado | Decisiones arbitrarias sin razonamiento |
| Realismo | Las herramientas y volúmenes están validados con datos reales | Suposiciones sobre el tamaño de datos sin verificar |
| Accionabilidad | Cada paso del plan puede ejecutarlo un agente sin volver a preguntar | El plan requiere interpretación constante |
| Escalabilidad | Si los datos crecen 10x, el diseño tiene un upgrade path claro | El diseño colapsa si los datos crecen |
