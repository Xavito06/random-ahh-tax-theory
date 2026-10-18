"""Random Ahh Physical Person Rent Taxation Theory (RAPPRTT).

Toy model: piecewise-linear *average/effective* tax rates anchored at
SMI (0%), median income (10%), mean income (20%), and the highest
recorded income (50%). Below SMI, the first segment is extrapolated,
so the effective rate and tax liability become negative.

All amounts must use the same currency and time period (e.g. gross annual
income and annual thresholds). This is an illustrative model, not tax advice.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TaxParameters:
    """Income anchors for one jurisdiction and one consistent time period."""

    smi: float
    median_income: float
    mean_income: float
    highest_recorded_income: float

    def validate(self) -> None:
        anchors = (self.smi, self.median_income, self.mean_income,
                   self.highest_recorded_income)
        if any(value < 0 for value in anchors):
            raise ValueError("Income thresholds cannot be negative.")
        if not (self.smi < self.median_income < self.mean_income
                < self.highest_recorded_income):
            raise ValueError(
                "Expected SMI < median income < mean income < highest recorded income."
            )


def effective_tax_rate(income: float, parameters: TaxParameters) -> float:
    """Return the effective tax rate as a decimal, e.g. 0.10 means 10%.

    Rate knots are (SMI, 0%), (median, 10%), (mean, 20%), and
    (maximum, 50%). Between knots, interpolate linearly. Below SMI,
    extrapolate the SMI-to-median segment, producing a negative rate.
    At and above the highest recorded income, cap the rate at 50%.
    """
    if income < 0:
        raise ValueError("Income cannot be negative.")
    parameters.validate()

    knots = (
        (parameters.smi, 0.00),
        (parameters.median_income, 0.10),
        (parameters.mean_income, 0.20),
        (parameters.highest_recorded_income, 0.50),
    )

    # Extrapolate the first segment below SMI, yielding a negative rate.
    if income < knots[0][0]:
        (x0, y0), (x1, y1) = knots[0], knots[1]
        return y0 + (income - x0) * (y1 - y0) / (x1 - x0)

    for (x0, y0), (x1, y1) in zip(knots, knots[1:]):
        if income <= x1:
            return y0 + (income - x0) * (y1 - y0) / (x1 - x0)

    return knots[-1][1]


def tax_amount(income: float, parameters: TaxParameters) -> float:
    """Return tax due; a negative result represents a modeled transfer/refund."""
    return income * effective_tax_rate(income, parameters)


def net_income(income: float, parameters: TaxParameters) -> float:
    """Return income after tax (or plus the modeled negative-tax transfer)."""
    return income - tax_amount(income, parameters)


def example() -> None:
    """Run with illustrative placeholder amounts; replace with real inputs."""
    params = TaxParameters(
        smi=16_000,
        median_income=30_000,
        mean_income=36_000,
        highest_recorded_income=1_000_000,
    )
    for income in (12_000, 16_000, 30_000, 36_000, 1_000_000):
        rate = effective_tax_rate(income, params)
        due = tax_amount(income, params)
        print(f"Income: {income:,.2f} | rate: {rate:.2%} | tax: {due:,.2f}")


if __name__ == "__main__":
    example()
