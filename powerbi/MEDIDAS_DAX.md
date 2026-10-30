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

### Promedio Churn Corte

Tasa de churn de la selección sin el filtro de antigüedad: línea de referencia del gráfico de ciclo de vida.

```dax
Promedio Churn Corte =
CALCULATE ( [Tasa Churn], REMOVEFILTERS ( dim_antiguedad ) )
```
Formato: `0.0%`

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
        v >= 0.75, "#138a3f",
        v >= 0.695, "#b07400",
        "#c8312f"
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
        v <= 0.45, "#138a3f",
        v <= 0.529, "#b07400",
        "#c8312f"
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
        v >= 64.76, "#138a3f",
        v >= 62.82, "#b07400",
        "#c8312f"
    )
```
Formato: `texto`

### Color Churn

Semáforo de la tasa de churn: verde ≤ 22 %, amarillo 22–26.5 %, rojo > 26.5 %.

```dax
Color Churn =
VAR v = ROUND ( [Tasa Churn], 3 )
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( [Tasa Churn] ), BLANK (),
        v <= 0.22, "#138a3f",
        v <= 0.265, "#b07400",
        "#c8312f"
    )
```
Formato: `texto`

### Color Plazo

Semáforo del % de contratos a plazo: verde ≥ 50 %, amarillo 45–50 %, rojo < 45 %.

```dax
Color Plazo =
VAR v = ROUND ( [% Contrato a Plazo], 3 )
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( [% Contrato a Plazo] ), BLANK (),
        v >= 0.5, "#138a3f",
        v >= 0.45, "#b07400",
        "#c8312f"
    )
```
Formato: `texto`

### Nota NSM

Brecha del NSM frente a la meta, en puntos porcentuales.

```dax
Nota NSM =
IF (
    ISBLANK ( [% MRR Retenido] ),
    BLANK (),
    FORMAT ( ( [% MRR Retenido] - 0.75 ) * 100, "+0.0;-0.0" ) & " pp vs. meta 75 %"
)
```
Formato: `texto`

### Nota MRR Perdido

Contexto de la tarjeta de MRR perdido.

```dax
Nota MRR Perdido =
FORMAT ( [% MRR Perdido], "0.0%" ) & " del MRR · meta ≤ 25 %"
```
Formato: `texto`

### Nota Churn

Contexto de la tarjeta de tasa de churn.

```dax
Nota Churn =
"Meta ≤ 22 % · " & FORMAT ( [Clientes Churn], "#,0" ) & " clientes"
```
Formato: `texto`

### Nota Churn Temprano

Contexto de la tarjeta de churn temprano.

```dax
Nota Churn Temprano =
"Meta ≤ 45 % · 49–72 m: " & FORMAT ( CALCULATE ( [Tasa Churn], dim_antiguedad[banda_antiguedad] = "49–72 m" ), "0.0%" )
```
Formato: `texto`

### Nota Plazo

Contexto de la tarjeta de contratos a plazo.

```dax
Nota Plazo =
"Meta ≥ 50 % · palanca L1"
```
Formato: `texto`

### Nota ARPU

Contexto de la tarjeta de ARPU.

```dax
Nota ARPU =
"Guardrail: no caer más de 3 %"
```
Formato: `texto`

### Color Barra Churn

Naranja si el grupo supera la tasa de churn de la selección; gris en otro caso.

```dax
Color Barra Churn =
IF ( [Tasa Churn] > CALCULATE ( [Tasa Churn], ALLSELECTED () ), "#eb6834", "#a9b6c6" )
```
Formato: `texto`

### Color Odds Ratio

Naranja si el factor aumenta el riesgo (OR ≥ 1); azul si lo reduce.

```dax
Color Odds Ratio =
IF ( [Odds Ratio] >= 1, "#eb6834", "#2a78d6" )
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

### Costo Salvado Focalizado

Costo por cliente salvado del programa focalizado (guardrail: < USD 200).

```dax
Costo Salvado Focalizado =
CALCULATE ( [Costo por Cliente Salvado], fact_clientes[riesgo] = "Alto" )
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

### Color ROI Focalizado

Verde si el ROI focalizado es ≥ 0.

```dax
Color ROI Focalizado =
IF ( [ROI Focalizado Riesgo Alto] >= 0, "#138a3f", "#c8312f" )
```
Formato: `texto`

### Color Costo Salvado

Verde si el costo por cliente salvado es < USD 200.

```dax
Color Costo Salvado =
IF ( [Costo Salvado Focalizado] < 200, "#138a3f", "#c8312f" )
```
Formato: `texto`

### Nota Riesgo Alto

Contexto de la tarjeta de clientes de riesgo alto.

```dax
Nota Riesgo Alto =
FORMAT ( DIVIDE ( [Clientes Riesgo Alto], [Clientes Activos] ), "0%" ) & " de los clientes activos"
```
Formato: `texto`

### Nota MRR Riesgo Alto

Contexto de la tarjeta de MRR de riesgo alto.

```dax
Nota MRR Riesgo Alto =
FORMAT ( DIVIDE ( [MRR Riesgo Alto], [MRR Activo] ), "0%" ) & " del MRR activo"
```
Formato: `texto`

### Nota MRR Riesgo Esperado

Concentración del MRR en riesgo esperado en el nivel alto.

```dax
Nota MRR Riesgo Esperado =
FORMAT ( DIVIDE ( CALCULATE ( [MRR en Riesgo Esperado], fact_clientes[riesgo] = "Alto" ), [MRR en Riesgo Esperado] ), "0%" ) & " está en riesgo alto"
```
Formato: `texto`

### Nota ROI Focalizado

Comparación del ROI focalizado con el ROI sin focalizar.

```dax
Nota ROI Focalizado =
"Sin focalizar: " & FORMAT ( [ROI Sin Focalizar], "+0%;-0%;0%" ) & " · escenario " & [Escenario Seleccionado]
```
Formato: `texto`

### Nota Costo Salvado

Contexto de la tarjeta de costo por cliente salvado.

```dax
Nota Costo Salvado =
"Meta < USD 200 por cliente"
```
Formato: `texto`

## 7. Simulador qué pasaría si

### Alternativa Seleccionada

Alternativa elegida (C1 = programa focalizado, por defecto).

```dax
Alternativa Seleccionada =
SELECTEDVALUE ( dim_alternativa[alternativa_id], "C1" )
```
Formato: `texto`

### Nombre Alternativa

Nombre de la alternativa elegida.

```dax
Nombre Alternativa =
SELECTEDVALUE ( dim_alternativa[alternativa], "C · Focalizado (riesgo alto)" )
```
Formato: `texto`

### Reducción Simulada

Reducción atribuible elegida en el parámetro; en blanco se usa la del escenario.

```dax
Reducción Simulada =
SELECTEDVALUE ( sim_reduccion[reduccion] )
```
Formato: `0%`

### Horizonte Simulado

Horizonte elegido en el parámetro; en blanco se usa el del escenario.

```dax
Horizonte Simulado =
SELECTEDVALUE ( sim_horizonte[horizonte_meses] )
```
Formato: `0`

### Sim Clientes

Clientes activos que recibe la alternativa elegida.

```dax
Sim Clientes =
VAR alt = [Alternativa Seleccionada]
RETURN
    COUNTROWS ( FILTER (
        fact_clientes,
        fact_clientes[churn] = 0
            && SWITCH (
                alt,
                "B", fact_clientes[contrato] = "Mes a mes",
                "C0", NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ),
                NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ) && fact_clientes[riesgo] = "Alto"
            )
    ) )
```
Formato: `#,0`

### Sim Clientes Salvados

Clientes que se espera salvar por corte con la alternativa y los supuestos elegidos.

```dax
Sim Clientes Salvados =
VAR esc = [Escenario Seleccionado]
VAR alt = [Alternativa Seleccionada]
VAR rSel = [Reducción Simulada]
VAR hSel = [Horizonte Simulado]
RETURN
    SUMX (
        FILTER (
        fact_clientes,
        fact_clientes[churn] = 0
            && SWITCH (
                alt,
                "B", fact_clientes[contrato] = "Mes a mes",
                "C0", NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ),
                NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ) && fact_clientes[riesgo] = "Alto"
            )
    ),
        VAR pal = IF ( alt = "B", "L1", fact_clientes[palanca_id] )
        VAR acc = LOOKUPVALUE ( supuestos_escenario[aceptacion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        VAR red = IF ( ISBLANK ( rSel ), LOOKUPVALUE ( supuestos_escenario[reduccion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal ), rSel )
        VAR mar = LOOKUPVALUE ( supuestos_escenario[margen], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        VAR hor = IF ( ISBLANK ( hSel ), LOOKUPVALUE ( supuestos_escenario[horizonte_meses], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal ), hSel )
        VAR con = LOOKUPVALUE ( supuestos_escenario[costo_contacto], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        VAR fij = LOOKUPVALUE ( supuestos_escenario[incentivo_fijo], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        VAR var_ = LOOKUPVALUE ( supuestos_escenario[incentivo_pct_cargo], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        RETURN
            fact_clientes[prob_churn] * acc * red
    )
```
Formato: `#,0.0`

### Sim MRR Salvado

MRR mensual que se espera conservar.

```dax
Sim MRR Salvado =
VAR esc = [Escenario Seleccionado]
VAR alt = [Alternativa Seleccionada]
VAR rSel = [Reducción Simulada]
VAR hSel = [Horizonte Simulado]
RETURN
    SUMX (
        FILTER (
        fact_clientes,
        fact_clientes[churn] = 0
            && SWITCH (
                alt,
                "B", fact_clientes[contrato] = "Mes a mes",
                "C0", NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ),
                NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ) && fact_clientes[riesgo] = "Alto"
            )
    ),
        VAR pal = IF ( alt = "B", "L1", fact_clientes[palanca_id] )
        VAR acc = LOOKUPVALUE ( supuestos_escenario[aceptacion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        VAR red = IF ( ISBLANK ( rSel ), LOOKUPVALUE ( supuestos_escenario[reduccion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal ), rSel )
        VAR mar = LOOKUPVALUE ( supuestos_escenario[margen], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        VAR hor = IF ( ISBLANK ( hSel ), LOOKUPVALUE ( supuestos_escenario[horizonte_meses], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal ), hSel )
        VAR con = LOOKUPVALUE ( supuestos_escenario[costo_contacto], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        VAR fij = LOOKUPVALUE ( supuestos_escenario[incentivo_fijo], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        VAR var_ = LOOKUPVALUE ( supuestos_escenario[incentivo_pct_cargo], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        RETURN
            fact_clientes[prob_churn] * fact_clientes[cargo_mensual] * acc * red
    )
```
Formato: `\$#,0`

### Sim Contribución

MRR salvado × margen × horizonte.

```dax
Sim Contribución =
VAR esc = [Escenario Seleccionado]
VAR alt = [Alternativa Seleccionada]
VAR rSel = [Reducción Simulada]
VAR hSel = [Horizonte Simulado]
RETURN
    SUMX (
        FILTER (
        fact_clientes,
        fact_clientes[churn] = 0
            && SWITCH (
                alt,
                "B", fact_clientes[contrato] = "Mes a mes",
                "C0", NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ),
                NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ) && fact_clientes[riesgo] = "Alto"
            )
    ),
        VAR pal = IF ( alt = "B", "L1", fact_clientes[palanca_id] )
        VAR acc = LOOKUPVALUE ( supuestos_escenario[aceptacion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        VAR red = IF ( ISBLANK ( rSel ), LOOKUPVALUE ( supuestos_escenario[reduccion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal ), rSel )
        VAR mar = LOOKUPVALUE ( supuestos_escenario[margen], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        VAR hor = IF ( ISBLANK ( hSel ), LOOKUPVALUE ( supuestos_escenario[horizonte_meses], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal ), hSel )
        VAR con = LOOKUPVALUE ( supuestos_escenario[costo_contacto], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        VAR fij = LOOKUPVALUE ( supuestos_escenario[incentivo_fijo], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        VAR var_ = LOOKUPVALUE ( supuestos_escenario[incentivo_pct_cargo], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        RETURN
            fact_clientes[prob_churn] * fact_clientes[cargo_mensual] * acc * red * mar * hor
    )
```
Formato: `\$#,0`

### Sim Costo

Costo de contacto + aceptación × incentivo.

```dax
Sim Costo =
VAR esc = [Escenario Seleccionado]
VAR alt = [Alternativa Seleccionada]
VAR rSel = [Reducción Simulada]
VAR hSel = [Horizonte Simulado]
RETURN
    SUMX (
        FILTER (
        fact_clientes,
        fact_clientes[churn] = 0
            && SWITCH (
                alt,
                "B", fact_clientes[contrato] = "Mes a mes",
                "C0", NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ),
                NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ) && fact_clientes[riesgo] = "Alto"
            )
    ),
        VAR pal = IF ( alt = "B", "L1", fact_clientes[palanca_id] )
        VAR acc = LOOKUPVALUE ( supuestos_escenario[aceptacion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        VAR red = IF ( ISBLANK ( rSel ), LOOKUPVALUE ( supuestos_escenario[reduccion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal ), rSel )
        VAR mar = LOOKUPVALUE ( supuestos_escenario[margen], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        VAR hor = IF ( ISBLANK ( hSel ), LOOKUPVALUE ( supuestos_escenario[horizonte_meses], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal ), hSel )
        VAR con = LOOKUPVALUE ( supuestos_escenario[costo_contacto], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        VAR fij = LOOKUPVALUE ( supuestos_escenario[incentivo_fijo], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        VAR var_ = LOOKUPVALUE ( supuestos_escenario[incentivo_pct_cargo], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
        RETURN
            con + acc * ( fij + var_ * fact_clientes[cargo_mensual] )
    )
```
Formato: `\$#,0`

### Sim ROI

ROI de la alternativa con los supuestos elegidos.

```dax
Sim ROI =
DIVIDE ( [Sim Contribución] - [Sim Costo], [Sim Costo] )
```
Formato: `+0%;-0%;0%`

### Sim Resultado Neto

Contribución − costo (USD).

```dax
Sim Resultado Neto =
[Sim Contribución] - [Sim Costo]
```
Formato: `\$#,0;-\$#,0`

### Sim Costo por Salvado

Costo por cliente salvado.

```dax
Sim Costo por Salvado =
DIVIDE ( [Sim Costo], [Sim Clientes Salvados] )
```
Formato: `\$#,0`

### Reducción de Equilibrio

Reducción atribuible mínima para que la alternativa no pierda dinero (ROI = 0).

```dax
Reducción de Equilibrio =
VAR k =
    VAR esc = [Escenario Seleccionado]
    VAR alt = [Alternativa Seleccionada]
    VAR rSel = BLANK ()
    VAR hSel = [Horizonte Simulado]
    RETURN
        SUMX (
            FILTER (
            fact_clientes,
            fact_clientes[churn] = 0
                && SWITCH (
                    alt,
                    "B", fact_clientes[contrato] = "Mes a mes",
                    "C0", NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ),
                    NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ) && fact_clientes[riesgo] = "Alto"
                )
        ),
            VAR pal = IF ( alt = "B", "L1", fact_clientes[palanca_id] )
            VAR acc = LOOKUPVALUE ( supuestos_escenario[aceptacion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
            VAR red = IF ( ISBLANK ( rSel ), LOOKUPVALUE ( supuestos_escenario[reduccion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal ), rSel )
            VAR mar = LOOKUPVALUE ( supuestos_escenario[margen], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
            VAR hor = IF ( ISBLANK ( hSel ), LOOKUPVALUE ( supuestos_escenario[horizonte_meses], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal ), hSel )
            VAR con = LOOKUPVALUE ( supuestos_escenario[costo_contacto], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
            VAR fij = LOOKUPVALUE ( supuestos_escenario[incentivo_fijo], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
            VAR var_ = LOOKUPVALUE ( supuestos_escenario[incentivo_pct_cargo], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
            RETURN
                fact_clientes[prob_churn] * fact_clientes[cargo_mensual] * acc * mar * hor
        )
RETURN
    DIVIDE ( [Sim Costo], k )
```
Formato: `0.0%`

### ROI Curva

ROI de la alternativa para cada valor del eje de reducción atribuible.

```dax
ROI Curva =
VAR contribucion =
    VAR esc = [Escenario Seleccionado]
    VAR alt = [Alternativa Seleccionada]
    VAR rSel = MAX ( eje_reduccion[reduccion_eje] )
    VAR hSel = [Horizonte Simulado]
    RETURN
        SUMX (
            FILTER (
            fact_clientes,
            fact_clientes[churn] = 0
                && SWITCH (
                    alt,
                    "B", fact_clientes[contrato] = "Mes a mes",
                    "C0", NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ),
                    NOT ( fact_clientes[palanca_id] IN { "L0", "NA" } ) && fact_clientes[riesgo] = "Alto"
                )
        ),
            VAR pal = IF ( alt = "B", "L1", fact_clientes[palanca_id] )
            VAR acc = LOOKUPVALUE ( supuestos_escenario[aceptacion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
            VAR red = IF ( ISBLANK ( rSel ), LOOKUPVALUE ( supuestos_escenario[reduccion], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal ), rSel )
            VAR mar = LOOKUPVALUE ( supuestos_escenario[margen], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
            VAR hor = IF ( ISBLANK ( hSel ), LOOKUPVALUE ( supuestos_escenario[horizonte_meses], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal ), hSel )
            VAR con = LOOKUPVALUE ( supuestos_escenario[costo_contacto], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
            VAR fij = LOOKUPVALUE ( supuestos_escenario[incentivo_fijo], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
            VAR var_ = LOOKUPVALUE ( supuestos_escenario[incentivo_pct_cargo], supuestos_escenario[escenario], esc, supuestos_escenario[palanca_id], pal )
            RETURN
                fact_clientes[prob_churn] * fact_clientes[cargo_mensual] * acc * red * mar * hor
        )
RETURN
    DIVIDE ( contribucion - [Sim Costo], [Sim Costo] )
```
Formato: `+0%;-0%;0%`

### ROI Cero

Línea de equilibrio (ROI = 0).

```dax
ROI Cero =
0
```
Formato: `0%`

### Color ROI Simulado

Verde si el ROI simulado es ≥ 0.

```dax
Color ROI Simulado =
IF ( [Sim ROI] >= 0, "#138a3f", "#c8312f" )
```
Formato: `texto`

### Nota Sim ROI

Lectura breve del ROI simulado.

```dax
Nota Sim ROI =
IF ( [Sim ROI] >= 0, "Rentable con estos supuestos", "Pierde dinero con estos supuestos" )
```
Formato: `texto`

### Lectura Simulador

Lectura automática del resultado del simulador.

```dax
Lectura Simulador =
VAR roi = [Sim ROI]
RETURN
    [Nombre Alternativa] & " · escenario " & [Escenario Seleccionado] & ": se intervienen "
        & FORMAT ( [Sim Clientes], "#,0" ) & " clientes, se salvan " & FORMAT ( [Sim Clientes Salvados], "0.0" )
        & " por corte y el ROI es " & FORMAT ( roi, "+0%;-0%;0%" ) & ". "
        & IF ( roi >= 0, "Resultado positivo: candidato a piloto con grupo control. ", "Resultado negativo: no ejecutar con estos supuestos. " )
        & "Para no perder dinero, la reducción atribuible debe superar " & FORMAT ( [Reducción de Equilibrio], "0.0%" ) & "."
```
Formato: `texto`

## Tablas calculadas del simulador

### dim_alternativa

Alternativas de decisión evaluadas en el simulador (tabla desconectada).

```dax
dim_alternativa =
DATATABLE ( "alternativa_id", STRING, "alternativa", STRING, "orden", INTEGER, { { "B", "B · Descuento masivo", 1 }, { "C0", "C · Sin focalizar", 2 }, { "C1", "C · Focalizado (riesgo alto)", 3 } } )
```

### sim_reduccion

Parámetro qué pasaría si: reducción atribuible del riesgo entre quienes aceptan (igual para todas las palancas).

```dax
sim_reduccion =
SELECTCOLUMNS ( GENERATESERIES ( 0, 40, 1 ), "reduccion", [Value] / 100 )
```

### sim_horizonte

Parámetro qué pasaría si: meses de permanencia adicional del cliente salvado.

```dax
sim_horizonte =
SELECTCOLUMNS ( GENERATESERIES ( 3, 24, 3 ), "horizonte_meses", [Value] )
```

### eje_reduccion

Eje de la curva de sensibilidad del ROI frente a la reducción atribuible.

```dax
eje_reduccion =
SELECTCOLUMNS ( GENERATESERIES ( 0, 20, 1 ), "reduccion_eje", [Value] / 100 )
```

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

Las tablas `dim_escenario`, `supuestos_escenario`, `drivers_modelo`, `dim_metricas`, `plan_monitoreo`, `dim_alternativa`, `sim_reduccion`, `sim_horizonte` y `eje_reduccion` están desconectadas: las leen las medidas con `SELECTEDVALUE`, `LOOKUPVALUE` o `MAX`.
