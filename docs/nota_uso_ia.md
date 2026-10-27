# Nota sobre el uso de herramientas de IA

Esta nota la exige la sección 13 del enunciado. El equipo debe revisar y completar lo que está entre corchetes antes de entregar. El mismo texto aparece en el Anexo F del informe (`informe/nota_uso_ia.tex`).

## Herramienta y uso

El equipo usó **Claude** (Anthropic), un asistente de IA, de forma sustancial para:

- organizar el proyecto según el enunciado y el material de las sesiones 1 a 8;
- escribir y depurar el código del notebook (auditoría, limpieza, métricas, modelo logístico, simulación de ROI y diseño del piloto);
- generar el modelo semántico y el reporte de Power BI (TMDL y PBIR), incluidas las medidas DAX;
- redactar borradores del informe y de la presentación ejecutiva.

## Controles automáticos incluidos

- El notebook se ejecuta de principio a fin y contiene validaciones (`assert`): llave única, ausencia de nulos, reconciliación del MRR y de los churners con el archivo crudo, tasas en [0, 1] e integridad referencial del modelo estrella.
- Las cifras del dashboard se contrastaron con las del notebook: NSM 69.5 %, MRR perdido USD 139 mil y ROI focalizado +179 %.

## Verificación y decisiones del equipo

[Completar por el equipo: qué partes revisó cada integrante (por ejemplo, reglas de limpieza, fórmulas del diccionario, supuestos del simulador, lectura de los resultados), qué cambió respecto a la propuesta de la herramienta y qué decisiones tomó el equipo (por ejemplo, la elección del dataset, el usuario de la decisión, la North Star, los umbrales y la recomendación final).]

El equipo es responsable de todo el contenido entregado y puede explicar y defender cada análisis, supuesto y recomendación.
