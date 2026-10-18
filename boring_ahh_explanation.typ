

= Propuesta actual: curva marginal continua con impuesto negativo

Esta versión reemplaza como candidata principal a las pruebas de interpolación anteriores. Conserva aquellas secciones como experimentos comparativos, pero plantea una curva única de tipo marginal continuo para reflejar mejor el gráfico de referencia.

== Definición

Sea $x$ la renta bruta anual, $q(x)$ el tipo marginal, $T(x)$ el impuesto neto y $N(x)$ la renta disponible antes de cotizaciones sociales:

$ T(x) = -G + integral_0^x q(u) dif u $ 

$ N(x) = x - T(x) $

Un $T(x)$ positivo es impuesto; un valor negativo es una transferencia. Para este ensayo, $G = 10.000$ euros anuales. La curva se construye con tipos marginales que cambian linealmente —sin saltos entre tipos— entre renta cero, el SMI, la mediana y un millón de euros.

Los tipos marginales en los puntos de apoyo se fijaron para que el área acumulada cumpla exactamente los objetivos de impuesto: 90,00% a renta cero; 30,66% en el SMI; 31,20% en la mediana; y 70,81% en un millón. Así se obtiene T(0) = −10.000 euros, T(SMI) = 0, T(mediana) = 10% de la mediana y T(1.000.000) = 500.000 euros, equivalente a una tasa efectiva del 50% en ese punto.

El tipo marginal de 90% en renta cero es una decisión del experimento. Hace que la transferencia se reduzca a medida que aumentan los ingresos por debajo del SMI. La renta disponible aún aumenta con cada euro adicional, pero cerca de cero solo se retiene aproximadamente el 10% de cada euro antes de cotizaciones. Este efecto de retirada puede ser fuerte y debe evaluarse como parte central del diseño, no como un detalle técnico.

== Resultados individuales de referencia

La comparación conserva las cotizaciones sociales actuales del trabajador y reemplaza solo el IRPF por la curva propuesta. El IRPF actual sigue siendo aproximado para una persona asalariada indefinida, soltera y sin hijos en Madrid.

#set text(size: 8pt)
#table(
  columns: (0.95fr, 0.95fr, 0.85fr, 0.95fr, 0.85fr, 0.95fr, 0.95fr, 0.95fr),
  inset: 3pt,
  [*Renta bruta*], [*Impuesto / transferencia*], [*Marginal propuesto*], [*IRPF actual aprox.*], [*SS trabajador*], [*Carga actual total*], [*Carga propuesta total*], [*Diferencia*],
  [0], [-10.000,00], [90,00%], [0,00], [0,00], [0,00], [-10.000,00], [-10.000,00],
  [SMI 16.576], [0,00], [30,66%], [116,98], [1.074,12], [1.191,10], [1.074,12], [-116,98],
  [Mediana 24.497], [2.449,72], [31,20%], [3.203,60], [1.587,42], [4.791,01], [4.037,13], [-753,88],
  [Media 29.540], [4.028,13], [31,40%], [4.514,73], [1.914,21], [6.428,93], [5.942,33], [-486,60],
  [2 × media 59.081], [13.481,21], [32,60%], [13.650,39], [3.817,88], [17.468,27], [17.299,09], [-169,18],
  [100.000], [27.161,18], [34,26%], [30.820,06], [3.888,62], [34.708,68], [31.049,80], [-3.658,89],
  [300.000], [103.808,21], [42,38%], [116.656,66], [4.268,62], [120.925,28], [108.076,83], [-12.848,45],
  [620.241], [260.365,81], [55,39%], [260.365,81], [4.877,07], [265.242,88], [265.242,88], [0,00],
  [1.000.000], [500.000,00], [70,81%], [430.932,79], [5.598,62], [436.531,41], [505.598,62], [69.067,21],
)
#set text(size: 11pt)

En este escenario individual, la carga total propuesta cruza por encima de la aproximación actual cerca de *620.241 euros anuales*. Por debajo del cruce la persona paga menos según el prototipo; por encima paga más. Esto no demuestra neutralidad presupuestaria ni permite inferir recaudación nacional.

== Visualización

La primera gráfica representa la renta disponible después del impuesto propuesto y las cotizaciones sociales actuales del trabajador. La línea discontinua es el salario bruto sin deducciones. La segunda separa el impuesto o transferencia del modelo y la carga total aproximada.

#figure(
  image("boring_ahh_income_curve_net.png", width: 100%),
  caption: [Renta disponible individual según la renta bruta.],
)

#figure(
  image("boring_ahh_income_curve_tax.png", width: 100%),
  caption: [Impuesto/transferencia de la curva propuesta frente a la carga total aproximada actual.],
)

== Conclusiones y decisiones pendientes

La curva cumple de forma continua los anclajes de impuesto cero en el SMI, 10% efectivo en la mediana y 50% efectivo en un millón, y contempla una transferencia de 10.000 euros a renta cero. En el ensayo, reduce la carga total en la mediana en unos 754 euros y en 100.000 euros en unos 3.659 euros, pero la eleva en unos 69.067 euros a un millón. En el punto de dos veces la media, la carga es casi igual a la referencia actual.

La intensidad de la retirada del impuesto negativo es una limitación importante: con una garantía de 10.000 euros y el SMI de 16.576 euros, la curva necesita un tipo marginal de 90% a renta cero para satisfacer todos los anclajes elegidos y mantener tipos crecientes desde el SMI. El tipo disminuye durante la retirada de la ayuda hasta 30,66% en el SMI. Cerca de cero, cada euro adicional de ingresos reduce la transferencia en unos 90 céntimos antes de cotizaciones.

La comparación depende del perfil fiscal y de los supuestos utilizados. El cruce de 620.241 euros es individual, no un punto de equilibrio presupuestario. Para probar si la recaudación total se mantiene o baja habría que aplicar el sistema actual y el propuesto a la misma distribución oficial de rentas, ponderando personas y hogares y definiendo cómo se cuenta la transferencia garantizada.

El anclaje de un millón sigue siendo un supuesto ilustrativo, no una cifra oficial máxima. El archivo `boring_ahh_income_curve.py` contiene la fórmula experimental y genera el CSV y las gráficas; las fuentes fiscales y salariales oficiales siguen documentadas en `boring_ahh_comparison.py` y en la sección anterior.
