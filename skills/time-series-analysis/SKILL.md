---
name: time-series-analysis
description: >
  Análisis de series temporales con Pandas, Statsmodels y Prophet.
  Trigger: Cuando trabajás con datos de fecha/hora, tendencias, estacionalidad, forecasting, o series de tiempo.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "1.1"
  model_tier: T3-balanced
---

# Skill: time-series-analysis

Análisis de series temporales: tendencias, estacionalidad, forecasting y feature engineering temporal.

## Trigger

Cargá esta skill cuando:
- Tus datos tienen una dimensión temporal (fechas, horas, timestamps)
- Necesitás analizar tendencias, estacionalidad y ciclos
- Querés hacer forecasting de valores futuros
- Trabajás con remuestreo, lag features o rolling windows

## Por qué las series temporales son distintas

En ML clásico asumimos que las observaciones son independientes. En series temporales no: el valor de hoy depende del valor de ayer. Ignorar esta estructura te lleva a modelos que hacen trampa (leakage temporal) y pronósticos inútiles.

## 1. Preparación de la serie

```python
import pandas as pd

df['fecha'] = pd.to_datetime(df['fecha'])
df = df.set_index('fecha').sort_index()

# Remuestreo — siempre verificá que el índice sea regular
df_diario = df.resample('D').sum()
df_semanal = df.resample('W').mean()
df_mensual = df.resample('ME').sum()

# Rolling windows
df['media_movil_7d'] = df['valor'].rolling(window=7).mean()
df['std_movil_7d'] = df['valor'].rolling(window=7).std()
```

**Por qué remuestrear**: muchas series vienen con frecuencia irregular. Remuestrear a frecuencia fija es necesario para modelos como SARIMA o Prophet.

## 2. Feature engineering temporal

```python
df['año'] = df.index.year
df['mes'] = df.index.month
df['dia_semana'] = df.index.dayofweek
df['es_fin_de_semana'] = df['dia_semana'].isin([5, 6]).astype(int)
df['dia_del_año'] = df.index.dayofyear
df['lag_1'] = df['valor'].shift(1)
df['lag_7'] = df['valor'].shift(7)
```

**Por qué lags**: un modelo sin lags no ve el pasado. Con `shift(1)` le das el valor del día anterior. Con `shift(7)` le das el de la semana pasada (útil para estacionalidad semanal).

## 3. Descomposición de la serie

```python
from statsmodels.tsa.seasonal import seasonal_decompose

result = seasonal_decompose(df['valor'], model='additive', period=30)
result.trend.plot()
result.seasonal.plot()
result.resid.plot()
```

**Aditivo vs multiplicativo**: aditivo cuando la amplitud de la estacionalidad es constante (`tendencia + estacionalidad + residuo`). Multiplicativo cuando crece con la tendencia (`tendencia × estacionalidad × residuo`).

## 4. Forecasting con Prophet

```python
from prophet import Prophet

df_prophet = df.reset_index()[['fecha', 'valor']].rename(
    columns={'fecha': 'ds', 'valor': 'y'}
)

model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
model.fit(df_prophet)

future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)
model.plot(forecast)
```

## Anti-patrones

- ❌ **No verificar estacionariedad**: modelos como ARIMA asumen que la serie es estacionaria (media y varianza constantes). Usá Dickey-Fuller (`adfuller` de statsmodels) para verificarlo.
- ❌ **Hacer train/test split aleatorio**: en series temporales el split es temporal. Train = pasado, test = futuro. Usá `TimeSeriesSplit`.
- ❌ **Leakage en feature engineering**: si usás `shift(-1)` o `rolling(center=True)`, estás filtrando información del futuro. Siempre usá `shift(1)` o `rolling(..., min_periods=..., closed='left')`.
- ❌ **Ignorar estacionalidad**: si tus datos tienen estacionalidad semanal y no la modelás, tu forecast va a ser malo.
- ❌ **Forecast muy lejano**: cuanto más lejos pronosticás, más incertidumbre. Prophet te da intervalos de confianza — usalos.

## Alternativas

- **Prophet**: fácil, robusto a outliers, maneja festividades. Bueno para negocio.
- **Statsmodels SARIMA**: más control estadístico, pero requiere más tuning.
- **Nixtla (MLForecast, StatsForecast)**: librerías modernas con modelos optimizados y paralelizados.
- **Kats (Meta)**: toolkit completo de Facebook para análisis de series temporales.
- **sktime**: API unificada tipo sklearn para series temporales.

## Tools relevantes

- `statsmodels.tsa` — descomposición, estacionariedad, SARIMA
- `prophet` — forecasting robusto con seasonality automática
- `pandas` — resample, rolling, shift, reindex
- `nixtla` — modelos modernos de forecasting
- `sktime` — pipelines de series temporales tipo sklearn
