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
│   ├── 1-Diagnóstico de la Calidad Datos (QA).ipynb
│   ├── 2. Feature engineering.ipynb
│   ├── 3. EDA.ipynb
│   ├── 4. Pre Modelado.ipynb
│   ├── 5. Modelado.ipynb
│
├── output/
│   ├── data-bank_1.parquet                   # Salida de la etapa 1 (calidad de datos)
│   ├── data-bank_2_FE.parquet                # Salida de la etapa 2 (feature engineering)
│   ├── data-bank_3_EDA.parquet               # Salida de la etapa 3 (EDA)
│   ├── data-bank_4_PreModeling.parquet       # Salida de la etapa 4 (pre-modelado)
│   ├── fig_curva_ROC.png
│   ├── fig_matrices_confusion.png
│   ├── fig_metricas_comparacion.png
│   ├── fig_overfitting.png
│   └── resultados_modelado.json              # Métricas finales de los modelos
└── docs/
    └── Comprension_Negocio.xlsx              # Comprensión del negocio (CRISP-DM)
```

## Flujo de ejecución

Los notebooks de `core/` se ejecutan en orden. Cada uno lee la salida del anterior y guarda su resultado en `output/`.

| Paso | Notebook | Entrada | Salida |
|---|---|---|---|
| 1 | `1-Diagnóstico de la Calidad Datos (QA).ipynb` | `data/bank.csv` | `output/data-bank_1.parquet` |
| 2 | `2. Feature engineering.ipynb` | `data-bank_1.parquet` | `output/data-bank_2_FE.parquet` |
| 3 | `3. EDA.ipynb` | `data-bank_2_FE.parquet` | `output/data-bank_3_EDA.parquet` |
| 4 | `4. Pre Modelado.ipynb` | `data-bank_3_EDA.parquet` | `output/data-bank_4_PreModeling.parquet` |
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

pip install scikit-learn==1.8.* pandas numpy matplotlib seaborn pyarrow jupyter
jupyter notebook
```

Luego abrir los notebooks de `core/` y ejecutarlos en el orden indicado.

## Resultados principales

Exactitud (accuracy) sobre el conjunto de prueba y validación cruzada de 5 pliegues:

| Modelo | Accuracy (prueba) | Accuracy (validación cruzada) |
|---|---|---|
| **SVM** | **84,22 %** | **84,43 %** |
| Regresión Logística | 82,03 % | 82,03 % |
| Árbol de Decisión (CART) | 78,53 % | 78,33 % |
| Naïve Bayes | 74,81 % | 73,83 % |

- El SVM obtuvo además el mayor AUC (0,9155) entre los cuatro modelos.
- El Árbol de Decisión alcanza 100 % en entrenamiento (sobreajuste); la validación cruzada permite estimar su desempeño real.
- Variables más influyentes: duración del último contacto (55,10 %), tipo de contacto (12,50 %) y número de contactos previos a la campaña (8,71 %).

### Limitaciones a considerar

- Se usa la versión **balanceada** del dataset (≈47 % de casos positivos), por lo que las métricas no son directamente comparables con las del conjunto original desbalanceado (≈11 %).
- El modelo incluye la variable `duration`, que solo se conoce una vez finalizada la llamada. Sin ella, el AUC del SVM baja de 0,9155 a 0,7854.
- La partición es aleatoria estratificada, no temporal, lo que puede sobreestimar el desempeño frente a una campaña futura.

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
