# Prueba PCHIP: tasa efectiva frente a tasa marginal acumulada

Se movió el anclaje del 20% desde la renta media a **dos veces la renta media**. Con el dato INE usado (29.540,26 €), ese punto queda en **59.080,52 €**. Se mantuvo la mediana en 24.497,17 €, el SMI 2025 en 16.576 € y el anclaje superior supuesto en 1.000.000 €.

PCHIP (Piecewise Cubic Hermite Interpolating Polynomial) es una interpolación cúbica que conserva la monotonía de anclajes crecientes y evita oscilaciones espurias. Se comparan dos significados distintos de la curva: (A) los anclajes son tipos efectivos, de modo que impuesto = renta × tasa; (B) los anclajes son tipos marginales, y el impuesto acumulado es el área bajo esa tasa marginal.

| Renta bruta | IRPF actual aprox. | Cotización trabajador | Impuesto PCHIP efectivo | Total PCHIP efectivo + SS | Impuesto marginal integrado | Total marginal + SS |
|---:|---:|---:|---:|---:|---:|---:|
| 16.576,00 | 116,98 | 1.074,12 | 0,00 | 1.074,12 | 0,00 | 1.074,12 |
| 24.497,17 | 3.203,60 | 1.587,42 | 2.449,72 | 4.037,13 | 443,23 | 2.030,65 |
| 29.540,26 | 4.514,73 | 1.914,21 | 3.698,63 | 5.612,84 | 1.012,86 | 2.927,06 |
| 59.080,52 | 13.650,39 | 3.817,88 | 11.816,10 | 15.633,98 | 6.094,37 | 9.912,24 |
| 100.000,00 | 30.820,06 | 3.888,62 | 23.025,31 | 26.913,93 | 14.904,07 | 18.792,69 |
| 1.000.000,00 | 430.932,79 | 5.598,62 | 500.000,00 | 505.598,62 | 391.777,94 | 397.376,56 |

## Qué destaca

En la variante efectiva, cada tasa anclada se aplica a toda la renta. Por tanto, conserva la interpretación del prototipo actual, aunque el impuesto puede aumentar bruscamente al cruzar puntos donde cambia la pendiente de la tasa. PCHIP hace la tasa más suave, pero no convierte por sí mismo el impuesto en marginal.

En la variante marginal, el impuesto se acumula euro a euro integrando el tipo marginal. El total es continuo y cada incremento pequeño de renta afecta solo al impuesto del ingreso adicional. Los números de anclaje ahora describen tipos marginales locales, no porcentajes efectivos sobre toda la renta; por eso los impuestos acumulados son distintos y suelen menores que renta × porcentaje marginal.

Por debajo del SMI, ambas variantes reutilizan explícitamente el impuesto negativo efectivo del prototipo original para mantener esa hipótesis; no se extrapola la tasa marginal cúbica hacia abajo. Esto introduce una regla especial bajo el SMI y una unión no completamente suave. Se puede revisar por separado si se adopta definitivamente el enfoque marginal.

El sistema actual es una aproximación al IRPF general estatal y autonómico de Madrid 2025 más cotizaciones del trabajador para una persona soltera sin hijos y sin otras rentas. No incluye cotización patronal ni estima recaudación nacional. El máximo de 1.000.000 € es un supuesto editable, no una observación oficial.

![Comparación PCHIP](https://private-us-east-1.manuscdn.com/sessionFile/YQ4IHdw4LXLKLbioQNuITZ/sandbox/G9huFPtxqo6hBAdTa8jV1y-images_1792314715711_na1fn_L2hvbWUvdWJ1bnR1L2JvcmluZ19haGhfaW50ZXJwb2xhdGlvbl90ZXN0.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvWVE0SUhkdzRMWExLTGJpb1FOdUlUWi9zYW5kYm94L0c5aHVGUHR4cW82aEJBZFRhOGpWMXktaW1hZ2VzXzE3OTIzMTQ3MTU3MTFfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwySnZjbWx1WjE5aGFHaGZhVzUwWlhKd2IyeGhkR2x2Ymw5MFpYTjAucG5nIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzk0NzAwODAwfX19XX0_&Key-Pair-Id=K2QY5QTL8JSY6C&Signature=MEUCIAKaFpic5RQxtdXTZ7GO788SiP7NLBI0~mfpN9SbodWdAiEA1KMXBLbtwRWxJcjysNy2j-ue8MiJjNmdOnnRtFvs~68_)

## Archivos y repetición

Ejecutar `python3 boring_ahh_interpolation_test.py` regenera esta gráfica y el CSV. El prototipo original no se modifica.

Los datos de SMI, salarios y normativa se documentaron en `boring_ahh_comparison.py`; sus fuentes principales son BOE RD 87/2025, INE EAES 2024, AEAT Renta 2025 y BOE Orden PJC/178/2025.
