# Patrones: Data Modeler

## Pipeline rápido (clasificación)

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

num_cols = X.select_dtypes(include=np.number).columns
cat_cols = X.select_dtypes(include='object').columns

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), num_cols),
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
])

pipe = Pipeline([
    ('prep', preprocessor),
    ('model', RandomForestClassifier(n_estimators=100, random_state=42))
])
```

## Cross-validation con métricas

```python
from sklearn.model_selection import cross_validate

scores = cross_validate(pipe, X_train, y_train,
                        cv=5, scoring=['accuracy', 'f1', 'roc_auc'],
                        return_train_score=True)

print(f"Train F1: {scores['train_f1'].mean():.3f} (±{scores['train_f1'].std():.3f})")
print(f"Val F1:   {scores['test_f1'].mean():.3f} (±{scores['test_f1'].std():.3f})")
```

## Detectar overfitting

```python
# learning curve
from sklearn.model_selection import learning_curve
train_sizes, train_scores, val_scores = learning_curve(
    pipe, X_train, y_train, cv=5,
    train_sizes=np.linspace(0.1, 1.0, 10)
)
gap = train_scores.mean() - val_scores.mean()
print(f"Brecha train-val: {gap:.3f}")  # >0.1 es overfitting
```

## SHAP explicability

```python
import shap
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test, feature_names=X.columns)
```
