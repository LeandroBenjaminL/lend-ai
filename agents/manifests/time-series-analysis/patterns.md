# Patterns: Time Series Cheat Sheet

## Preparación e indexado

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from prophet import Prophet
from sklearn.model_selection import TimeSeriesSplit
```

```python
# Parsear e indexar
df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')
df = df.set_index('fecha').sort_index()

# Verificar frecuencia
print(pd.infer_freq(df.index))

# Detectar gaps
gaps = df.asfreq('D').isnull().sum()
```

## Resampleo y ventanas

| Patrón | Código |
|---|---|
| Resample diario → mensual | `df.resample('ME').sum()` |
| Resample con múltiples aggs | `df.resample('W').agg({'ventas': 'sum', 'precio': 'mean'})` |
| Media móvil 7 días | `df['target'].rolling(7).mean()` |
| Media móvil centrada | `df['target'].rolling(7, center=True).mean()` |
| Desviación estándar móvil | `df['target'].rolling(30).std()` |
| Expansión acumulativa | `df['target'].expanding().mean()` |
| Rellenar gaps con frecuencia | `df.asfreq('D', fill_value=0)` |

## Feature engineering temporal

```python
# Componentes de fecha
df['año']        = df.index.year
df['mes']        = df.index.month
df['dia']        = df.index.day
df['dia_semana'] = df.index.dayofweek       # 0=lunes, 6=domingo
df['trimestre']  = df.index.quarter
df['dia_año']    = df.index.dayofyear
df['semana_año'] = df.index.isocalendar().week
df['es_finde']   = df['dia_semana'].isin([5, 6]).astype(int)
df['es_principio_mes'] = (df.index.day <= 7).astype(int)

# Lags y diferencias
df['lag_1']  = df['target'].shift(1)
df['lag_7']  = df['target'].shift(7)
df['lag_30'] = df['target'].shift(30)
df['diff_1']  = df['target'].diff(1)
df['diff_7']  = df['target'].diff(7)
df['pct_change'] = df['target'].pct_change()
```

## Test de estacionariedad

```python
# ADF Test
result = adfuller(df['target'].dropna())
print(f'ADF Statistic: {result[0]:.4f}')
print(f'p-value: {result[1]:.4f}')
print(f'Critical Values: {result[4]}')
# p-value < 0.05 → rechazar H0 → la serie ES estacionaria

# Si no es estacionaria, diferenciar
df['target_diff'] = df['target'].diff().dropna()

# KPSS — complemento (H0: es estacionaria, al revés que ADF)
from statsmodels.tsa.stattools import kpss
stat, pval, _, crit = kpss(df['target'].dropna(), regression='c')
```

## Descomposición

```python
# Descomposición aditiva (amplitud estacional constante)
decomp = seasonal_decompose(df['target'].dropna(), model='additive', period=12)
trend = decomp.trend
seasonal = decomp.seasonal
residual = decomp.resid

# Descomposición multiplicativa (amplitud crece con tendencia)
decomp = seasonal_decompose(df['target'].dropna(), model='multiplicative', period=12)

# STL — más robusto con estacionalidad cambiante
from statsmodels.tsa.seasonal import STL
stl = STL(df['target'].dropna(), period=12, seasonal=7)
result = stl.fit()
result.plot()
```

## ACF / PACF

```python
# Siempre sobre la serie estacionaria (diferenciada si aplica)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
plot_acf(df['target_diff'].dropna(), lags=40, ax=ax1)
plot_pacf(df['target_diff'].dropna(), lags=40, ax=ax2)
plt.tight_layout()
```

**Interpretación rápida:**
| Patrón ACF/PACF | Modelo sugerido |
|---|---|
| ACF corta brusco en q, PACF decae | MA(q) |
| PACF corta brusco en p, ACF decae | AR(p) |
| Ambos decaen lentamente | ARMA(p,q) — diferenciar más |
| Picos en lags estacionales (s, 2s) | Agregar componente estacional → SARIMA |

## Modelos

### ARIMA

```python
model = ARIMA(train['target'], order=(p, d, q))
fitted = model.fit()
print(fitted.summary())
forecast = fitted.forecast(steps=30)
```

### SARIMA

```python
# (p,d,q) no estacional × (P,D,Q,s) estacional
model = SARIMAX(train['target'],
                order=(1, 1, 1),
                seasonal_order=(1, 1, 1, 12))  # s=12 para mensual
fitted = model.fit()
forecast = fitted.get_forecast(steps=12)
ci = forecast.conf_int()  # intervalos de confianza
```

### Exponential Smoothing (Holt-Winters)

```python
model = ExponentialSmoothing(
    train['target'],
    trend='add',              # 'add' o 'mul'
    seasonal='add',           # 'add' o 'mul'
    seasonal_periods=12
)
fitted = model.fit()
forecast = fitted.forecast(steps=12)
```

### Prophet

```python
df_prophet = df.reset_index()[['fecha', 'target']].rename(
    columns={'fecha': 'ds', 'target': 'y'}
)

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    changepoint_prior_scale=0.05
)
# Agregar feriados si aplica
model.add_country_holidays(country_name='AR')
model.fit(df_prophet)

future = model.make_future_dataframe(periods=90)
forecast = model.predict(future)
model.plot(forecast)
model.plot_components(forecast)
```

## Train / Test split TEMPORAL (sagrado)

```python
# ✅ CORRECTO: split cronológico
train = df[:'2024-06-30']
test  = df['2024-07-01':]

# ✅ CORRECTO: TimeSeriesSplit de sklearn
tscv = TimeSeriesSplit(n_splits=5)
for train_idx, test_idx in tscv.split(df):
    train, test = df.iloc[train_idx], df.iloc[test_idx]
    # entrenar y evaluar...

# ❌ NUNCA hagas esto con series temporales:
# train_test_split(df, shuffle=True)  ← EL TIEMPO NO SE SHUFFLEA, CHE.

# Para modelos que no dependen del orden (boosting con lags ya creados):
# split temporal con los índices, no aleatorio.
```

## Métricas y validación

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error

def forecast_metrics(actual, predicted):
    mae  = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    return {'MAE': mae, 'RMSE': rmse, 'MAPE': mape}

# Análisis de residuos
residuals = fitted.resid
plot_acf(residuals.dropna(), lags=30)   # deben ser ruido blanco
residuals.plot(kind='hist', bins=30)    # centrados en 0, normales
```

## Checklist previa a devolver

- [ ] El índice es `DatetimeIndex` monotónico creciente.
- [ ] La frecuencia está definida explícitamente.
- [ ] No hay valores futuros filtrándose al entrenamiento.
- [ ] El modelo se evaluó con backtesting temporal (split cronológico).
- [ ] Los residuos no muestran autocorrelación significativa.
- [ ] El forecast incluye intervalos de confianza.
- [ ] Si MAPE > 20%, se justificó por qué.
