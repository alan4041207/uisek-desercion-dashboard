# 🎓 Dashboard EDA — Deserción Estudiantil UISEK

Dashboard interactivo de análisis exploratorio de datos (EDA) sobre deserción estudiantil en la Universidad Internacional SEK (UISEK), desarrollado con Streamlit.

## 📊 Descripción

Este dashboard analiza los factores que influyen en la deserción estudiantil a partir de un dataset de 300 estudiantes con 16 variables académicas, financieras y de comportamiento.

## 🚀 Demo en vivo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://alan4041207-uisek-desercion-dashboard.streamlit.app)

## 📋 Contenido del Dashboard

| Tab | Contenido |
|-----|-----------|
| 📊 **Estadísticas Descriptivas** | Tabla con Media, Mediana, Std, Skewness, Kurtosis · Distribución por carrera |
| 📦 **Distribuciones** | Boxplots de 12 variables · Violin plots comparativos |
| 🔗 **Análisis Bivariado** | Medias por grupo con poder estadístico · Scatter plots clave |
| 🌡️ **Correlaciones** | Heatmap triangular · Pair plot · Correlación con deserción |
| 📋 **Perfil & Resumen** | Perfil del estudiante en riesgo · Resumen ejecutivo |

## 🔍 Variables del Dataset

| Variable | Descripción |
|----------|-------------|
| `carrera` | Carrera universitaria |
| `semestre_actual` | Semestre en curso |
| `promedio_notas` | Promedio académico (0–10) |
| `asistencia_porcentaje` | Porcentaje de asistencia a clases |
| `materias_reprobadas_acum` | Materias reprobadas acumuladas |
| `trabaja` | Si el estudiante trabaja (0/1) |
| `horas_trabajo_semanal` | Horas de trabajo por semana |
| `actividad_canvas_semanal` | Actividad semanal en el LMS Canvas |
| `tiene_beca` | Si cuenta con beca (0/1) |
| `deuda_pendiente_usd` | Deuda pendiente en USD |
| `vive_fuera_de_quito` | Si vive fuera de Quito (0/1) |
| `visitas_tutoria_semestre` | Visitas a tutoría en el semestre |
| `participa_extracurricular` | Participación en actividades extracurriculares |
| `deserto_semestre` | Variable objetivo: deserción (0/1) |

## 🔑 Hallazgos Principales

1. **Predictor financiero:** `deuda_pendiente_usd` es el factor más crítico (r=+0.239)
2. **Rendimiento académico:** `promedio_notas` con correlación negativa fuerte (r=-0.257)
3. **Factor protector:** Tasa de deserción SIN beca: ~33% vs CON beca: ~14%
4. **Asistencia:** Cae de 71.4% a 65.4% en estudiantes desertores

## 🛠️ Instalación local

```bash
git clone https://github.com/alan4041207/uisek-desercion-dashboard.git
cd uisek-desercion-dashboard
pip install -r requirements.txt
streamlit run Dashboard.py
```

## 📦 Tecnologías

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.57-red)
![Pandas](https://img.shields.io/badge/Pandas-3.0-green)
![Seaborn](https://img.shields.io/badge/Seaborn-0.13-orange)

## 👨‍💻 Autor

Desarrollado para la materia de **Ingeniería de Data Science** — UISEK
