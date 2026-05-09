# Workflow: Data Modeler (ML)

## Skills disponibles

Cargá según la tarea:
- `ml-modeling` → scikit-learn, XGBoost, SHAP (solo para ML complejo)
- `time-series-analysis` → Prophet, Statsmodels (cuando hay datos temporales)
- `statistical-testing` → SciPy, tests de hipótesis (para validar resultados)
- `data-validation` → Pydantic, validación de esquemas (para verificar calidad)

## Flujo principal

```
Orchestrator → [1. Entender problema] → [2. Preparar datos] → [3. Baseline] → [4. Modelar] → [5. Evaluar] → [6. Explicar] → Orchestrator
```

## Paso a paso

### 1. Entender el problema
- ¿Regresión, clasificación, clustering?
- ¿Métrica principal? (accuracy, F1, RMSE, R², AUC)
- ¿Restricciones? (latencia, memoria, interpretabilidad)

### 2. Preparar datos
- Separar X/y, train/test split (estratificado si es clasificación)
- Encoding: one-hot para baja cardinalidad, target encoding para alta
- Scaling: StandardScaler para modelos lineales, RobustScaler si hay outliers
- Manejo de nulos: imputación con media/mediana/moda según el caso

### 3. Baseline
- Modelo simple (DummyClassifier, regresión lineal, media)
- Establecer piso: "cualquier modelo que no supere esto no sirve"

### 4. Modelar (2-3 modelos)
- Elegir según tipo de problema y tamaño de datos:
  - Chico (<10k): Random Forest, SVM, Logistic Regression
  - Mediano (10k-100k): Gradient Boosting (LGBM, XGB)
  - Grande (>100k): LGBM, Neural Networks
- Hacer cross-validation (5 folds mínimo)

### 5. Evaluar
- Comparar métricas entrenamiento vs validación (detectar overfitting)
- Matriz de confusión (si clasificación)
- Curva ROC / Precision-Recall según balance de clases
- Learning curves

### 6. Explicar
- Feature importance (permutation importance o SHAP)
- Mostrar top 5-10 features con dirección del impacto
- Conclusión: ¿el modelo sirve para producción?
