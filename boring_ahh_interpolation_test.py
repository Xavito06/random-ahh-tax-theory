"""Prueba comparativa de interpolación PCHIP para RAPPRTT.

Conserva intacto boring_ahh_math.py. Compara:
1) Tasa efectiva PCHIP entre 0% SMI, 10% mediana, 20% doble de la media, 50% máximo.
2) Tasa marginal PCHIP con los mismos anclajes, integrada desde SMI para obtener
   el impuesto acumulado. Para ingresos inferiores al SMI se conserva la regla
   de transferencia negativa original, explicitada en el informe.

Uso: python3 boring_ahh_interpolation_test.py
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import boring_ahh_comparison as base

OUT = Path(__file__).parent
SMI = base.SMI
MEDIAN = base.MEDIAN_WAGE
DOUBLE_MEAN = 2.0 * base.MEAN_WAGE
MAX_ANCHOR = 1_000_000.0  # supuesto, no dato oficial
XS = np.array([SMI, MEDIAN, DOUBLE_MEAN, MAX_ANCHOR], dtype=float)
YS = np.array([0.0, 0.10, 0.20, 0.50], dtype=float)


def pchip_slopes(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Derivadas PCHIP monotónicas, siguiendo Fritsch-Butland / PCHIP."""
    h = np.diff(x)
    delta = np.diff(y) / h
    n = len(x)
    d = np.zeros(n, dtype=float)
    if n == 2:
        d[:] = delta[0]
        return d
    for k in range(1, n - 1):
        if delta[k - 1] == 0 or delta[k] == 0 or np.sign(delta[k - 1]) != np.sign(delta[k]):
            d[k] = 0.0
        else:
            w1 = 2 * h[k] + h[k - 1]
            w2 = h[k] + 2 * h[k - 1]
            d[k] = (w1 + w2) / (w1 / delta[k - 1] + w2 / delta[k])
    d0 = ((2 * h[0] + h[1]) * delta[0] - h[0] * delta[1]) / (h[0] + h[1])
    if np.sign(d0) != np.sign(delta[0]):
        d0 = 0.0
    elif np.sign(delta[0]) != np.sign(delta[1]) and abs(d0) > abs(3 * delta[0]):
        d0 = 3 * delta[0]
    dn = ((2 * h[-1] + h[-2]) * delta[-1] - h[-1] * delta[-2]) / (h[-1] + h[-2])
    if np.sign(dn) != np.sign(delta[-1]):
        dn = 0.0
    elif np.sign(delta[-1]) != np.sign(delta[-2]) and abs(dn) > abs(3 * delta[-1]):
        dn = 3 * delta[-1]
    d[0], d[-1] = d0, dn
    return d


SLOPES = pchip_slopes(XS, YS)


def segment_coefficients(i: int):
    """Return coefficients a,b,c,d for y(t)=a+b*t+c*t²+d*t³, t in [0,1]."""
    h = XS[i + 1] - XS[i]
    y0, y1 = YS[i], YS[i + 1]
    m0, m1 = SLOPES[i], SLOPES[i + 1]
    a = y0
    b = h * m0
    c = 3 * (y1 - y0) - 2 * h * m0 - h * m1
    d = 2 * (y0 - y1) + h * (m0 + m1)
    return a, b, c, d, h


def pchip_value(value: float) -> float:
    if value <= XS[0]:
        return YS[0] + SLOPES[0] * (value - XS[0])
    if value >= XS[-1]:
        return YS[-1]
    i = int(np.searchsorted(XS, value, side="right") - 1)
    a, b, c, d, h = segment_coefficients(i)
    t = (value - XS[i]) / h
    return a + b * t + c * t**2 + d * t**3


def integrate_pchip_to(value: float) -> float:
    """Integrate marginal PCHIP from SMI to income; hold 50% above final knot."""
    if value <= SMI:
        return 0.0
    total = 0.0
    stop = min(value, MAX_ANCHOR)
    for i in range(len(XS) - 1):
        lo, hi = XS[i], min(XS[i + 1], stop)
        if hi <= lo:
            continue
        a, b, c, d, h = segment_coefficients(i)
        t = (hi - XS[i]) / h
        # dx = h dt; exact antiderivative of the cubic Hermite segment.
        total += h * (a*t + b*t**2/2 + c*t**3/3 + d*t**4/4)
        if stop <= XS[i + 1]:
            break
    if value > MAX_ANCHOR:
        total += (value - MAX_ANCHOR) * YS[-1]
    return total


def original_negative_tax(income: float) -> float:
    """Keep the project's negative-tax rule below SMI for this comparison."""
    rate = 0.10 * (income - SMI) / (MEDIAN - SMI)
    return income * rate


def pchip_effective_tax(income: float) -> float:
    if income < SMI:
        return original_negative_tax(income)
    return income * pchip_value(income)


def pchip_marginal_tax(income: float) -> float:
    if income < SMI:
        return original_negative_tax(income)
    return integrate_pchip_to(income)


def fmt(n: float) -> str:
    return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def run() -> None:
    grid = np.linspace(0, MAX_ANCHOR * 1.10, 1801)
    rows = []
    for income in grid:
        actual_total = base.official_irpf(float(income)) + base.employee_social_security(float(income))
        effective_tax = pchip_effective_tax(float(income))
        marginal_tax = pchip_marginal_tax(float(income))
        social = base.employee_social_security(float(income))
        rows.append({
            "salario_bruto_eur": float(income),
            "tasa_pchip_efectiva": pchip_value(float(income)) if income >= SMI else 0.10*(income-SMI)/(MEDIAN-SMI),
            "impuesto_pchip_efectiva": effective_tax,
            "tipo_marginal_pchip": pchip_value(float(income)),
            "impuesto_marginal_integrado": marginal_tax,
            "irpf_sistema_referencia_aprox": actual_total - social,
            "cotizacion_trabajador": social,
            "total_actual_aprox": actual_total,
            "total_pchip_efectiva_mas_ss": effective_tax + social,
            "total_pchip_marginal_mas_ss": marginal_tax + social,
        })

    csv_path = OUT / "boring_ahh_interpolation_test.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    plt.style.use("seaborn-v0_8-whitegrid")
    x = np.array([r["salario_bruto_eur"] for r in rows])
    actual = np.array([r["total_actual_aprox"] for r in rows])
    effective = np.array([r["total_pchip_efectiva_mas_ss"] for r in rows])
    marginal = np.array([r["total_pchip_marginal_mas_ss"] for r in rows])
    fig, (ax, zoom) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [1.5, 1]})
    for panel in (ax, zoom):
        panel.plot(x, actual, label="España 2025 aprox. + SS trabajador", lw=2.4)
        panel.plot(x, effective, label="PCHIP tasa efectiva + SS", lw=2.4)
        panel.plot(x, marginal, label="PCHIP marginal acumulada + SS", lw=2.4)
        for knot in (SMI, MEDIAN, DOUBLE_MEAN):
            panel.axvline(knot, color="#777777", alpha=.45, ls=":")
        panel.set_xlabel("Salario bruto anual (€)")
    ax.set_title("Vista general")
    ax.set_ylabel("IRPF/impuesto + cotización trabajador (€)")
    ax.set_xlim(0, MAX_ANCHOR*1.10)
    zoom.set_title("Detalle de rentas bajas y medias")
    zoom.set_xlim(0, 100_000)
    zoom.set_ylim(-500, max(actual[x <= 100_000].max(), effective[x <= 100_000].max(), marginal[x <= 100_000].max())*1.08)
    for knot, label in ((SMI,"SMI"),(MEDIAN,"Mediana"),(DOUBLE_MEAN,"2 × media")):
        zoom.text(knot, .98, label, rotation=90, va="top", ha="right", fontsize=8, transform=zoom.get_xaxis_transform())
    ax.legend(loc="upper left", fontsize=8)
    fig.suptitle("Prueba de interpolación PCHIP: dos interpretaciones del tipo")
    fig.tight_layout()
    graph = OUT / "boring_ahh_interpolation_test.png"
    fig.savefig(graph, dpi=180)
    plt.close(fig)

    chosen = sorted(set([SMI, MEDIAN, base.MEAN_WAGE, DOUBLE_MEAN, 100_000, MAX_ANCHOR]))
    tab = []
    for inc in chosen:
        s = base.employee_social_security(inc)
        a = base.official_irpf(inc)
        te = pchip_effective_tax(inc)
        tm = pchip_marginal_tax(inc)
        tab.append((inc, a, s, te, te+s, tm, tm+s))
    report = [
        "# Prueba PCHIP: tasa efectiva frente a tasa marginal acumulada", "",
        "Se movió el anclaje del 20% desde la renta media a **dos veces la renta media**. Con el dato INE usado (29.540,26 €), ese punto queda en **59.080,52 €**. Se mantuvo la mediana en 24.497,17 €, el SMI 2025 en 16.576 € y el anclaje superior supuesto en 1.000.000 €.", "",
        "PCHIP (Piecewise Cubic Hermite Interpolating Polynomial) es una interpolación cúbica que conserva la monotonía de anclajes crecientes y evita oscilaciones espurias. Se comparan dos significados distintos de la curva: (A) los anclajes son tipos efectivos, de modo que impuesto = renta × tasa; (B) los anclajes son tipos marginales, y el impuesto acumulado es el área bajo esa tasa marginal.", "",
        "| Renta bruta | IRPF actual aprox. | Cotización trabajador | Impuesto PCHIP efectivo | Total PCHIP efectivo + SS | Impuesto marginal integrado | Total marginal + SS |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for inc,a,s,te,tot_e,tm,tot_m in tab:
        report.append(f"| {fmt(inc)} | {fmt(a)} | {fmt(s)} | {fmt(te)} | {fmt(tot_e)} | {fmt(tm)} | {fmt(tot_m)} |")
    report += [
        "", "## Qué destaca", "",
        "En la variante efectiva, cada tasa anclada se aplica a toda la renta. Por tanto, conserva la interpretación del prototipo actual, aunque el impuesto puede aumentar bruscamente al cruzar puntos donde cambia la pendiente de la tasa. PCHIP hace la tasa más suave, pero no convierte por sí mismo el impuesto en marginal.", "",
        "En la variante marginal, el impuesto se acumula euro a euro integrando el tipo marginal. El total es continuo y cada incremento pequeño de renta afecta solo al impuesto del ingreso adicional. Los números de anclaje ahora describen tipos marginales locales, no porcentajes efectivos sobre toda la renta; por eso los impuestos acumulados son distintos y suelen menores que renta × porcentaje marginal.", "",
        "Por debajo del SMI, ambas variantes reutilizan explícitamente el impuesto negativo efectivo del prototipo original para mantener esa hipótesis; no se extrapola la tasa marginal cúbica hacia abajo. Esto introduce una regla especial bajo el SMI y una unión no completamente suave. Se puede revisar por separado si se adopta definitivamente el enfoque marginal.", "",
        "El sistema actual es una aproximación al IRPF general estatal y autonómico de Madrid 2025 más cotizaciones del trabajador para una persona soltera sin hijos y sin otras rentas. No incluye cotización patronal ni estima recaudación nacional. El máximo de 1.000.000 € es un supuesto editable, no una observación oficial.", "",
        "![Comparación PCHIP](boring_ahh_interpolation_test.png)", "",
        "## Archivos y repetición", "",
        "Ejecutar `python3 boring_ahh_interpolation_test.py` regenera esta gráfica y el CSV. El prototipo original no se modifica.", "",
        "Los datos de SMI, salarios y normativa se documentaron en `boring_ahh_comparison.py`; sus fuentes principales son BOE RD 87/2025, INE EAES 2024, AEAT Renta 2025 y BOE Orden PJC/178/2025."
    ]
    md = OUT / "boring_ahh_interpolation_test_report.md"
    md.write_text("\n".join(report)+"\n", encoding="utf-8")
    print("Puntos PCHIP:", list(zip(XS.tolist(), YS.tolist())))
    print("Pendientes PCHIP:", SLOPES.tolist())
    print("CSV:", csv_path)
    print("Gráfica:", graph)
    print("Informe:", md)
    print("Resultados:")
    for r in tab:
        print(" | ".join(fmt(v) for v in r))


if __name__ == "__main__":
    run()
