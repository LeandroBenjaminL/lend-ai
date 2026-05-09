---
name: ml-modeling
description: >
  Modelado de machine learning con Scikit-learn, LightGBM, XGBoost, y explicabilidad con SHAP/LIME.
  Trigger: Cuando necesitás entrenar modelos, hacer regresión, clasificación, feature importance, o explicar predicciones.
license: Apache-2.0
metadata:
  author: leandro-data
  version: "1.2"
  model_tier: T4-reasoning
---

# Skill: ml-modeling

Modelado de machine learning: regresión, clasificación, clustering y explicabilidad. Del baseline al modelo productivo.

## Trigger

Cargá esta skill cuando:
- Tenés una tarea de regresión, clasificación o clustering
- Necesitás evaluar qué features son más importantes
- Querés comparar múltiples modelos y elegir el mejor
- Te piden explicar por qué el modelo predice lo que predice

## Pipeline estándar — el orden importa

```python
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, mean_squared_error, r2_score

X = df.drop(columns=['target'])
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42,
    stratify=y if classification else None  # preserva proporciones
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**Por qué escalar**: modelos basados en distancias (KNN, SVM, regresión logística) asumen que todas las features están en la misma escala. Tree-based (Random Forest, LGBM) no necesitan escalado.

## Cómo elegir modelo

| Tarea | Modelo | Cuándo usarlo |
|-------|--------|---------------|
| Regresión | `LinearRegression` | Baseline simple, necesitás interpretabilidad |
| Regresión | `LGBMRegressor` | Grandes datasets (>10k filas), mejor performance |
| Regresión | `XGBRegressor` | Necesitás regularización fuerte, datos chicos |
| Clasificación | `LogisticRegression` | Baseline interpretable, probabilidades calibradas |
| Clasificación | `LGBMClassifier` | Default para clasificación en datos grandes |
| Clasificación | `RandomForestClassifier` | Interpretabilidad > performance |
| Clustering | `KMeans` | Segmentación simple, asumís clusters esféricos |

## Explicabilidad con SHAP

```python
import shap

model = LGBMClassifier()
model.fit(X_train, y_train)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

shap.summary_plot(shap_values, X_test, feature_names=X.columns)
```

**Por qué SHAP y no feature_importances_**: `feature_importances_` de sklearn te dice qué features usa el modelo, pero no cómo las usa (relación positiva o negativa). SHAP te da direccionalidad y magnitud por predicción individual.

## Ejemplo completo

```python
import lightgbm as lgb

model = lgb.LGBMClassifier(n_estimators=100, learning_rate=0.1)
scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='accuracy')
print(f'CV Accuracy: {scores.mean():.3f} (+/- {scores.std():.3f})')

model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred))
```

## Anti-patrones

- ❌ **No hacer train/test split**: evaluar en los mismos datos que entrenaste es hacer trampa y te da métricas irreales.
- ❌ **Hacer feature selection antes del split**: perdés información de la distribución del test set. Siempre split primero.
- ❌ **Escalar antes del split**: `fit_transform` en el set completo filtra información del test al train.
- ❌ **GridSearch con demasiadas combinaciones**: 10^4 combinaciones no es mejor que 50 bien elegidas.
- ❌ **Ignorar desbalanceo de clases**: si tenés 95% clase A y 5% clase B, accuracy del 95% no es bueno. Usá `class_weight` o SMOTE.

## Alternativas

- **PyCaret** — auto-ML con bajo código. Bueno para prototipar rápido.
- **H2O.ai** — auto-ML empresarial, maneja datasets enormes.
- **CatBoost** — maneja categóricas nativamente, ideal si tenés muchas.
- **scikit-learn** sigue siendo el estándar para prototipado y educación.

## Tools relevantes

- `scikit-learn` — base para modelos clásicos y preprocesamiento
- `lightgbm` / `xgboost` / `catboost` — gradient boosting
- `shap` / `lime` — explicabilidad
- `imblearn` — manejo de clases desbalanceadas (SMOTE)
- `optuna` — hyperparameter tuning más inteligente que GridSearch
