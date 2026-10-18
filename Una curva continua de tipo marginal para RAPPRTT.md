# Una curva continua de tipo marginal para RAPPRTT

## Definición de la prueba

En vez de interpolar una tasa efectiva aplicada a toda la renta, esta versión define un tipo marginal q(x) continuo y calcula el impuesto como el área bajo q(x), con una transferencia inicial. La renta disponible antes de cotizaciones es N(x)=x−T(x). Tipo positivo = impuesto; impuesto negativo = transferencia.

Los anclajes cumplen T(0)=−10.000,00 €, T(SMI 16.576,00 €)=0, T(mediana 24.497,17 €)=10% de la mediana y T(1.000.000 €)=500.000 € (50% efectivo). La curva marginal se interpola linealmente entre x=0, SMI, mediana y 1.000.000 €. Los tipos marginales requeridos para que las áreas den exactamente esos impuestos son: 90.00% a renta cero; 30.66% en el SMI; 31.20% en la mediana; y 70.81% en 1.000.000 €. Por encima de un millón se mantiene el último tipo marginal.

El tipo marginal a renta cero se eligió como 90% para esta prueba, no es un dato oficial ni está impuesto por los otros anclajes. El resultado mantiene la renta disponible creciente y hace que el tipo marginal decrezca durante la retirada de la transferencia bajo el SMI, y crezca desde el SMI en adelante.

En este escenario individual, la carga total propuesta cruza por encima de la aproximación actual cerca de 620.240,71 € de salario bruto anual. Por debajo de ese cruce el trabajador paga menos en el prototipo; por encima paga más. Este punto no es una conclusión sobre el balance de recaudación nacional.

## Resultados puntuales

| Renta bruta | Impuesto/transferencia | Tipo marginal propuesto | IRPF actual aprox. | SS trabajador | Carga actual total | Carga propuesta total | Diferencia propuesta−actual |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0,00 | -10.000,00 | 90.00% | 0,00 | 0,00 | 0,00 | -10.000,00 | -10.000,00 |
| 16.576,00 | 0,00 | 30.66% | 116,98 | 1.074,12 | 1.191,10 | 1.074,12 | -116,98 |
| 24.497,17 | 2.449,72 | 31.20% | 3.203,60 | 1.587,42 | 4.791,01 | 4.037,13 | -753,88 |
| 29.540,26 | 4.028,13 | 31.40% | 4.514,73 | 1.914,21 | 6.428,93 | 5.942,33 | -486,60 |
| 59.080,52 | 13.481,21 | 32.60% | 13.650,39 | 3.817,88 | 17.468,27 | 17.299,09 | -169,18 |
| 100.000,00 | 27.161,18 | 34.26% | 30.820,06 | 3.888,62 | 34.708,68 | 31.049,80 | -3.658,89 |
| 300.000,00 | 103.808,21 | 42.38% | 116.656,66 | 4.268,62 | 120.925,28 | 108.076,83 | -12.848,45 |
| 620.240,71 | 260.365,81 | 55.39% | 260.365,81 | 4.877,08 | 265.242,88 | 265.242,88 | 0,00 |
| 1.000.000,00 | 500.000,00 | 70.81% | 430.932,79 | 5.598,62 | 436.531,41 | 505.598,62 | 69.067,21 |

## Gráficas

![Renta disponible](https://private-us-east-1.manuscdn.com/sessionFile/YQ4IHdw4LXLKLbioQNuITZ/sandbox/dq8O6HIfxjL4AdtazDT5GG-images_1792317360316_na1fn_L2hvbWUvdWJ1bnR1L2JvcmluZ19haGhfaW5jb21lX2N1cnZlX25ldA.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvWVE0SUhkdzRMWExLTGJpb1FOdUlUWi9zYW5kYm94L2RxOE82SElmeGpMNEFkdGF6RFQ1R0ctaW1hZ2VzXzE3OTIzMTczNjAzMTZfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwySnZjbWx1WjE5aGFHaGZhVzVqYjIxbFgyTjFjblpsWDI1bGRBLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5NDcwMDgwMH19fV19&Key-Pair-Id=K2QY5QTL8JSY6C&Signature=MEUCIQDmXATL8ILnpq2XP8ZdBYnL8sExO-mOHsruIr8~QQgLgQIgCFx8y00phIA0GjAxDSRkwwngmsCR-vv1od8AqhctNOU_)

![Impuesto y cotizaciones](https://private-us-east-1.manuscdn.com/sessionFile/YQ4IHdw4LXLKLbioQNuITZ/sandbox/dq8O6HIfxjL4AdtazDT5GG-images_1792317360316_na1fn_L2hvbWUvdWJ1bnR1L2JvcmluZ19haGhfaW5jb21lX2N1cnZlX3RheA.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvWVE0SUhkdzRMWExLTGJpb1FOdUlUWi9zYW5kYm94L2RxOE82SElmeGpMNEFkdGF6RFQ1R0ctaW1hZ2VzXzE3OTIzMTczNjAzMTZfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwySnZjbWx1WjE5aGFHaGZhVzVqYjIxbFgyTjFjblpsWDNSaGVBLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5NDcwMDgwMH19fV19&Key-Pair-Id=K2QY5QTL8JSY6C&Signature=MEUCIHYUiYKcuFups~bgbO~4Z9R0cczKjs3vUfvJLFTPw1sNAiEA8s95N2wFLdkD2ZxxkrPfltTARPH0Ej1B3VJwdybfX1o_)

## Qué significa

La gráfica de renta disponible compara el salario bruto con lo que queda después del impuesto y las cotizaciones del trabajador. Por debajo del SMI, el impuesto es negativo: a renta cero el abono es 10.000 €. En el SMI el impuesto del modelo se hace cero; la cotización social se conserva por separado en la comparación.

Los anclajes se expresan como tasas efectivas acumuladas: 10% en la mediana y 50% a un millón. La curva marginal necesaria para generar esos acumulados no es la misma que la tasa efectiva: en esta prueba la marginal llega a cerca de 71% en el anclaje de un millón. La media y dos veces la media no son anclajes del nuevo diseño; se incluyen como puntos de lectura.

## Límites

El cálculo actual aproximado es para asalariado indefinido en Madrid, persona soltera sin hijos y sin otras rentas; conserva cotizaciones del trabajador y reemplaza solo IRPF. No incluye aportaciones patronales. La curva describe pagos por salario individual; no calcula recaudación nacional. Para comprobar si se mantiene o baja la recaudación hay que aplicar ambos esquemas a una distribución oficial de ingresos con pesos, y decidir si el beneficio se limita por hogar, renta familiar y otras fuentes de ingresos.

G=10.000 € y tipo marginal inicial 90% son opciones de diseño del experimento. Un 90% marginal inicial implica que de cada euro adicional ganado en renta muy baja, al principio se retienen unos 10 céntimos antes de cotizaciones. Esa retirada debe evaluarse por incentivos laborales y puede ajustarse cambiando el tipo inicial o el importe garantizado; cambiar uno obliga a recalibrar los tipos marginales de los otros anclajes.

El anclaje superior de un millón es hipotético, no el máximo oficial observado. Fuentes estadísticas y normativas de España: ver `boring_ahh_comparison.py` y `boring_ahh_comparison_report.md`.

Reproducción: `python3 boring_ahh_income_curve.py` genera este CSV, informe y gráficas.
