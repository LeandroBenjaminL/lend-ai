# Workflow: Time Series Analysis

## Flujo principal

```
Orchestrator → [1. Parsear] → [2. Resamplear] → [3. Visualizar] → [4. Test estacionariedad] → [5. Descomponer] → [6. ACF/PACF] → [7. Elegir modelo] → [8. Validar con backtesting] → [9. Forecast + CI] → Orchestrator
```

## Paso a paso

### 1. Parsear fechas e indexar
- `pd.to_datetime()` con `format` explícito si se conoce. Siempre.
- Setear la columna de fecha como índice: `df.set_index('fecha').sort_index()`.
- Verificar que el índice es monotónico. Si tiene huecos, detectarlos y reportarlos.
- Identificar frecuencia natural: `pd.infer_freq(df.index)`. Si no la detecta, preguntar o deducir de los datos.

### 2. Resamplear a la frecuencia necesaria
- Definir la frecuencia objetivo: diaria (`'D'`), semanal (`'W'`), mensual (`'ME'`), trimestral (`'QE'`).
- Elegir función de agregación según el dominio: `sum` para ventas, `mean` para temperatura, `last` para precios de cierre.
- `df.resample('ME')['target'].sum()`. Si hay gaps, `asfreq()` para hacerlos explícitos.
- Si la frecuencia original es mayor que la objetivo, interpolar con criterio (linear, spline, time). No interpolar a lo loco sin justificar.

### 3. Visualizar tendencia y estacionalidad
- Gráfico de línea crudo: `df['target'].plot()`.
- Media móvil para suavizar tendencia: `df['target'].rolling(30).mean()`.
- Boxplots por mes/día de la semana para detectar patrones estacionales.
- Heatmap año × mes si hay varios años de datos.
- Si algo no se ve a ojo, no es buen momento para modelar.

### 4. Test de estacionariedad (ADF)
- `adfuller(df['target'].dropna())`.
- Interpretar: p-value < 0.05 → estacionaria. Si no, diferenciar.
- `df['target_diff'] = df['target'].diff().dropna()` y re-testear.
- Si requiere 2 diferencias (`d=2`), considerá si tiene sentido o si hay que transformar (log, raíz cuadrada).
- KPSS como test complementario si ADF es ambiguo.

### 5. Descomposición
- `seasonal_decompose(df['target'], model='additive'|'multiplicative', period=<freq>)`.
  - **Aditivo** si la amplitud estacional es constante.
  - **Multiplicativo** si la amplitud crece/decrece con la tendencia.
- Analizar visualmente: tendencia, estacional, residual.
- Si el residuo muestra patrones, la descomposición no capturó todo → revisar el período o probar STL (`STL` de statsmodels).

### 6. Análisis de autocorrelación (ACF/PACF)
- `plot_acf(df['target_diff'], lags=40)` para ver autocorrelación.
- `plot_pacf(df['target_diff'], lags=40)` para identificar orden del AR.
- Reglas heurísticas clásicas para ARIMA:
  - PACF con corte brusco en lag `p` → AR(p).
  - ACF con corte brusco en lag `q` → MA(q).
  - Ambos decaen lentamente → ARMA, posiblemente necesitás diferenciar de nuevo.
- Si hay picos en lags estacionales (7, 14, 21... o 12, 24...), necesitás componente estacional → SARIMA.

### 7. Elegir modelo
- **Datos estacionarios, sin estacionalidad fuerte, pocos parámetros**: `ARIMA(p,d,q)`.
- **Con estacionalidad clara**: `SARIMA(p,d,q)(P,D,Q,s)` donde `s` es el período estacional.
- **Con changepoints, feriados, múltiples estacionalidades**: `Prophet`.
- **Serie suave, pocos datos, forecast corto**: `ExponentialSmoothing` (Holt-Winters).
- **Serie compleja con features exógenas**: `SARIMAX` o Prophet con regresores adicionales.
- Documentar por qué elegiste ese modelo. No es una decisión automática.

### 8. Validar con backtesting temporal
- **NUNCA usar train/test split aleatorio.** El tiempo no es aleatorio.
- Split cronológico:
  ```python
  train = df[:'2024-06-30']
  test  = df['2024-07-01':]
  ```
- O `TimeSeriesSplit(n_splits=5)` de sklearn para validación cruzada temporal.
- Métricas: MAE, RMSE, MAPE. Si MAPE > 20%, el modelo probablemente es malo para el negocio.
- Analizar residuos: deben ser ruido blanco (sin autocorrelación, media ≈ 0, varianza constante).
- `plot_acf(residuals)` para confirmar que no quedó estructura sin modelar.

### 9. Forecast + intervalos de confianza
- Generar forecast para el horizonte pedido.
- Siempre incluir intervalos de confianza (típicamente 80% y 95%).
- Graficar: datos históricos + forecast + banda de confianza.
- Si el forecast se va al infinito o las bandas explotan → el modelo no es confiable, reportalo.
- Devolver: fechas, valor pronosticado, límite inferior, límite superior.
