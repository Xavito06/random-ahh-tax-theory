#set document(title: "Random Ahh Physical Person Rent Taxation Theory")
#set page(margin: 2.3cm)
#set text(size: 11pt)
#set par(leading: 0.72em, spacing: 0.8em)
#set heading(numbering: "1.")

= Random Ahh Physical Person Rent Taxation Theory

== Resumen

Este proyecto propone un modelo hipotético de tributación de la renta personal sin tramos legales convencionales. En lugar de asignar una tasa fija a cada intervalo, la tasa efectiva se interpola linealmente entre cuatro puntos de referencia. El modelo también extrapola la primera parte de la curva por debajo del salario mínimo interprofesional (SMI), de modo que la obligación tributaria sea negativa en ese rango.

Es un ejercicio matemático y no una descripción de la legislación vigente ni asesoramiento fiscal. Las cantidades de ejemplo son ficticias.

== Puntos de referencia

El modelo relaciona la renta bruta individual $x$ con una tasa efectiva $r(x)$ mediante estos anclajes:

#table(
  columns: (1fr, 1fr),
  [*Referencia de renta*], [*Tasa efectiva*],
  [SMI o renta mínima vital usada como umbral], [0%],
  [Renta mediana], [10%],
  [Renta media (promedio)], [20%],
  [Máxima renta registrada], [50%],
)

Los términos «renta mediana» y «renta media» no son intercambiables: la mediana es el valor central de la distribución y la media es el promedio aritmético. Para que la curva descrita aquí quede bien definida, se supone que SMI < mediana < media < máximo. Si los datos reales no cumplen este orden, habría que acordar otra definición o reordenar los puntos antes de aplicar el modelo.

== Fórmula

Entre dos anclajes consecutivos $(x_0, r_0)$ y $(x_1, r_1)$, la tasa se calcula por interpolación lineal:

$ r(x) = r_0 + (x - x_0) (r_1 - r_0) / (x_1 - x_0) $

La obligación tributaria se define como:

$ T(x) = x r(x) $

Y la renta neta resultante como:

$ N(x) = x - T(x) $

En el intervalo desde el SMI hasta la mediana, la expresión se simplifica a. Aquí $s$ representa el SMI y $m$ la renta mediana:

$ r(x) = 0.10 (x - s) / (m - s) $

Por debajo del SMI se prolonga esa misma recta, no se fija un nuevo tramo. Por tanto, $r(x) < 0$ si $0 <= x < s$, y $T(x)$ también es negativa para rentas positivas de ese intervalo. El valor absoluto de $T(x)$ representa una transferencia o devolución en este modelo, no un impuesto cobrado. Para rentas iguales o superiores al máximo, se mantiene la tasa en 50% (tope).

== Ejemplo ilustrativo

El archivo `boring_ahh_math.py` contiene una ejecución de ejemplo con umbrales ficticios: SMI 16.000, mediana 30.000, media 36.000 y máximo registrado 1.000.000 unidades monetarias por año. Con esos datos, una renta de 12.000 queda por debajo del SMI: la tasa efectiva calculada es aproximadamente -2,86%, por lo que la obligación matemática es aproximadamente -342,86. En el SMI exacto la tasa y el impuesto son cero; en los tres anclajes restantes las tasas son 10%, 20% y 50% respectivamente.

Las cantidades solo son comparables si todas usan la misma moneda, periodo y concepto de renta (por ejemplo, renta bruta anual). Antes de usar datos reales habría que especificar jurisdicción, año, definición del SMI y fuente para mediana, media y máximo registrado.

== Implementación

El módulo Python ofrece `TaxParameters` para introducir los cuatro valores, `effective_tax_rate` para obtener la tasa como decimal, `tax_amount` para calcular la obligación y `net_income` para calcular renta después de impuestos o transferencias. Los valores de ejemplo están separados de la lógica y deben sustituirse por datos coherentes.

== Supuestos y limitaciones

- La tasa calculada es una tasa efectiva aplicada a toda la renta, no una tasa marginal aplicada solo a la parte que supera un umbral.
- La interpolación lineal es una elección de diseño para completar la fórmula; no estaba especificada por los puntos de referencia por sí solos.
- El tramo inferior se extrapola sin límite adicional. Esto puede generar transferencias crecientes según la forma de la curva; no se incorpora un mínimo, máximo ni financiación del gasto.
- No se modelan deducciones, cotizaciones, composición familiar, inflación, evasión, ingresos no laborales ni efectos económicos.
- Una tasa negativa o una devolución de impuestos puede tener implicaciones legales y presupuestarias. Aquí se usa solo para satisfacer la hipótesis del proyecto.

== Archivos

- `boring_ahh_math.py`: implementación y ejemplo ejecutable.
- `boring_ahh_explanation.typ`: esta explicación en fuente Typst.


= Comparación con el sistema español y una alternativa lineal

== Alcance del ejercicio

Esta sección compara el modelo RAPPRTT con una aproximación del sistema español para el ejercicio fiscal 2025, y con una curva alternativa de tasa efectiva lineal. El escenario fiscal es una persona asalariada con contrato indefinido, residente en la Comunidad de Madrid, soltera, sin hijos, sin otras rentas y sin deducciones particulares. Los importes se expresan en euros anuales.

En la comparación, el IRPF aproximado y las cotizaciones a cargo del trabajador forman el sistema actual de referencia. En RAPPRTT y en la alternativa lineal, se reemplaza únicamente el IRPF y se mantienen las cotizaciones sociales actuales del trabajador. Así se distingue el efecto de la propuesta fiscal del de las cotizaciones. No se incluyen las aportaciones a cargo del empleador.

Los anclajes utilizados son SMI de 2025: 16.576 euros; salario bruto mediano de 2024: 24.497,17 euros; y salario bruto medio de 2024: 29.540,26 euros. Las dos últimas cifras son los datos anuales más recientes publicados por el INE en las fuentes consultadas. Se combinan con normativa fiscal de 2025, por lo que las referencias estadísticas y la normativa no corresponden exactamente al mismo año.

La renta máxima individual no está publicada como cifra identificable. Para poder representar el anclaje superior al 50%, se usa *1.000.000 euros anuales como supuesto ilustrativo*, no como dato oficial. El script de comparación permite modificar ese valor.

== Resultados en puntos de referencia

La columna «IRPF aprox.» es una estimación simplificada para el perfil indicado, no una liquidación individual oficial. «Total» suma ese IRPF estimado y las cotizaciones a cargo de la persona trabajadora.

#table(
  columns: (1.1fr, 1fr, 0.9fr, 1fr, 1fr, 1.15fr, 1.1fr),
  inset: 4pt,
  [*Salario bruto*], [*IRPF aprox.*], [*Cotizaciones trabajador*], [*Total actual aprox.*], [*Impuesto RAPPRTT*], [*RAPPRTT + cotizaciones*], [*Lineal + cotizaciones*],
  [16.576,00], [116,98], [1.074,12], [1.191,10], [0,00], [1.074,12], [1.074,12],
  [24.497,17], [3.203,60], [1.587,42], [4.791,01], [2.449,72], [4.037,13], [1.686,08],
  [29.540,26], [4.514,73], [1.914,21], [6.428,93], [5.908,05], [7.822,26], [2.108,92],
  [40.000,00], [7.241,39], [2.592,00], [9.833,39], [8.129,34], [10.721,34], [3.068,38],
  [60.000,00], [13.979,99], [3.819,26], [17.799,25], [12.564,96], [16.384,22], [5.143,93],
  [100.000,00], [30.820,06], [3.888,62], [34.708,68], [22.178,13], [26.066,76], [8.130,13],
  [1.000.000,00], [430.932,79], [5.598,62], [436.531,41], [500.000,00], [505.598,62], [505.598,62],
)

== Gráficas

La vista general permite ver los importes hasta el anclaje superior supuesto; el panel lateral amplía las rentas bajas y medias. La gráfica de tipos expresa la carga total del trabajador como proporción del salario bruto.

#figure(
  image("boring_ahh_comparison_amounts.png", width: 100%),
  caption: [Carga anual estimada: sistema español de referencia, RAPPRTT y curva lineal.],
)

#figure(
  image("boring_ahh_comparison_rates.png", width: 100%),
  caption: [Tipo efectivo total: carga estimada dividida por salario bruto.],
)

== Cómo leer la comparación

La alternativa «lineal» es una sola recta de tasa efectiva que parte del 0% en el SMI y llega al 50% en el anclaje superior supuesto. Ignora los anclajes de mediana y media; por eso no coincide con la curva RAPPRTT entre esos puntos. En ambas alternativas se prolonga la tasa por debajo del SMI y puede resultar negativa.

RAPPRTT aplica una tasa efectiva a toda la renta, no un tipo marginal solo a la parte que supera un umbral. En el cálculo agregado mostrado, el tipo efectivo y el impuesto de RAPPRTT se aplican a la renta bruta; después se suman las cotizaciones del trabajador que se mantienen en este escenario. Por ejemplo, en la mediana INE de 24.497,17 euros, la tasa RAPPRTT es 10%, por lo que el impuesto modelado es 2.449,72 euros. El total ilustrativo de RAPPRTT más cotizaciones es 4.037,13 euros.

== Método y límites

El IRPF se aproxima con las escalas progresivas estatal y autonómica de Madrid para 2025. La base de empleo parte del salario bruto y resta las cotizaciones del trabajador y 2.000 euros de gastos generales deducibles. Cuando corresponde, se incluye la reducción general de la AEAT por rendimientos del trabajo y se resta el efecto fiscal del mínimo personal de 5.550 euros. Se supone que se cumple la condición de no tener más de 6.500 euros de rentas distintas del trabajo. La declaración real depende de circunstancias personales, familiares, otras rentas, deducciones autonómicas y otros detalles que este escenario no modela.

Las cotizaciones consideradas son contingencias comunes, desempleo de contrato indefinido, formación profesional, mecanismo de equidad intergeneracional y la aportación de solidaridad del trabajador por remuneraciones superiores a la base máxima. Se excluyen las cotizaciones patronales y las primas por accidentes de trabajo, que corresponden al empleador. Por tanto, «total» no significa coste laboral total ni recaudación pública agregada.

Las gráficas trazan funciones sobre una rejilla de salarios y *no* estiman la recaudación nacional: no se ponderan millones de personas según su distribución de ingresos. El valor del máximo y la elección de Madrid son supuestos de este primer análisis. El SMI tampoco es lo mismo que la renta mínima vital ni constituye por sí solo un umbral fiscal.

== Fuentes oficiales

- AEAT, escala estatal del IRPF 2025: https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c15-calculo-impuesto-determinacion-cuotas-integras/gravamen-base-liquidable-general/gravamen-estatal.html
- AEAT, escala autonómica de Madrid 2025: https://sede.agenciatributaria.gob.es/Sede/en_gb/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c15-calculo-impuesto-determinacion-cuotas-integras/gravamen-base-liquidable-general/gravamen-autonomico/comunidad-madrid.html
- AEAT, reducción por rendimientos del trabajo 2025: https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c03-rendimientos-trabajo/rendimiento-neto-trabajo-integrar-base-imponible/fase-3-determinacion-rendimiento-neto-reducido.html
- AEAT, ejemplo de aplicación del mínimo personal de 5.550 euros: https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c15-calculo-impuesto-determinacion-cuotas-integras/ejemplo-practico-calculo-cuotas-integras-autonomica.html
- BOE, Real Decreto 87/2025 que fija el SMI de 2025: https://www.boe.es/buscar/act.php?id=BOE-A-2025-2576
- INE, Encuesta Anual de Estructura Salarial 2024, salario medio y mediano: https://www.ine.es/dyngs/Prensa/EAES2024.htm
- BOE, Orden PJC/178/2025 de bases y tipos de cotización a la Seguridad Social: https://www.boe.es/buscar/act.php?id=BOE-A-2025-3780

La lógica de cálculo y generación de las gráficas está en `boring_ahh_comparison.py`. El CSV de 1.501 puntos permite consultar la curva completa. Los gráficos incluidos son `boring_ahh_comparison_amounts.png` y `boring_ahh_comparison_rates.png`.
