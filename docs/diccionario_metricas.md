# Diccionario técnico de métricas — DataForge Consulting

Generado por `notebooks/DataForge_Telco_Churn.ipynb` (sección 8.2). Valores calculados sobre el corte del dataset Telco Customer Churn (IBM).

## 1. % MRR retenido (North Star)

| Campo | Definición |
|---|---|
| Tipo | Tasa / North Star Metric |
| Objetivo asociado | Proteger el ingreso recurrente |
| Decisión que soporta | Cuánto presupuesto asignar a retención y si el programa funciona |
| Definición de negocio | Proporción del ingreso recurrente mensual que se conserva al cierre del período |
| Fórmula | 1 − Σ cargo_mensual[churn = 1] / Σ cargo_mensual |
| Numerador | MRR de clientes que abandonan en el período |
| Denominador | MRR de todos los clientes al inicio del período |
| Unidad | % |
| Ventana temporal | Período de corte (mensual a futuro) |
| Filtros de inclusión | registro_valido = 1 |
| Exclusiones | Ninguna en el corte; a futuro, cuentas internas y de prueba |
| Dimensiones de segmentación | Contrato, servicio de internet, método de pago, antigüedad, riesgo, palanca |
| Meta o umbral | ≥ 75 % (verde); 69.5–75 % (amarillo); < 69.5 % (rojo) |
| Dirección deseada | Subir |
| Métricas de balance | ARPU, costo de retención, ROI del programa |
| Dueño | Gerencia de Retención |
| Riesgos de interpretación | Puede subir por alzas de precio a clientes que se quedan; con un solo corte no hay tendencia; la ventana del churn es ambigua |
| Acción asociada | Si cae al rojo, el Comité revisa el presupuesto y las palancas del mes |
| Medida DAX | [% MRR Retenido] |
| Valor en el corte | 69.5 % |
| Fuente de datos | df_analitico (derivada de WA_Fn-UseC_-Telco-Customer-Churn.csv) / fact_clientes en Power BI |
| Frecuencia de actualización | Mensual, con cada corte de clientes (hoy existe un solo corte) |
| Granularidad | Cliente (cálculo) → segmento y mes (reporte) |
| Unidad de análisis | Cliente |

## 2. Tasa de churn de clientes

| Campo | Definición |
|---|---|
| Tipo | Tasa |
| Objetivo asociado | Retener clientes |
| Decisión que soporta | Qué segmentos intervenir |
| Definición de negocio | Porcentaje de clientes que abandonan en el período |
| Fórmula | DISTINCTCOUNT(customer_id)[churn = 1] / DISTINCTCOUNT(customer_id) |
| Numerador | Clientes únicos con churn = 1 |
| Denominador | Clientes únicos en el corte |
| Unidad | % |
| Ventana temporal | Período de corte |
| Filtros de inclusión | registro_valido = 1 |
| Exclusiones | Ninguna |
| Dimensiones de segmentación | Contrato, internet, pago, antigüedad, protección, demografía |
| Meta o umbral | ≤ 22 % (verde); 22–26.5 % (amarillo); > 26.5 % (rojo) |
| Dirección deseada | Bajar |
| Métricas de balance | % MRR retenido (pondera valor), ARPU |
| Dueño | Gerencia de Retención |
| Riesgos de interpretación | No pondera el valor del cliente; el corte sobrerrepresenta el churn (no anualizar); promediar tasas de segmentos sin ponderar la sesga |
| Acción asociada | Si un segmento supera el 40 %, entra a la priorización P1/P2 |
| Medida DAX | [Tasa Churn] |
| Valor en el corte | 26.5 % |
| Fuente de datos | df_analitico (derivada de WA_Fn-UseC_-Telco-Customer-Churn.csv) / fact_clientes en Power BI |
| Frecuencia de actualización | Mensual, con cada corte de clientes (hoy existe un solo corte) |
| Granularidad | Cliente (cálculo) → segmento y mes (reporte) |
| Unidad de análisis | Cliente |

## 3. MRR perdido por churn

| Campo | Definición |
|---|---|
| Tipo | Volumen (USD) |
| Objetivo asociado | Proteger el ingreso recurrente |
| Decisión que soporta | Tamaño del problema y del presupuesto de retención |
| Definición de negocio | Ingreso mensual recurrente que se va con los clientes que abandonan |
| Fórmula | Σ cargo_mensual × churn |
| Numerador | — |
| Denominador | — (volumen) |
| Unidad | USD por mes |
| Ventana temporal | Período de corte |
| Filtros de inclusión | churn = 1 |
| Exclusiones | Ninguna |
| Dimensiones de segmentación | Contrato × internet (contribución), antigüedad, pago |
| Meta o umbral | ≤ 25 % del MRR total |
| Dirección deseada | Bajar |
| Métricas de balance | Clientes salvados, costo del programa |
| Dueño | CFO / Gerencia de Retención |
| Riesgos de interpretación | Depende del tamaño de la base; compárese como % del MRR. TotalCharges no es ingreso del período |
| Acción asociada | Priorizar los segmentos que concentran el 80 % de la pérdida |
| Medida DAX | [MRR Perdido] |
| Valor en el corte | USD 139,131 |
| Fuente de datos | df_analitico (derivada de WA_Fn-UseC_-Telco-Customer-Churn.csv) / fact_clientes en Power BI |
| Frecuencia de actualización | Mensual, con cada corte de clientes (hoy existe un solo corte) |
| Granularidad | Cliente (cálculo) → segmento y mes (reporte) |
| Unidad de análisis | Cliente |

## 4. Churn temprano (0–6 meses)

| Campo | Definición |
|---|---|
| Tipo | Tasa (cohorte de antigüedad) |
| Objetivo asociado | Mejorar la experiencia inicial |
| Decisión que soporta | Si reforzar el onboarding de clientes nuevos |
| Definición de negocio | Porcentaje de clientes con 0 a 6 meses de antigüedad que abandonan |
| Fórmula | Σ churn[antigüedad ≤ 6] / clientes[antigüedad ≤ 6] |
| Numerador | Clientes con antigüedad ≤ 6 y churn = 1 |
| Denominador | Clientes con antigüedad ≤ 6 |
| Unidad | % |
| Ventana temporal | Período de corte; cohorte por antigüedad |
| Filtros de inclusión | antiguedad_meses ≤ 6 |
| Exclusiones | Ninguna |
| Dimensiones de segmentación | Contrato, internet, pago |
| Meta o umbral | ≤ 45 % (verde); 45–52.9 % (amarillo); > 52.9 % (rojo) |
| Dirección deseada | Bajar |
| Métricas de balance | Costo de onboarding por cliente, satisfacción (no disponible) |
| Dueño | Customer Success |
| Riesgos de interpretación | Mezcla efecto contrato (los nuevos son mayoritariamente mes a mes) y sesgo de supervivencia |
| Acción asociada | Si sube, contactar a los clientes nuevos en los meses 1 a 3 (palanca L4) |
| Medida DAX | [Churn Temprano 0-6m] |
| Valor en el corte | 52.9 % |
| Fuente de datos | df_analitico (derivada de WA_Fn-UseC_-Telco-Customer-Churn.csv) / fact_clientes en Power BI |
| Frecuencia de actualización | Mensual, con cada corte de clientes (hoy existe un solo corte) |
| Granularidad | Cliente (cálculo) → segmento y mes (reporte) |
| Unidad de análisis | Cliente |

## 5. % clientes con contrato a plazo

| Campo | Definición |
|---|---|
| Tipo | Composición |
| Objetivo asociado | Estabilizar la base |
| Decisión que soporta | Si invertir en migración a contratos anuales |
| Definición de negocio | Proporción de clientes con contrato de uno o dos años |
| Fórmula | clientes[contrato ≠ 'Mes a mes'] / clientes |
| Numerador | Clientes con contrato de 1 o 2 años |
| Denominador | Clientes en el corte |
| Unidad | % |
| Ventana temporal | Período de corte |
| Filtros de inclusión | registro_valido = 1 |
| Exclusiones | Ninguna |
| Dimensiones de segmentación | Internet, antigüedad, pago |
| Meta o umbral | ≥ 50 % |
| Dirección deseada | Subir |
| Métricas de balance | ARPU (descuentos de migración), ROI de L1 |
| Dueño | Dirección Comercial |
| Riesgos de interpretación | Manipulable con descuentos (Goodhart): subirla comprando permanencia puede destruir margen |
| Acción asociada | Ofrecer migración solo a clientes de riesgo alto con ROI positivo |
| Medida DAX | [% Contrato a Plazo] |
| Valor en el corte | 45.0 % |
| Fuente de datos | df_analitico (derivada de WA_Fn-UseC_-Telco-Customer-Churn.csv) / fact_clientes en Power BI |
| Frecuencia de actualización | Mensual, con cada corte de clientes (hoy existe un solo corte) |
| Granularidad | Cliente (cálculo) → segmento y mes (reporte) |
| Unidad de análisis | Cliente |

## 6. % clientes con pago automático

| Campo | Definición |
|---|---|
| Tipo | Composición |
| Objetivo asociado | Reducir la fricción de pago |
| Decisión que soporta | Si incentivar el cambio desde cheque electrónico |
| Definición de negocio | Proporción de clientes que pagan con transferencia o tarjeta automática |
| Fórmula | clientes[pago_automatico = 1] / clientes |
| Numerador | Clientes con pago automático |
| Denominador | Clientes en el corte |
| Unidad | % |
| Ventana temporal | Período de corte |
| Filtros de inclusión | registro_valido = 1 |
| Exclusiones | Ninguna |
| Dimensiones de segmentación | Contrato, internet, antigüedad |
| Meta o umbral | ≥ 50 % |
| Dirección deseada | Subir |
| Métricas de balance | Costo del incentivo (L3), reclamos de facturación (no disponible) |
| Dueño | Facturación y cobranzas |
| Riesgos de interpretación | La asociación con menor churn puede reflejar el perfil del cliente y no causalidad |
| Acción asociada | Crédito de USD 10 por migrar a pago automático (palanca L3) y medir con grupo control |
| Medida DAX | [% Pago Automático] |
| Valor en el corte | 43.5 % |
| Fuente de datos | df_analitico (derivada de WA_Fn-UseC_-Telco-Customer-Churn.csv) / fact_clientes en Power BI |
| Frecuencia de actualización | Mensual, con cada corte de clientes (hoy existe un solo corte) |
| Granularidad | Cliente (cálculo) → segmento y mes (reporte) |
| Unidad de análisis | Cliente |

## 7. Adopción de protección

| Campo | Definición |
|---|---|
| Tipo | Tasa de adopción |
| Objetivo asociado | Aumentar el valor percibido del servicio de internet |
| Decisión que soporta | Si ofrecer el bundle de seguridad y soporte |
| Definición de negocio | Proporción de clientes con internet que tienen seguridad online o soporte técnico |
| Fórmula | clientes[tiene_proteccion = 1 y tiene_internet = 1] / clientes[tiene_internet = 1] |
| Numerador | Clientes con internet y seguridad o soporte |
| Denominador | Clientes con internet (excluye 'Sin servicio') |
| Unidad | % |
| Ventana temporal | Período de corte |
| Filtros de inclusión | tiene_internet = 1 |
| Exclusiones | Clientes sin internet |
| Dimensiones de segmentación | Tipo de internet, contrato, antigüedad |
| Meta o umbral | +5 pp sobre el corte |
| Dirección deseada | Subir |
| Métricas de balance | Costo del bundle (L2), ARPU |
| Dueño | Producto / Marketing de servicios |
| Riesgos de interpretación | Incluir clientes sin internet en el denominador subestima la adopción; la asociación no es causal |
| Acción asociada | Bundle de 3 meses sin costo para clientes de fibra sin protección (palanca L2) |
| Medida DAX | [Adopción Protección] |
| Valor en el corte | 53.7 % |
| Fuente de datos | df_analitico (derivada de WA_Fn-UseC_-Telco-Customer-Churn.csv) / fact_clientes en Power BI |
| Frecuencia de actualización | Mensual, con cada corte de clientes (hoy existe un solo corte) |
| Granularidad | Cliente (cálculo) → segmento y mes (reporte) |
| Unidad de análisis | Cliente |

## 8. ARPU (balance)

| Campo | Definición |
|---|---|
| Tipo | Razón (unit economics) |
| Objetivo asociado | Evitar retener destruyendo valor |
| Decisión que soporta | Límite a los descuentos de retención |
| Definición de negocio | Ingreso recurrente mensual promedio por cliente |
| Fórmula | Σ cargo_mensual / DISTINCTCOUNT(customer_id) |
| Numerador | MRR total |
| Denominador | Clientes únicos |
| Unidad | USD por cliente por mes |
| Ventana temporal | Período de corte |
| Filtros de inclusión | registro_valido = 1 |
| Exclusiones | Ninguna |
| Dimensiones de segmentación | Contrato, internet, estado del cliente |
| Meta o umbral | No caer más de 3 % frente al corte |
| Dirección deseada | Mantener |
| Métricas de balance | Es la métrica de balance del NSM |
| Dueño | CFO |
| Riesgos de interpretación | Puede subir porque se van los clientes de menor valor (efecto mezcla); calcularlo como razón de sumas |
| Acción asociada | Si cae más de 3 %, suspender o limitar la palanca de descuento (L1) |
| Medida DAX | [ARPU] |
| Valor en el corte | USD 64.76 |
| Fuente de datos | df_analitico (derivada de WA_Fn-UseC_-Telco-Customer-Churn.csv) / fact_clientes en Power BI |
| Frecuencia de actualización | Mensual, con cada corte de clientes (hoy existe un solo corte) |
| Granularidad | Cliente (cálculo) → segmento y mes (reporte) |
| Unidad de análisis | Cliente |

## 9. MRR en riesgo esperado

| Campo | Definición |
|---|---|
| Tipo | Volumen esperado (USD) |
| Objetivo asociado | Anticipar la pérdida (indicador líder) |
| Decisión que soporta | A quién contactar esta semana y con qué prioridad |
| Definición de negocio | Pérdida de MRR esperada en el próximo período si se repiten las tasas del corte |
| Fórmula | Σ prob_churn × cargo_mensual (clientes activos) |
| Numerador | — |
| Denominador | — (volumen esperado) |
| Unidad | USD por mes |
| Ventana temporal | Próximo período |
| Filtros de inclusión | churn = 0 (clientes activos) |
| Exclusiones | Clientes que ya abandonaron |
| Dimensiones de segmentación | Riesgo (alto/medio/bajo), segmento, palanca |
| Meta o umbral | −15 % frente al corte; alerta si sube más de 10 % |
| Dirección deseada | Bajar |
| Métricas de balance | Costo del programa, ROI |
| Dueño | Gerencia de Retención |
| Riesgos de interpretación | Depende de un modelo calibrado en un corte con churn sobrerrepresentado; usar para ordenar, no como pronóstico exacto |
| Acción asociada | Asignar las palancas a los clientes de riesgo alto (sección 10) |
| Medida DAX | [MRR en Riesgo Esperado] |
| Valor en el corte | USD 68,096 |
| Fuente de datos | df_analitico (derivada de WA_Fn-UseC_-Telco-Customer-Churn.csv) / fact_clientes en Power BI |
| Frecuencia de actualización | Mensual, con cada corte de clientes (hoy existe un solo corte) |
| Granularidad | Cliente (cálculo) → segmento y mes (reporte) |
| Unidad de análisis | Cliente |
