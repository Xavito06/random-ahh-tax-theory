"""Comparación ilustrativa de impuestos sobre salarios en España, ejercicio 2025.

Uso:
    python3 boring_ahh_comparison.py
    python3 boring_ahh_comparison.py --max-recorded-income 750000 --output-dir ./comparacion

El escenario es una persona asalariada con contrato indefinido, residente en
Comunidad de Madrid, soltera, sin hijos ni otras rentas. Se calcula IRPF general
simplificado y cotizaciones a cargo de la persona trabajadora. No se incluyen
aportaciones empresariales, deducciones personales/autonómicas ni otros regímenes.

Las fuentes oficiales y los supuestos están documentados en el informe .md
que genera el script. No constituye asesoramiento fiscal.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Fuentes oficiales utilizadas (datos del año 2025 salvo salarios 2024):
# SMI 2025, 16.576 EUR/año: https://www.boe.es/buscar/act.php?id=BOE-A-2025-2576
# Salario medio 2024 29.540,26 y mediano 24.497,17 EUR/año:
#   https://www.ine.es/dyngs/Prensa/EAES2024.htm
# IRPF estatal 2025:
#   https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c15-calculo-impuesto-determinacion-cuotas-integras/gravamen-base-liquidable-general/gravamen-estatal.html
# IRPF autonómico Madrid 2025:
#   https://sede.agenciatributaria.gob.es/Sede/en_gb/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c15-calculo-impuesto-determinacion-cuotas-integras/gravamen-base-liquidable-general/gravamen-autonomico/comunidad-madrid.html
# Cotizaciones 2025, BOE-A-2025-3780:
#   https://www.boe.es/buscar/act.php?id=BOE-A-2025-3780
# El máximo de renta individual no se publica de forma identificable. El valor
# 1.000.000 EUR es un anclaje de escenario, editable por CLI, NO un dato oficial.

YEAR = 2025
SMI = 16_576.00
MEDIAN_WAGE = 24_497.17  # INE, 2024
MEAN_WAGE = 29_540.26    # INE, 2024
PERSONAL_MINIMUM = 5_550.00
EMPLOYMENT_EXPENSE = 2_000.00

# Renta general: escala estatal (tramos de base liquidable, tipos marginales).
STATE_BRACKETS = [
    (12_450.00, 0.095),
    (20_200.00, 0.120),
    (35_200.00, 0.150),
    (60_000.00, 0.185),
    (300_000.00, 0.225),
    (math.inf, 0.245),
]
# Comunidad de Madrid, ejercicio 2025.
MADRID_BRACKETS = [
    (13_362.22, 0.085),
    (19_004.63, 0.107),
    (35_425.68, 0.128),
    (57_320.40, 0.174),
    (math.inf, 0.205),
]

# Trabajador indefinido: contingencias comunes 4,70%, desempleo 1,55%,
# formación 0,10%, MEI 0,13%, aplicados a la base de cotización hasta el tope.
EMPLOYEE_RATE = 0.0470 + 0.0155 + 0.0010 + 0.0013
ANNUAL_MAX_CONTRIBUTION_BASE = 4_909.50 * 12
# Cotización adicional de solidaridad a cargo del trabajador, anualizada.
SOLIDARITY_BANDS = [
    (4_909.50 * 12, 5_400.45 * 12, 0.0015),
    (5_400.45 * 12, 7_364.25 * 12, 0.0017),
    (7_364.25 * 12, math.inf, 0.0019),
]

# Reducción AEAT 2025 por obtención de rendimientos del trabajo. Se presupone
# que el contribuyente cumple la condición de no superar 6.500 EUR de otras rentas.
def work_income_reduction(net_work_income: float) -> float:
    if net_work_income <= 0:
        return 0.0
    if net_work_income <= 14_852.00:
        return 7_302.00
    if net_work_income <= 17_673.52:
        return 7_302.00 - 1.75 * (net_work_income - 14_852.00)
    if net_work_income < 19_747.50:
        return 2_364.34 - 1.14 * (net_work_income - 17_673.52)
    return 0.0


def progressive_tax(base: float, brackets: list[tuple[float, float]]) -> float:
    """Tax a base with marginal-rate brackets expressed as (upper limit, rate)."""
    remaining = max(0.0, base)
    lower = 0.0
    tax = 0.0
    for upper, rate in brackets:
        width = min(remaining, upper - lower)
        if width > 0:
            tax += width * rate
            remaining -= width
        if remaining <= 0:
            break
        lower = upper
    return tax


def employee_social_security(gross_salary: float) -> float:
    base = min(max(gross_salary, 0.0), ANNUAL_MAX_CONTRIBUTION_BASE)
    contributions = base * EMPLOYEE_RATE
    for lower, upper, rate in SOLIDARITY_BANDS:
        taxable_slice = max(0.0, min(gross_salary, upper) - lower)
        contributions += taxable_slice * rate
    return contributions


def official_irpf(gross_salary: float) -> float:
    """Simplified regular IRPF: Madrid resident with one employment income."""
    social = employee_social_security(gross_salary)
    net_work = max(0.0, gross_salary - social - EMPLOYMENT_EXPENSE)
    reduction = work_income_reduction(net_work)
    taxable_base = max(0.0, net_work - reduction)
    gross_scale_tax = (
        progressive_tax(taxable_base, STATE_BRACKETS)
        + progressive_tax(taxable_base, MADRID_BRACKETS)
    )
    personal_minimum_tax = (
        progressive_tax(PERSONAL_MINIMUM, STATE_BRACKETS)
        + progressive_tax(PERSONAL_MINIMUM, MADRID_BRACKETS)
    )
    return max(0.0, gross_scale_tax - personal_minimum_tax)


def load_original_model():
    module_path = Path(__file__).with_name("boring_ahh_math.py")
    spec = importlib.util.spec_from_file_location("boring_ahh_math", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_rows(highest_anchor: float, points: int = 1_501):
    math_model = load_original_model()
    params = math_model.TaxParameters(
        smi=SMI,
        median_income=MEDIAN_WAGE,
        mean_income=MEAN_WAGE,
        highest_recorded_income=highest_anchor,
    )
    incomes = np.linspace(0, highest_anchor * 1.10, points)
    rows = []
    for income in incomes:
        social = employee_social_security(float(income))
        irpf = official_irpf(float(income))
        official_total = social + irpf
        theory_tax = math_model.tax_amount(float(income), params)
        # Linear comparator: one straight ramp in the effective tax rate from
        # 0% at SMI to 50% at the chosen upper anchor; extrapolate below SMI.
        linear_rate = 0.50 * (float(income) - SMI) / (highest_anchor - SMI)
        linear_tax = float(income) * linear_rate
        rows.append({
            "renta_bruta_eur": float(income),
            "irpf_oficial_aprox_eur": irpf,
            "cotizacion_trabajador_eur": social,
            "total_sistema_actual_eur": official_total,
            "impuesto_rapprtt_eur": theory_tax,
            "total_rapprtt_manteniendo_ss_eur": social + theory_tax,
            "tasa_lineal_efectiva": linear_rate,
            "impuesto_lineal_eur": linear_tax,
            "total_lineal_manteniendo_ss_eur": social + linear_tax,
        })
    return rows, params


def save_charts(rows, highest_anchor: float, output_dir: Path) -> tuple[Path, Path]:
    x = np.array([r["renta_bruta_eur"] for r in rows])
    actual = np.array([r["total_sistema_actual_eur"] for r in rows])
    theory = np.array([r["total_rapprtt_manteniendo_ss_eur"] for r in rows])
    linear = np.array([r["total_lineal_manteniendo_ss_eur"] for r in rows])

    plt.style.use("seaborn-v0_8-whitegrid")
    markers = ((SMI, "SMI"), (MEDIAN_WAGE, "Mediana"), (MEAN_WAGE, "Media"))
    fig, (ax, zoom) = plt.subplots(1, 2, figsize=(15, 6.5), gridspec_kw={"width_ratios": [1.6, 1]})
    for panel in (ax, zoom):
        panel.plot(x, actual, label="España 2025: IRPF aprox. + SS trabajador", linewidth=2.5)
        panel.plot(x, theory, label="RAPPRTT + SS trabajador actual", linewidth=2.5)
        panel.plot(x, linear, label="Tasa lineal 0→50% + SS trabajador", linewidth=2.2, linestyle="--")
        for value, _ in markers:
            panel.axvline(value, color="#7a7a7a", alpha=0.5, linestyle=":")
        panel.set_xlabel("Salario bruto anual (€)")
    for value, label in markers:
        zoom.text(value, 0.98, label, rotation=90, va="top", ha="right", fontsize=8,
                  transform=zoom.get_xaxis_transform())
    ax.set_title("Vista general")
    ax.set_ylabel("IRPF + cotización del trabajador (€)")
    ax.set_xlim(0, highest_anchor * 1.10)
    ax.set_ylim(bottom=min(-1000, min(theory.min(), linear.min()) * 1.08))
    zoom.set_title("Detalle de rentas bajas y medias")
    zoom.set_xlim(0, min(70_000, highest_anchor * 1.10))
    local = x <= 70_000
    local_min = min(actual[local].min(), theory[local].min(), linear[local].min())
    local_max = max(actual[local].max(), theory[local].max(), linear[local].max())
    zoom.set_ylim(min(-500, local_min * 1.08), local_max * 1.08)
    ax.legend(loc="upper left", frameon=True, fontsize=8)
    fig.suptitle("Carga anual del trabajador por nivel de salario bruto")
    fig.tight_layout()
    chart_amount = output_dir / "boring_ahh_comparison_amounts.png"
    fig.savefig(chart_amount, dpi=180)
    plt.close(fig)

    # Effective burden as a share of gross income; show the cash amount in the
    # first graph because the percentage is undefined at zero income.
    safe_x = np.where(x > 0, x, np.nan)
    fig, (ax, zoom) = plt.subplots(1, 2, figsize=(15, 6.5), gridspec_kw={"width_ratios": [1.6, 1]})
    for panel in (ax, zoom):
        panel.plot(x, 100 * actual / safe_x, label="Actual aproximado: IRPF + SS", linewidth=2.5)
        panel.plot(x, 100 * theory / safe_x, label="RAPPRTT + SS", linewidth=2.5)
        panel.plot(x, 100 * linear / safe_x, label="Lineal + SS", linewidth=2.2, linestyle="--")
        for value, _ in markers:
            panel.axvline(value, color="#7a7a7a", alpha=0.5, linestyle=":")
        panel.axhline(0, color="black", linewidth=0.8)
        panel.set_xlabel("Salario bruto anual (€)")
    for value, label in markers:
        zoom.text(value, 0.98, label, rotation=90, va="top", ha="right", fontsize=8,
                  transform=zoom.get_xaxis_transform())
    ax.set_title("Vista general")
    ax.set_ylabel("Carga total / salario bruto (%)")
    ax.set_xlim(0, highest_anchor * 1.10)
    zoom.set_title("Detalle de rentas bajas y medias")
    zoom.set_xlim(0, min(70_000, highest_anchor * 1.10))
    ax.legend(loc="upper left", frameon=True, fontsize=8)
    fig.suptitle("Tipo efectivo total sobre salario bruto")
    fig.tight_layout()
    chart_rate = output_dir / "boring_ahh_comparison_rates.png"
    fig.savefig(chart_rate, dpi=180)
    plt.close(fig)
    return chart_amount, chart_rate


def fmt(value: float) -> str:
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def save_report(rows, highest_anchor: float, output_dir: Path) -> Path:
    math_model = load_original_model()
    params = math_model.TaxParameters(SMI, MEDIAN_WAGE, MEAN_WAGE, highest_anchor)
    selected = sorted(set([SMI, MEDIAN_WAGE, MEAN_WAGE, 40_000, 60_000, 100_000, highest_anchor]))
    report_rows = []
    for income in selected:
        social = employee_social_security(income)
        irpf = official_irpf(income)
        theory_tax = math_model.tax_amount(income, params)
        linear_rate = 0.50 * (income - SMI) / (highest_anchor - SMI)
        linear_tax = income * linear_rate
        report_rows.append({
            "renta_bruta_eur": income,
            "irpf_oficial_aprox_eur": irpf,
            "cotizacion_trabajador_eur": social,
            "total_sistema_actual_eur": irpf + social,
            "impuesto_rapprtt_eur": theory_tax,
            "total_rapprtt_manteniendo_ss_eur": theory_tax + social,
            "total_lineal_manteniendo_ss_eur": linear_tax + social,
        })

    lines = [
        "# Comparación fiscal ilustrativa: RAPPRTT frente a España y una curva lineal",
        "",
        "**Referencia normativa:** ejercicio fiscal 2025. **Salarios de referencia:** INE 2024, últimos datos oficiales anuales localizados. **Escenario:** trabajador asalariado indefinido en Comunidad de Madrid, una persona, soltero, sin hijos, sin otras rentas ni deducciones particulares. Importes anuales en euros.",
        "",
        "## Qué compara",
        "",
        "El escenario actual combina IRPF general estatal y autonómico de Madrid con las cotizaciones a cargo del trabajador. La columna RAPPRTT reemplaza únicamente el IRPF por la fórmula del proyecto y conserva las cotizaciones sociales actuales. La alternativa lineal sustituye la curva de tasas del proyecto por una única recta efectiva que va de 0% en el SMI a 50% en el anclaje superior. Bajo el SMI, ambas propuestas prolongan esa recta hacia tasas negativas.",
        "",
        f"El anclaje superior se ha fijado en **{fmt(highest_anchor)} €** solo para el escenario. No se ha tratado como dato oficial: el máximo individual de renta/salario no está publicado como cifra identificable. Se puede cambiar al ejecutar el programa con `--max-recorded-income`.",
        "",
        "## Resultados en puntos de referencia",
        "",
        "| Salario bruto | IRPF actual aprox. | SS trabajador | Total actual aprox. | Impuesto RAPPRTT | Total RAPPRTT + SS | Total lineal + SS |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in report_rows:
        lines.append(
            f"| {fmt(r['renta_bruta_eur'])} | {fmt(r['irpf_oficial_aprox_eur'])} | "
            f"{fmt(r['cotizacion_trabajador_eur'])} | {fmt(r['total_sistema_actual_eur'])} | "
            f"{fmt(r['impuesto_rapprtt_eur'])} | {fmt(r['total_rapprtt_manteniendo_ss_eur'])} | "
            f"{fmt(r['total_lineal_manteniendo_ss_eur'])} |"
        )
    lines += [
        "",
        "## Método y límites",
        "",
        "El IRPF se aproxima aplicando las escalas progresivas estatales y madrileñas de 2025 a una base de empleo calculada como salario bruto menos cotizaciones del trabajador, 2.000 € de otros gastos deducibles y, cuando procede, la reducción general por rendimientos del trabajo de la AEAT. Se resta el efecto fiscal del mínimo personal de 5.550 €. Se supone que la persona cumple la condición de rentas distintas del trabajo no superiores a 6.500 €. La liquidación real puede variar por situación familiar, otras rentas, deducciones y reglas individuales; por eso el gráfico lo denomina IRPF aproximado.",
        "",
        "Las cotizaciones del trabajador incluyen contingencias comunes, desempleo indefinido, formación profesional, MEI y cotización de solidaridad por encima de la base máxima. Se excluyen las cotizaciones empresariales y accidentes de trabajo, que son a cargo del empleador. Así, ‘total’ significa carga directa de la persona trabajadora, no coste laboral total ni toda la financiación pública asociada al empleo.",
        "",
        "Los ingresos mediano y medio proceden de la Encuesta Anual de Estructura Salarial del INE para 2024. Se combinan con las reglas fiscales de 2025 porque son los datos salariales anuales más recientes publicados en las fuentes consultadas; existe, por tanto, una diferencia de año entre estadísticas de salarios y normativa fiscal. No se crea una población ficticia: las gráficas muestran curvas de función sobre una rejilla de salarios, no una estimación de recaudación nacional.",
        "",
        "La mediana y la media se usan como anclajes de tasa de la teoría, no como umbrales legales del sistema español. El SMI no equivale a una renta mínima vital y no es, por sí solo, un umbral fiscal. El modelo aplica una tasa efectiva a toda la renta (no marginal), tal como está implementado en `boring_ahh_math.py`.",
        "",
        "## Gráficas",
        "",
        "![Importe anual total](boring_ahh_comparison_amounts.png)",
        "",
        "![Tipo efectivo total](boring_ahh_comparison_rates.png)",
        "",
        "## Fuentes oficiales",
        "",
        "- AEAT, Manual práctico de Renta 2025, gravamen estatal: <https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c15-calculo-impuesto-determinacion-cuotas-integras/gravamen-base-liquidable-general/gravamen-estatal.html>",
        "- AEAT, Manual práctico de Renta 2025, gravamen autonómico de Madrid: <https://sede.agenciatributaria.gob.es/Sede/en_gb/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c15-calculo-impuesto-determinacion-cuotas-integras/gravamen-base-liquidable-general/gravamen-autonomico/comunidad-madrid.html>",
        "- AEAT, reducción por rendimientos del trabajo en 2025: <https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c03-rendimientos-trabajo/rendimiento-neto-trabajo-integrar-base-imponible/fase-3-determinacion-rendimiento-neto-reducido.html>",
        "- AEAT, ejemplo de mínimo personal y familiar de 5.550 €: <https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c15-calculo-impuesto-determinacion-cuotas-integras/ejemplo-practico-calculo-cuotas-integras-autonomica.html>",
        "- BOE, Real Decreto 87/2025, salario mínimo interprofesional de 2025: <https://www.boe.es/buscar/act.php?id=BOE-A-2025-2576>",
        "- INE, Encuesta Anual de Estructura Salarial 2024: <https://www.ine.es/dyngs/Prensa/EAES2024.htm>",
        "- BOE, Orden PJC/178/2025, bases y tipos de cotización a la Seguridad Social: <https://www.boe.es/buscar/act.php?id=BOE-A-2025-3780>",
        "",
        "## Archivos generados",
        "",
        "- `boring_ahh_comparison_amounts.png`: importe de la carga por renta.",
        "- `boring_ahh_comparison_rates.png`: tasa efectiva total por renta.",
        "- `boring_ahh_comparison.csv`: valores de la curva, para inspección y reutilización.",
    ]
    report_path = output_dir / "boring_ahh_comparison_report.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-recorded-income", type=float, default=1_000_000.0,
                        help="Anclaje superior hipotético (EUR/año); no es dato oficial.")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent,
                        help="Carpeta donde guardar PNG, CSV e informe.")
    args = parser.parse_args()
    if args.max_recorded_income <= MEAN_WAGE:
        parser.error("--max-recorded-income debe superar la renta media de referencia.")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows, _ = make_rows(args.max_recorded_income)
    csv_path = args.output_dir / "boring_ahh_comparison.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    chart_amount, chart_rate = save_charts(rows, args.max_recorded_income, args.output_dir)
    report_path = save_report(rows, args.max_recorded_income, args.output_dir)
    print(f"CSV: {csv_path}")
    print(f"Gráfica de importes: {chart_amount}")
    print(f"Gráfica de tasas: {chart_rate}")
    print(f"Informe metodológico: {report_path}")
    print(f"Anclajes oficiales: SMI={SMI:.2f}; mediana={MEDIAN_WAGE:.2f}; media={MEAN_WAGE:.2f}")
    print(f"Anclaje máximo hipotético: {args.max_recorded_income:.2f} EUR/año")


if __name__ == "__main__":
    main()
