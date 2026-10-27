# PlayLoop: no ampliar CoinRush sin validar su recuperación

**Informe ejecutivo · Caso de negocio simulado de BigDataStack · Corte: 22/07/2024**

**Por cada 1.000 € invertidos en CoinRush, se han registrado aproximadamente 270 € netos hasta la extracción.**

## Decisión y contexto

Se propone aumentar un 60% el presupuesto de CoinRush. El canal aporta 2.800 de los 8.000 jugadores (35%) y tiene el menor coste por instalación de pago: 0,45 €. Sin embargo, el volumen y el bajo coste no se traducen en recuperación del gasto. Recomendamos **no aprobar el aumento por ahora**, mantener la inversión sujeta a seguimiento y revisar la calidad de la captación antes de escalar.

## Evidencia principal

| Canal | Instalaciones | CPI | Retención D7 | Conversión a pagador | ROAS neto observado |
|---|---:|---:|---:|---:|---:|
| CoinRush | 2.800 | 0,45 € | 2,4% | 0,11% | 0,27 |
| TikTok | 700 | 1,20 € | 19,5% | 1,00% | 1,06 |
| Google | 1.400 | 1,50 € | 18,7% | 1,79% | 1,16 |
| Meta | 1.600 | 1,80 € | 22,5% | 2,31% | 1,35 |
| Apple Search | 900 | 2,20 € | 25,4% | 2,56% | 1,42 |

CoinRush genera **338,31 € netos registrados frente a 1.259,99 € de adquisición**: saldo observado de **−921,68 €**, antes de otros costes. Los demás canales de pago cubren su gasto publicitario registrado. Su D1 del 37% no anticipaba una separación tan marcada: en D7 solo vuelve el 2,4%, frente al 18,7–25,4% de los demás canales. Solo tres jugadores de CoinRush realizan compras válidas.

La baja D7 se repite en España, México, Portugal e Italia (1,4–2,8%); no parece concentrada en un único país. Este desglose no calcula rentabilidad por país ni prueba que la falta de retención cause por sí sola la baja monetización.

**Apoyo visual:** [retención por canal](img/retencion_por_canal.png) · [conversión](img/conversion_por_canal.png) · [ROAS](img/roas_por_canal.png).

## Acción propuesta

Frenar el aumento de CoinRush y revisar campañas, creatividades y segmentación mediante una prueba acotada con criterios de éxito definidos antes de empezar. Priorizar la evaluación de Meta y Apple Search para posibles incrementos graduales, sin asumir que su retorno se mantendrá al escalar. Antes de reasignar presupuesto, validar los gastos elevados y comparar cohortes por semana de instalación con ingresos acumulados a una misma edad, por ejemplo D7 y D30. Monitorizar retención, conversión y recuperación del gasto conjuntamente.

## Alcance y límites

Resultados acumulados al corte, no LTV completo ni beneficio final. D7 incluye solo jugadores con al menos siete días observables; conversión y ROAS usan todos los jugadores y sus ingresos disponibles, por lo que **todavía no constituyen una comparación económica a igual edad de cohorte**. El ROAS se define aquí como compras netas de comisión más anuncios, dividido entre adquisición: 1 indica recuperación de ese gasto, antes de servidores, personal y otros costes. Se aplica la comisión del caso del 30% y se excluyen reembolsos y compras en MXN. Hay **600 ingresos publicitarios desconocidos** y **tres gastos superiores a 1.000 € pendientes de validación**. No se ha estimado su impacto; la recomendación es provisional y no demuestra que CoinRush sea irrecuperable ni que otros canales admitan inversión ilimitada.

**Entregas y reproducibilidad:** [informe interactivo Power BI](../powerbi/PlayLoop_Analytics.pbix), [modelo y medidas](powerbi.md), [análisis SQL](../notebooks/03_analisis.ipynb), [visualizaciones desde CSV limpios](../notebooks/04_visualizaciones.ipynb) y [corrección de fechas](correccion_fechas.md). Este proyecto simula una decisión; no afirma un impacto en una empresa real.
