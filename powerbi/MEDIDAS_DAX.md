# Medidas DAX del modelo — DataForge Consulting

Generado junto con `DataForge_Telco_Churn.SemanticModel`. Todas las medidas viven en la tabla `Medidas` y se organizan por carpetas.

## 1. Base

### Clientes

Clientes únicos en el contexto de filtro.

```dax
Clientes =
DISTINCTCOUNT ( fact_clientes[customer_id] )
```
Formato: `#,0`

### Clientes Churn

Clientes que abandonaron en el período de corte.

```dax
Clientes Churn =
CALCULATE ( [Clientes], fact_clientes[churn] = 1 )
```
Formato: `#,0`

### Clientes Activos

Clientes activos al cierre del corte.

```dax
Clientes Activos =
CALCULATE ( [Clientes], fact_clientes[churn] = 0 )
```
Formato: `#,0`

### MRR Total

Ingreso recurrente mensual de todos los clientes del corte (USD).

```dax
MRR Total =
SUM ( fact_clientes[cargo_mensual] )
```
Formato: `\$#,0`

### MRR Perdido

MRR de los clientes que abandonaron (USD por mes).

```dax
MRR Perdido =
SUM ( fact_clientes[mrr_perdido] )
```
Formato: `\$#,0`

### MRR Activo

MRR de los clientes activos (USD por mes).

```dax
MRR Activo =
CALCULATE ( [MRR Total], fact_clientes[churn] = 0 )
```
Formato: `\$#,0`

## 2. KPIs estratégicos

### % MRR Perdido

MRR perdido / MRR total del período de corte.

```dax
% MRR Perdido =
DIVIDE ( [MRR Perdido], [MRR Total] )
```
Formato: `0.0%`

### % MRR Retenido

North Star Metric: proporción del MRR que se conserva al cierre del período (1 − MRR perdido / MRR total).

```dax
% MRR Retenido =
IF ( ISBLANK ( [MRR Total] ), BLANK (), 1 - [% MRR Perdido] )
```
Formato: `0.0%`

### Tasa Churn

Clientes que abandonan / clientes del corte. Tasa del período de corte: no anualizar.

```dax
Tasa Churn =
DIVIDE ( [Clientes Churn], [Clientes] )
```
Formato: `0.0%`

### % Contrato a Plazo

Clientes con contrato de uno o dos años / clientes.

```dax
% Contrato a Plazo =
DIVIDE ( CALCULATE ( [Clientes], dim_contrato[es_plazo] = 1 ), [Clientes] )
```
Formato: `0.0%`

## 3. KPIs operativos

### Churn Temprano 0-6m

Tasa de churn de clientes con 0 a 6 meses de antigüedad.

```dax
Churn Temprano 0-6m =
CALCULATE ( [Tasa Churn], dim_antiguedad[banda_antiguedad] = "0–6 m" )
```
Formato: `0.0%`

### % Pago Automático

Clientes con transferencia o tarjeta automática / clientes.

```dax
% Pago Automático =
DIVIDE ( CALCULATE ( [Clientes], dim_pago[es_automatico] = 1 ), [Clientes] )
```
Formato: `0.0%`

### Adopción Protección

Clientes con internet que tienen seguridad online o soporte técnico / clientes con internet.

```dax
Adopción Protección =
DIVIDE (
    CALCULATE ( [Clientes], fact_clientes[tiene_internet] = 1, fact_clientes[tiene_proteccion] = 1 ),
    CALCULATE ( [Clientes], fact_clientes[tiene_internet] = 1 )
)
```
Formato: `0.0%`

### Clientes Riesgo Alto

Clientes activos con score de churn ≥ 40 %.

```dax
Clientes Riesgo Alto =
CALCULATE ( [Clientes Activos], fact_clientes[riesgo] = "Alto" )
```
Formato: `#,0`

### MRR Riesgo Alto

MRR de los clientes activos de riesgo alto.

```dax
MRR Riesgo Alto =
CALCULATE ( [MRR Activo], fact_clientes[riesgo] = "Alto" )
```
Formato: `\$#,0`

### MRR en Riesgo Esperado

Σ probabilidad de churn × cargo mensual de los clientes activos: pérdida esperada si se repiten las tasas del corte.

```dax
MRR en Riesgo Esperado =
VAR v = SUM ( fact_clientes[mrr_riesgo_esperado] )
RETURN
    IF ( v > 0, v )
```
Formato: `\$#,0`

## 4. Diagnóstico y balance

### ARPU

Métrica de balance: MRR / clientes (razón de sumas).

```dax
ARPU =
DIVIDE ( [MRR Total], [Clientes] )
```
Formato: `\$#,0.00`

### ARPU Churners

ARPU de los clientes que abandonaron.

```dax
ARPU Churners =
DIVIDE ( [MRR Perdido], [Clientes Churn] )
```
Formato: `\$#,0.00`

### Participación MRR Perdido

Participación del segmento en el MRR perdido de la selección.

```dax
Participación MRR Perdido =
DIVIDE ( [MRR Perdido], CALCULATE ( [MRR Perdido], ALLSELECTED ( fact_clientes ) ) )
```
Formato: `0.0%`

### Odds Ratio

Odds ratio ajustado del modelo logístico (> 1 aumenta el riesgo).

```dax
Odds Ratio =
MAX ( drivers_modelo[odds_ratio] )
```
Formato: `0.00`

## 5. Alertas

### Estado NSM

Semáforo del % MRR retenido: verde ≥ 75 %, amarillo 69.5–75 %, rojo < 69.5 %.

```dax
Estado NSM =
VAR v = ROUND ( [% MRR Retenido], 3 )
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( [% MRR Retenido] ), BLANK (),
        v >= 0.75, "Verde · en meta",
        v >= 0.695, "Amarillo · vigilar",
        "Rojo · crítico"
    )
```
Formato: `texto`

### Color NSM

Color del semáforo del NSM.

```dax
Color NSM =
VAR v = ROUND ( [% MRR Retenido], 3 )
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( [% MRR Retenido] ), BLANK (),
        v >= 0.75, "#0ca30c",
        v >= 0.695, "#b07400",
        "#d03b3b"
    )
```
Formato: `texto`

### Estado Churn Temprano

Semáforo: verde ≤ 45 %, amarillo 45–52.9 %, rojo > 52.9 %.

```dax
Estado Churn Temprano =
VAR v = ROUND ( [Churn Temprano 0-6m], 3 )
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( [Churn Temprano 0-6m] ), BLANK (),
        v <= 0.45, "Verde · en meta",
        v <= 0.529, "Amarillo · vigilar",
        "Rojo · crítico"
    )
```
Formato: `texto`

### Color Churn Temprano

Color del semáforo de churn temprano.

```dax
Color Churn Temprano =
VAR v = ROUND ( [Churn Temprano 0-6m], 3 )
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( [Churn Temprano 0-6m] ), BLANK (),
        v <= 0.45, "#0ca30c",
        v <= 0.529, "#b07400",
        "#d03b3b"
    )
```
Formato: `texto`

### Estado ARPU

Guardrail: verde ≥ USD 64.76, amarillo hasta −3 %, rojo < USD 62.82.

```dax
Estado ARPU =
VAR v = ROUND ( [ARPU], 3 )
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( [ARPU] ), BLANK (),
        v >= 64.76, "Verde · en meta",
        v >= 62.82, "Amarillo · vigilar",
        "Rojo · crítico"
    )
```
Formato: `texto`

### Color ARPU

Color del guardrail de ARPU.

```dax
Color ARPU =
VAR v = ROUND ( [ARPU], 3 )
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( [ARPU] ), BLANK (),
        v >= 64.76, "#0ca30c",
        v >= 62.82, "#b07400",
        "#d03b3b"
    )
```
Formato: `texto`

## 6. Simulador del programa

### Escenario Seleccionado

Escenario elegido en el segmentador (Base por defecto).

```dax
Escenario Seleccionado =
SELECTEDVALUE ( dim_escenario[escenario], "Base" )
```
Formato: `texto`

### Clientes Objetivo

Clientes activos con una palanca asignada.

```dax
Clientes Objetivo =
CALCULATE ( [Clientes Activos], NOT fact_clientes[palanca_id] IN { "L0", "NA" } )
```
Formato: `#,0`

### Clientes Salvados Esperados

Σ prob. de churn × aceptación × reducción atribuible (supuestos del escenario).

```dax
Clientes Salvados Esperados =
VAR esc = [Escenario Seleccionado]
RETURN
    SUMX (
        FILTER ( fact_clientes, fact_clientes[churn] = 0 && NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ) ),
        fact_clientes[prob_churn] * LOOKUPVALUE ( supuestos_escenario[aceptacion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], fact_clientes[palanca_id] ) * LOOKUPVALUE ( supuestos_escenario[reduccion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], fact_clientes[palanca_id] )
    )
```
Formato: `#,0.0`

### MRR Salvado Esperado

MRR mensual que se espera conservar con el programa.

```dax
MRR Salvado Esperado =
VAR esc = [Escenario Seleccionado]
RETURN
    SUMX (
        FILTER ( fact_clientes, fact_clientes[churn] = 0 && NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ) ),
        fact_clientes[prob_churn] * fact_clientes[cargo_mensual] * LOOKUPVALUE ( supuestos_escenario[aceptacion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], fact_clientes[palanca_id] ) * LOOKUPVALUE ( supuestos_escenario[reduccion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], fact_clientes[palanca_id] )
    )
```
Formato: `\$#,0`

### Contribución Salvada

MRR salvado × margen de contribución × horizonte (meses).

```dax
Contribución Salvada =
VAR esc = [Escenario Seleccionado]
RETURN
    SUMX (
        FILTER ( fact_clientes, fact_clientes[churn] = 0 && NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ) ),
        fact_clientes[prob_churn] * fact_clientes[cargo_mensual] * LOOKUPVALUE ( supuestos_escenario[aceptacion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], fact_clientes[palanca_id] ) * LOOKUPVALUE ( supuestos_escenario[reduccion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], fact_clientes[palanca_id] )
            * LOOKUPVALUE ( supuestos_escenario[margen], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], fact_clientes[palanca_id] ) * LOOKUPVALUE ( supuestos_escenario[horizonte_meses], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], fact_clientes[palanca_id] )
    )
```
Formato: `\$#,0`

### Costo Programa

Costo de contacto + aceptación × incentivo de cada palanca.

```dax
Costo Programa =
VAR esc = [Escenario Seleccionado]
RETURN
    SUMX (
        FILTER ( fact_clientes, fact_clientes[churn] = 0 && NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ) ),
        LOOKUPVALUE ( supuestos_escenario[costo_contacto], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], fact_clientes[palanca_id] )
            + LOOKUPVALUE ( supuestos_escenario[aceptacion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], fact_clientes[palanca_id] ) * ( LOOKUPVALUE ( supuestos_escenario[incentivo_fijo], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], fact_clientes[palanca_id] ) + LOOKUPVALUE ( supuestos_escenario[incentivo_pct_cargo], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], fact_clientes[palanca_id] ) * fact_clientes[cargo_mensual] )
    )
```
Formato: `\$#,0`

### ROI Programa

(Contribución salvada − costo) / costo, con los supuestos del escenario seleccionado.

```dax
ROI Programa =
DIVIDE ( [Contribución Salvada] - [Costo Programa], [Costo Programa] )
```
Formato: `+0%;-0%;0%`

### Costo por Cliente Salvado

Costo del programa por cliente salvado.

```dax
Costo por Cliente Salvado =
DIVIDE ( [Costo Programa], [Clientes Salvados Esperados] )
```
Formato: `\$#,0`

### ROI Focalizado Riesgo Alto

ROI del programa aplicado solo a clientes activos de riesgo alto.

```dax
ROI Focalizado Riesgo Alto =
CALCULATE ( [ROI Programa], fact_clientes[riesgo] = "Alto" )
```
Formato: `+0%;-0%;0%`

### ROI Sin Focalizar

ROI del programa aplicado a todos los clientes activos con palanca.

```dax
ROI Sin Focalizar =
CALCULATE ( [ROI Programa], REMOVEFILTERS ( dim_riesgo ) )
```
Formato: `+0%;-0%;0%`

### Costo Focalizado

Costo del programa focalizado.

```dax
Costo Focalizado =
CALCULATE ( [Costo Programa], fact_clientes[riesgo] = "Alto" )
```
Formato: `\$#,0`

### Contribución Focalizada

Contribución esperada del programa focalizado.

```dax
Contribución Focalizada =
CALCULATE ( [Contribución Salvada], fact_clientes[riesgo] = "Alto" )
```
Formato: `\$#,0`

### Decisión Sugerida

Regla de decisión según el ROI focalizado del escenario.

```dax
Decisión Sugerida =
VAR roi = [ROI Focalizado Riesgo Alto]
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( roi ), "Sin clientes objetivo en la selección",
        roi >= 0, "ROI focalizado positivo en el escenario " & [Escenario Seleccionado] & ": ejecutar como piloto con grupo control",
        "ROI negativo en el escenario " & [Escenario Seleccionado] & ": no escalar; revisar palancas y costos"
    )
```
Formato: `texto`

## Relaciones (modelo estrella, filtro simple dimensión → hechos)

| Desde (muchos) | Hacia (uno) |
|---|---|
| `fact_clientes[antiguedad_meses]` | `dim_antiguedad[antiguedad_meses]` |
| `fact_clientes[contrato]` | `dim_contrato[contrato]` |
| `fact_clientes[servicio_internet]` | `dim_internet[servicio_internet]` |
| `fact_clientes[metodo_pago]` | `dim_pago[metodo_pago]` |
| `fact_clientes[riesgo]` | `dim_riesgo[riesgo]` |
| `fact_clientes[palanca_id]` | `dim_palanca[palanca_id]` |
| `fact_clientes[segmento_id]` | `dim_segmento[segmento_id]` |
