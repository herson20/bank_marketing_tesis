# Bank Marketing – Análisis comparativo de modelos de clasificación supervisada

Repositorio de reproducibilidad de la tesis **"Análisis comparativo de modelos de clasificación supervisada para seleccionar la mejor tasa de éxito en la adquisición de un depósito a plazo fijo usando métricas de rendimiento en aprendizaje automático de máquinas"**.

- **Autor:** Herson Raúl Urbina Cayo
- **Asesor:** Mag. Gianfranco Málaga Tejada
- **Institución:** Universidad Nacional Jorge Basadre Grohmann (UNJBG) – Facultad de Ingeniería, Escuela Profesional de Ingeniería en Informática y Sistemas
- **Grado:** Título Profesional de Ingeniero en Informática y Sistemas

---

## Objetivo

Comparar cuatro algoritmos de clasificación supervisada para predecir si un cliente de una entidad bancaria portuguesa suscribirá un depósito a plazo fijo tras una campaña de telemarketing, y seleccionar el de mejor desempeño con métricas de rendimiento (accuracy, precision, recall, F1-score, matriz de confusión y curva ROC/AUC).

Modelos evaluados:

- Support Vector Machine (SVM)
- Regresión Logística
- Árbol de Decisión (CART)
- Naïve Bayes

Metodología: **CRISP-DM**.

## Dataset

- **Fuente:** [Bank Marketing Dataset – Kaggle](https://www.kaggle.com/datasets/janiobachmann/bank-marketing-dataset) (Bachmann, 2017).
- **Origen:** versión con clases balanceadas del conjunto original *Bank Marketing* del [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/222/bank+marketing) (Moro et al., 2014).
- **Tamaño:** 11 162 registros y 17 variables (16 atributos de entrada y la variable objetivo `deposit`).
- **Archivo en el repositorio:** `data/bank.csv`.

## Estructura del repositorio

```
bank_marketing_tesis/
├── data/
│   └── bank.csv                              # Dataset original (Kaggle)
├── core/
│   ├── 1. Profile_data_QA.ipynb
│   ├── 2. Feature_engineering.ipynb
│   ├── 3. EDA.ipynb
│   ├── 4. Pre_Modelado.ipynb
│   ├── 5. Modelado.ipynb
│
├── output/
│   ├── data-bank_1.parquet                   # Salida de la etapa 1 (calidad de datos)
│   ├── data-bank_2_FE.parquet                # Salida de la etapa 2 (feature engineering)
│   ├── data-bank_3_EDA.parquet               # Salida de la etapa 3 (EDA)
│   ├── data-bank_4_PreModeling.parquet       # Salida de la etapa 4 (pre-modelado)
└── docs/
    └── Comprension_Negocio.xlsx              # Comprensión del negocio (CRISP-DM)
```

## Flujo de ejecución

Los notebooks de `core/` se ejecutan en orden. Cada uno lee la salida del anterior y guarda su resultado en `output/`.

| Paso | Notebook | Entrada | Salida |
|---|---|---|---|
| 1 | `1. Profile_data_QA.ipynb` | `data/bank.csv` | `output/data-bank_1.parquet` |
| 2 | `2. Feature_engineering.ipynb` | `data-bank_1.parquet` | `output/data-bank_2_FE.parquet` |
| 3 | `3. EDA.ipynb` | `data-bank_2_FE.parquet` | `output/data-bank_3_EDA.parquet` |
| 4 | `4. Pre_Modelado.ipynb` | `data-bank_3_EDA.parquet` | `output/data-bank_4_PreModeling.parquet` |
| 5 | `5. Modelado.ipynb` | `data-bank_4_PreModeling.parquet` | `output/fig_*.png`, `output/resultados_modelado.json` |

## Configuración para reproducir los resultados

- **Python:** 3.12
- **scikit-learn:** 1.8
- **Semilla aleatoria:** `random_state = 42` en todos los modelos y particiones.
- **Partición:** 80 % entrenamiento / 20 % prueba, estratificada.
- **Validación cruzada:** `StratifiedKFold` con 5 pliegues (`shuffle=True`, `random_state=42`), métrica accuracy.

### Instalación

```bash
git clone https://github.com/herson20/bank_marketing_tesis.git
cd bank_marketing_tesis

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install \
  pandas numpy scipy scikit-learn \
  matplotlib seaborn missingno plotly \
  pyarrow \
  jupyter notebook ipykernel ipywidgets \
  watermark ydata-profiling

jupyter notebook
```

## Resultados principales

Métricas sobre el conjunto de prueba (20 %) y media de **validación cruzada estratificada de 5 pliegues**, con `random_state=42`:

| Modelo | Accuracy (prueba) | Accuracy (CV) | Precision | Recall | F1 | AUC |
|---|---|---|---|---|---|---|
| **SVM (RBF)** | **83,37 %** | **83,64 %** | 80,30 % | 86,00 % | 0,8305 | **0,9122** |
| Regresión Logística | 81,58 % | 81,42 % | 79,63 % | 82,12 % | 0,8086 | 0,8965 |
| Árbol de Decisión (CART) | 77,68 % | 77,47 % | 77,38 % | 74,74 % | 0,7603 | 0,7753 |
| Naïve Bayes | 71,22 % | 70,44 % | 79,60 % | 52,79 % | 0,6348 | 0,8213 |

- El **SVM** fue el mejor modelo tanto en accuracy como en AUC (0,9122), con un recall alto (86 %) que lo hace particularmente útil cuando el costo de un falso negativo (no contactar a un cliente que sí habría aceptado) es relevante.
- **Análisis de sobreajuste** (brecha `accuracy_train` − `cv_mean`):

| Modelo | Train | CV | Brecha |
|---|---|---|---|
| Árbol de Decisión (CART) | 100,00 % | 77,47 % | **+22,53 pp** (sobreajuste severo) |
| SVM | 87,51 % | 83,64 % | +3,87 pp (sobreajuste leve) |
| Regresión Logística | 81,77 % | 81,42 % | +0,35 pp |
| Naïve Bayes | 70,43 % | 70,44 % | −0,01 pp |

- El **Árbol de Decisión** alcanza 100 % en entrenamiento pero cae a ~77 % en validación cruzada: memoriza el set de entrenamiento y no generaliza. La validación cruzada permite medir ese efecto.
- Variables más influyentes según el árbol CART: **duración del último contacto (55,10 %)**, **tipo de contacto (12,50 %)** y **número de contactos previos a la campaña (8,71 %)**.

### Limitaciones a considerar

- Se usa la versión **balanceada** del dataset (≈47 % de casos positivos), por lo que las métricas no son directamente comparables con las del conjunto original desbalanceado (≈11 %).
- El modelo incluye la variable `duration` (segundos de la última llamada), que solo se conoce *después* de realizada la llamada. Sin esa variable, el AUC del SVM baja aproximadamente a ~0,78, lo que marca el techo real para un escenario predictivo *antes* del contacto.
- La partición es aleatoria estratificada, **no temporal**: no simula el paso del tiempo entre campañas y puede sobreestimar el desempeño frente a una campaña futura con distribuciones diferentes.
- Los resultados dependen del estado aleatorio fijado (`random_state=42`). Variaciones de ±0,5 pp en accuracy son esperables al cambiarlo.


## Cómo citar

```bibtex
@thesis{urbina2026bankmarketing,
  author = {Urbina Cayo, Herson Raúl},
  title  = {Análisis comparativo de modelos de clasificación supervisada para seleccionar la mejor tasa de éxito en la adquisición de un depósito a plazo fijo usando métricas de rendimiento en aprendizaje automático de máquinas},
  school = {Universidad Nacional Jorge Basadre Grohmann},
  year   = {2026},
  type   = {Tesis de pregrado},
  address = {Tacna, Perú}
}
```

## Referencias

- Moro, S., Cortez, P., & Rita, P. (2014). A data-driven approach to predict the success of bank telemarketing. *Decision Support Systems, 62*, 22–31. https://doi.org/10.1016/j.dss.2014.03.001
- Bachmann, J. (2017). *Bank marketing dataset* [Conjunto de datos]. Kaggle. https://www.kaggle.com/datasets/janiobachmann/bank-marketing-dataset

## Licencia y uso de datos

El código de este repositorio es de uso académico. El dataset pertenece a sus autores originales; consultar los términos de uso en Kaggle y UCI antes de redistribuirlo.
