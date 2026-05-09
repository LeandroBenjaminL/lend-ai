# Patterns: Cheat Sheet Técnico de ML

## Configuración inicial estándar

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, f1_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import lightgbm as lgb
import xgboost as xgb
import shap
```

## Train/test split — ANTES de cualquier transformación

```python
X = df.drop(columns=['target'])
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42,
    stratify=y if is_classification else None
)
```

## Pipeline con ColumnTransformer — evitá el leakage

```python
numeric_features = ['edad', 'ingreso', 'antiguedad']
categorical_features = ['provincia', 'rubro']

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_features),
    ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
])

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', lgb.LGBMClassifier(random_state=42))
])

pipeline.fit(X_train, y_train)
```

## Validación cruzada — nunca evalúes sobre una sola partición

```python
from sklearn.model_selection import StratifiedKFold, cross_val_score
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(pipeline, X_train, y_train, cv=skf, scoring='f1_macro')
print(f"F1 CV: {scores.mean():.4f} (+/- {scores.std():.4f})")
```

## Evaluación de clasificación — siempre matriz de confusión

```python
y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(f"ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")
```

## Feature importance nativa + SHAP

```python
# Acceder al modelo dentro del pipeline
model = pipeline.named_steps['model']
feat_names = pipeline.named_steps['preprocessor'].get_feature_names_out()
feat_imp = pd.DataFrame({'feature': feat_names, 'importance': model.feature_importances_})
feat_imp.sort_values('importance', ascending=False).head(10)

# SHAP: explicabilidad real, no solo importancia
X_processed = pipeline.named_steps['preprocessor'].transform(X_test)
X_processed_df = pd.DataFrame(X_processed, columns=feat_names)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_processed)
shap.summary_plot(shap_values, X_processed_df)
shap.dependence_plot(feat_imp.iloc[0]['feature'], shap_values, X_processed_df)
```

## Reglas de oro

- **NUNCA** escalar antes de hacer el split — leakage seguro
- **NUNCA** usar `sparse_output=True` con SHAP — explota
- **SIEMPRE** usar `random_state` para reproducibilidad
- **SIEMPRE** verificar que `feature_names_out()` matchee con las columnas procesadas
- Para datasets grandes (>100k filas), LightGBM con `n_estimators=200, learning_rate=0.05` es el default razonable
- Para datasets chicos (<5k filas), Random Forest con `n_estimators=100` y validación cruzada estratificada
- Serializar con `joblib.dump(pipeline, 'modelo.pkl')` — mantiene todo el pipeline junto
