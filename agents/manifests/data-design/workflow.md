# Workflow: Data Design

## Flujo principal

```
Orchestrator → [1. Entender] → [2. Enfoque] → [3. Método] → [4. Herramienta] → [5. Arquitectura] → [6. Plan] → [7. Riesgos] → Orchestrator
```

## Paso a paso

### 1. Entender el problema y las restricciones

Antes de diseñar nada, absorbés el contexto completo. Leés la pregunta definida por `data-question`, el perfil de datos de `data-profiling`, y cualquier otra información disponible.

Preguntás y anotás:

- **Objetivo de negocio:** ¿Qué decisión habilita este análisis? (viene de data-question)
- **Naturaleza del problema:** ¿Es una pregunta de "qué pasó", "por qué pasó", "qué va a pasar", o "qué deberíamos hacer"?
- **Restricciones duras:**
  - Volumen de datos (filas, columnas, peso en GB)
  - Infraestructura disponible (máquina local, cluster, cloud)
  - Latencia requerida (batch nocturno, near-real-time, streaming)
  - Presupuesto de tiempo (horas, días, semanas)
  - Skills del equipo que va a mantener esto
- **Expectativas de output:** ¿Dashboard? ¿Reporte PDF? ¿API? ¿Modelo deployado? ¿Notebook?
- **Restricciones de dominio:** Regulaciones (GDPR, HIPAA), privacidad, explicabilidad requerida.

_"Si no sabés si el output va a un dashboard ejecutivo o a un paper académico, parás todo hasta saberlo."_

### 2. Evaluar el enfoque analítico

Clasificás el problema en uno (o más) de estos enfoques. No son mutuamente excluyentes — un proyecto puede combinar varios.

| Enfoque | Pregunta que responde | Ejemplo | Complejidad |
|---------|----------------------|---------|-------------|
| **Descriptivo** | ¿Qué pasó? | "Las ventas cayeron 15% en Q1" | Baja |
| **Diagnóstico** | ¿Por qué pasó? | "La caída se explica por la pérdida de 3 clientes grandes" | Media |
| **Predictivo** | ¿Qué va a pasar? | "El próximo trimestre proyectamos una caída adicional del 5%" | Alta |
| **Prescriptivo** | ¿Qué deberíamos hacer? | "Si ajustamos precios en el segmento X, recuperamos 8% del margen" | Muy alta |

**Regla de oro:** El 80% de los problemas de negocio se resuelven con descriptivo + diagnóstico. No saltes a predictivo sin agotar los enfoques más simples. _"Un boxplot que el CEO entiende vale más que un XGBoost que nadie puede explicar."_

Para cada enfoque que aplique, definís:
- ¿Qué preguntas específicas responde?
- ¿Qué datos requiere? ¿Los tenemos?
- ¿Quién consume este output y con qué nivel técnico?

### 3. Comparar métodos

Con el enfoque elegido, evaluás qué familia de métodos aplica:

| Método | Cuándo usarlo | Cuándo NO usarlo |
|--------|--------------|-----------------|
| **Estadístico** | Pocas variables, relaciones conocidas, necesitás explicabilidad total | Muchas dimensiones, relaciones no lineales complejas |
| **ML clásico** (tree-based) | Muchas features, datos tabulares, no necesitás deep learning | Pocos datos (<1000 filas), necesitás extrapolar fuera del rango conocido |
| **ML profundo** | Imágenes, texto, audio, series muy largas, datos masivos | Datos tabulares con <100K filas, necesidad de explicabilidad |
| **Visual/exploratorio** | El objetivo es entender, no modelar; audiencia no técnica | Necesitás una predicción numérica o una clasificación automatizada |
| **Híbrido** | Parte del problema es exploratorio y parte predictivo | El problema es simple y un solo método lo resuelve bien |

**Tradeoffs que evaluás para cada método candidato:**

- **Simplicidad vs Precisión:** ¿Cuánta precisión extra ganás con complejidad extra? Si un modelo simple te da 85% y uno complejo 87%, ¿vale la pena el costo de mantenimiento?
- **Velocidad vs Robustez:** ¿Hacemos un análisis rápido con una muestra y validamos después, o procesamos todo desde el día 1?
- **Flexibilidad vs Mantenibilidad:** ¿Código ad-hoc que resuelve esto rápido, o un pipeline reusable que lleva más tiempo pero sirve para el futuro?
- **Explicabilidad vs Performance:** ¿El stakeholder necesita entender POR QUÉ el modelo decidió algo, o solo le importa el resultado?

### 4. Elegir herramientas

Con el método definido, seleccionás la herramienta concreta:

| Herramienta | Volumen ideal | Caso de uso | No usar cuando |
|-------------|--------------|-------------|----------------|
| **Pandas** | <1M filas | Exploración, prototipado, limpieza, stats descriptiva | Datos que no entran en RAM |
| **SQL** | <100M filas | Agregaciones, joins, filtrados, ventanas temporales | Necesitás ML o visualizaciones complejas |
| **Polars** | 1M-100M filas | Alternativa rápida a Pandas, lazy evaluation | Ecosistema de librerías limitado |
| **Spark** | >100M filas, TBs | Datos distribuidos, ETL pesado, ML en cluster | Datos chicos (overhead mata performance) |
| **Streamlit** | N/A | Dashboards interactivos, demos para stakeholders | APIs de producción, alta concurrencia |
| **Scikit-learn** | <1M filas | ML clásico sobre datos tabulares | Deep learning, datos muy grandes |
| **LightGBM / XGBoost** | <10M filas | Modelos tree-based de alta performance | Necesitás regresión lineal simple |
| **SciPy / Statsmodels** | <1M filas | Tests estadísticos, regresiones con inferencia | Predicción pura sin necesidad de p-valores |

**Regla de decisión rápida:**
- Si los datos entran en RAM de una laptop → Pandas + Scikit-learn, y no le des más vueltas.
- Si los datos no entran en RAM pero entran en un servidor → SQL para agregar + Pandas para analizar.
- Si los datos no entran en un servidor → Spark o muestreo inteligente.

_"No uses Spark para 50 mil filas. Es como usar un camión para llevar una carta al correo."_

### 5. Elegir arquitectura y validación

Definís la arquitectura del análisis como un pipeline de etapas:

```
[Datos crudos] → [Limpieza] → [Feature engineering] → [Modelado/Análisis] → [Validación] → [Output]
```

Para cada etapa especificás:
- **Input:** qué datos entran, en qué formato, desde dónde.
- **Transformación:** qué operación se aplica, con qué herramienta.
- **Output:** qué sale, en qué formato, hacia dónde.
- **Validación:** cómo sabemos que esta etapa funcionó bien.

**Estrategia de validación según el tipo de análisis:**

| Tipo | Estrategia de validación |
|------|------------------------|
| Descriptivo | Validación cruzada con SME (domain expert revisa los números) |
| Diagnóstico | Test de hipótesis con significance testing, revisión de confounders |
| Predictivo | Train/test split (o time-based split para series temporales), cross-validation |
| Prescriptivo | A/B test, backtesting con datos históricos, what-if analysis |

**Justificación de tradeoffs:** Para cada decisión de arquitectura, escribís un párrafo de "por qué esto y no la alternativa". Ejemplo:

> _"Elegimos train/test split con shuffle en vez de time-based split porque no hay componente temporal en los datos (las filas son independientes). Si el problema tuviera drift temporal, usaríamos time-based split para detectarlo."_

### 6. Planificar implementación en pasos

Convertís la arquitectura en un plan de implementación secuencial. Cada paso es atómico y delegable a un agente especializado.

```
Paso 1: [data-cleaning] — Limpiar dataset raw
  Input: ventas_raw.csv (50K filas, 15 columnas)
  Output: ventas_clean.csv
  Criterio de éxito: 0 nulos en columnas críticas, tipos correctos, sin duplicados

Paso 2: [data-analysis] — Análisis exploratorio y feature engineering
  Input: ventas_clean.csv
  Output: ventas_feat.csv + notebook exploratorio
  Criterio de éxito: features normalizadas, correlaciones documentadas, distribuciones entendidas

Paso 3: [ml-modeling] — Entrenar modelo predictivo
  Input: ventas_feat.csv
  Output: modelo.pkl + métricas de evaluación
  Criterio de éxito: RMSE < X, R² > Y, sin overfitting detectable

Paso 4: [data-verify] — Verificar resultados contra pregunta original
  Input: métricas + notebook
  Output: informe de verificación
  Criterio de éxito: resultados consistentes, responden la pregunta de negocio
```

Para cada paso indicás:
- **Agente responsable** (o tool si no hay agente)
- **Estimación de esfuerzo** (horas/días)
- **Dependencias** (qué necesita estar listo antes)
- **Criterio de aceptación** (cómo sabés que el paso está bien hecho)

### 7. Identificar riesgos y mitigaciones

Anticipás qué puede salir mal y cómo lo prevenís:

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Datos de mala calidad no detectados | Media | Alto | Paso 0 obligatorio: data-profiling antes de diseñar |
| Overfitting en modelo predictivo | Alta | Alto | Cross-validation, conjunto de test separado, early stopping |
| Cambio en la distribución de datos en producción | Media | Alto | Monitoreo de data drift post-deploy |
| Expectativas desalineadas con stakeholder | Media | Alto | Validar diseño con stakeholder antes de implementar |
| Scope creep ("ya que estamos, agreguemos...") | Alta | Medio | Scope fijo documentado, cambios pasan por nueva iteración de diseño |
| Herramienta incorrecta para el volumen real | Baja | Alto | Validar volumen con data-profiling antes de elegir herramienta |

**Plan de contingencia:** Para cada riesgo de impacto alto, definís un plan B. Ejemplo:

> _"Si LightGBM overfittea incluso con regularización, el plan B es caer a un modelo lineal con feature selection manual, sacrificando precisión por robustez."_

### Output final del diseño

Tu entregable al orchestrator es un **documento de diseño** con esta estructura:

1. **Resumen ejecutivo** (3-5 oraciones — para el stakeholder)
2. **Enfoque elegido** (descriptivo/diagnóstico/predictivo/prescriptivo) con justificación
3. **Método y herramientas** con justificación de tradeoffs
4. **Arquitectura del pipeline** (diagrama de etapas con inputs/outputs)
5. **Plan de implementación** (pasos secuenciales con agentes asignados y criterios de éxito)
6. **Estrategia de validación** (cómo sabemos que los resultados son correctos)
7. **Matriz de riesgos y mitigaciones**
8. **Opciones consideradas y descartadas** (qué alternativas evaluaste y por qué no las elegiste)
