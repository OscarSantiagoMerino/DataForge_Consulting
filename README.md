# DataForge Consulting · Sistema de Decision Intelligence para la retención de clientes (Caso Telco)

Proyecto final de *Decision Intelligence & Business Analytics*, Maestría en Ciencia de Datos, Escuela Colombiana de Ingeniería Julio Garavito. Docente: Juliana De Mier Medellín.

**Equipo:** Oscar Santiago Merino Suárez · Claudia Rocío Rodríguez Ortiz · Paula Andrea Gacha García · Daniel Felipe Pérez Pineda

> **Pregunta de decisión:** ¿Qué segmentos de clientes activos debe priorizar la Gerencia de Retención este mes, con qué palanca de retención y con qué retorno esperado, para reducir el MRR perdido por churn sin deteriorar el ARPU?

## Resultados en una mirada

| | |
|---|---|
| Problema | 26.5 % de los clientes abandonó en el período de corte: USD 139 mil de MRR, el **30.5 % del MRR** |
| North Star | **% MRR retenido = 69.5 %** (meta ≥ 75 %) |
| Concentración | Clientes *mes a mes con fibra*: 30 % de la base y **72 % del MRR perdido** |
| Drivers | Primeros meses (52.9 % de churn en 0–6 m), contrato mes a mes, fibra (OR 2.1), cheque electrónico (OR 1.4); seguridad y soporte reducen el riesgo (OR ≈ 0.7) |
| Recomendación | Piloto con grupo control del **programa focalizado** sobre 820 clientes de riesgo alto (ROI base +179 %). **No** lanzar un descuento masivo (ROI base −32 %) |

## Entregables (sección 7 del enunciado)

| # | Entregable | Ubicación |
|---|---|---|
| 1 | Informe final en PDF (14 páginas de cuerpo + anexos) | [`informe/informe_final.pdf`](informe/informe_final.pdf) (fuente LaTeX: `informe/informe_final.tex`) |
| 2 | Notebook reproducible (de la carga a los análisis) | [`notebooks/DataForge_Telco_Churn.ipynb`](notebooks/DataForge_Telco_Churn.ipynb) |
| 3 | Dashboard en Power BI (proyecto PBIP, 4 páginas, 39 medidas DAX) | [`powerbi/DataForge_Telco_Churn.pbip`](powerbi/DataForge_Telco_Churn.pbip) · capturas en `outputs/figuras/dashboard_p*.png` |
| 4 | Diccionario de métricas (9 métricas críticas, Plantilla 2) | [`docs/diccionario_metricas.md`](docs/diccionario_metricas.md) |
| 5 | Presentación ejecutiva (≤ 10 min, con notas del orador) | [`presentacion/DataForge_Presentacion_Ejecutiva.pptx`](presentacion/DataForge_Presentacion_Ejecutiva.pptx) |
| 6 | README con instrucciones | Este archivo |

## Estructura del repositorio

```
├── Data/                         Dataset original (no se modifica)
├── notebooks/                    Notebook reproducible
├── outputs/
│   ├── figuras/                  Figuras del análisis y capturas del dashboard
│   ├── tablas/                   Auditoría, df_analitico, KPIs, segmentación, ROI, plan de monitoreo…
│   └── cifras_clave.json         Cifras usadas en el informe y la presentación
├── powerbi/
│   ├── data/                     Modelo estrella en CSV (lo genera el notebook)
│   ├── DataForge_Telco_Churn.pbip
│   ├── DataForge_Telco_Churn.SemanticModel/   Modelo TMDL (tablas, relaciones, medidas)
│   ├── DataForge_Telco_Churn.Report/          Reporte PBIR (4 páginas)
│   └── MEDIDAS_DAX.md            Documentación de las medidas
├── informe/                      Informe LaTeX + PDF
├── presentacion/                 Presentación ejecutiva
└── docs/                         Diccionario de métricas y nota de uso de IA
```

Las carpetas `Enunciado/` y `Documentos/` (material del curso) están excluidas del repositorio por `.gitignore`.

## Cómo reproducir el análisis

### 1. Notebook (Python 3.10+)

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
jupyter notebook notebooks/DataForge_Telco_Churn.ipynb
```

Ejecute *Run All*. El notebook lee `Data/WA_Fn-UseC_-Telco-Customer-Churn.csv` y regenera `outputs/`, `powerbi/data/` y `docs/diccionario_metricas.md`. Si alguna validación de calidad falla, el notebook se detiene. Funciona desde la raíz del repositorio o desde `notebooks/`.

**En Google Colab:** `!git clone <url-del-repositorio>`, luego `%cd <carpeta-del-repositorio>` y abrir el notebook. Las librerías ya vienen instaladas.

### 2. Dashboard en Power BI Desktop

1. Abra `powerbi/DataForge_Telco_Churn.pbip` (Power BI Desktop, versión 2025 o posterior).
2. La primera vez aparece el aviso *"Algunas de las tablas tienen datos incompletos o no tienen datos"*: pulse **Actualizar ahora**.
3. Si el repositorio está en una ruta distinta a `C:\Users\kimbo\Downloads\ProyectoFinalDIBA`, vaya a **Transformar datos → Editar parámetros**, cambie `RutaDatos` a la ruta de su carpeta `powerbi\data\` (con la barra final) y vuelva a actualizar.
4. Para entregar un archivo único: **Archivo → Guardar como → tipo "Archivos de Power BI (\*.pbix)"**.

Las páginas son: **1 · Resumen ejecutivo**, **2 · Diagnóstico**, **3 · Monitoreo y acción** (con un simulador de ROI por escenario) y **4 · Definiciones y supuestos**.

### 3. Informe (LaTeX)

```bash
cd informe
python generar_anexos.py                 # regenera el anexo del diccionario desde powerbi/data/dim_metricas.csv
pdflatex informe_final.tex               # ejecutar dos veces
```

## Fuente de datos

IBM, *Telco Customer Churn* (IBM Sample Data Sets), publicado en Kaggle por blastchar: <https://www.kaggle.com/datasets/blastchar/telco-customer-churn>. Es un dataset público, didáctico y ficticio.

## Uso de herramientas de IA

Ver [`docs/nota_uso_ia.md`](docs/nota_uso_ia.md) (sección 13 del enunciado).
