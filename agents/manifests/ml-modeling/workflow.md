# Workflow: Modelado de Machine Learning

Seguí este flujo siempre. No saltees pasos. Si los datos no pasan la validación, parás y delegás.

## 1. Entender el problema de negocio
- ¿Qué decisión se va a tomar con las predicciones?
- ¿Clasificación, regresión, clustering, ranking?
- ¿Cuál es la métrica de negocio que importa? (no solo accuracy técnica)
- ¿Hay restricciones de latencia, interpretabilidad, fairness?

## 2. Validar que los datos estén limpios
- Si el dataset no fue limpiado → **delegar a `data-cleaning`**
- Verificar nulos, outliers, tipos correctos, encoding
- Si hay fuga de datos (data leakage) potencial, marcarla YA

## 3. Feature engineering y selección
- Crear features derivadas con sentido de negocio (no feature explosion sin criterio)
- Encoding: OneHot para baja cardinalidad, Target Encoding para alta, Ordinal cuando hay orden
- Escalar SIEMPRE para modelos sensibles a escala (regresión lineal, SVM, KNN, NN)
- Seleccionar con mutual information, permutation importance o RFE — no por intuición

## 4. Baseline simple primero
- **Clasificación**: LogisticRegression o DecisionTreeClassifier (max_depth=3)
- **Regresión**: LinearRegression o DecisionTreeRegressor (max_depth=3)
- Evaluar con cross_val_score (cv=5 o StratifiedKFold si desbalanceo)
- Esta es tu vara. Si un modelo complejo no supera significativamente esto, no lo usás.

## 5. Probar modelos más complejos SOLO si el baseline no alcanza
- LightGBM / XGBoost como default para tabulares
- Random Forest cuando la interpretabilidad importa más que 1% de accuracy
- SVM o KNN solo si hay justificación clara

## 6. Tuning de hiperparámetros
- RandomizedSearchCV primero (más rápido, igual de efectivo para explorar)
- GridSearchCV solo si el espacio de búsqueda es chico y justificado
- Nunca tunear sobre el conjunto de test — eso es hacer trampa

## 7. Evaluar con métricas relevantes
- **Clasificación**: No solo accuracy. Mirá precision, recall, F1, ROC-AUC, matriz de confusión
- **Clases desbalanceadas**: F1 macro, precision-recall curve, no accuracy
- **Regresión**: RMSE, MAE, R², y mirá los residuos (no solo un número)
- **Siempre**: comparar contra un dummy baseline (clase mayoritaria, media)

## 8. Explicar el modelo
- **SHAP** para explicaciones locales y globales: summary_plot, dependence_plot, waterfall
- **LIME** como alternativa cuando SHAP es muy lento
- **Permutation importance** para validar que las features importantes tienen sentido de negocio
- Si una feature top no tiene explicación de negocio, investigá — puede ser leakage

## 9. Entregar modelo + explicación
- Serializar con joblib (no pickle para objetos grandes)
- Documentar: features usadas, métricas alcanzadas, limitaciones conocidas
- Incluir al menos UN gráfico de explicabilidad (SHAP summary)
- Si el modelo va a producción, dejar script de inferencia listo
