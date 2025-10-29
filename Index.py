"""
Valuation_Reasoner.py

A self-contained Python script that performs a Discounted Cash Flow (DCF) valuation and
produces a step-by-step, human-readable explanation of the reasoning.

Contents:
- A simple DCF implementation (project free cash flows, discount, terminal value)
- Functions that emit clear step-by-step textual explanations for each major calculation
- Example input and sample output printed when run
- A short README at the bottom (as a multiline string) describing reasoning design

Run: python Valuation_Reasoner.py

This file is suitable for use as a script or embedding inside a notebook cell.
"""

from dataclasses import dataclass, asdict
from typing import List, Tuple
import math
import json


@dataclass
class DCFInputs:
    current_revenue: float                   # Current (most recent) revenue
    # Year-by-year revenue growth rates (decimals)
    revenue_growth_rates: List[float]
    # Expected normalized free-cash-flow margin (decimals)
    profit_margin: float
    # Tax rate applied to operating profit (decimals)
    tax_rate: float
    # Portion of NOPAT reinvested (decimals) OR used within margin logic
    reinvestment_rate: float
    discount_rate: float                     # WACC or discount rate (decimals)
    # Perpetual growth rate for terminal value (decimals)
    terminal_growth_rate: float
    forecast_periods: int                    # Number of explicit projection years


def project_revenues(current_revenue: float, growth_rates: List[float]) -> List[float]:
    revenues = []
    r = current_revenue
    for g in growth_rates:
        r = r * (1 + g)
        revenues.append(r)
    return revenues


def project_free_cash_flows(revenues: List[float], margin: float, reinvestment_rate: float) -> List[float]:
    # Simplified: FCF = Revenue * margin * (1 - reinvestment_rate)
    # Another interpretation would separate NOPAT and reinvestment; this keeps logic compact and explainable.
    fcfs = []
    for rev in revenues:
        fcf = rev * margin * (1 - reinvestment_rate)
        fcfs.append(fcf)
    return fcfs


def discount_cash_flows(cash_flows: List[float], discount_rate: float) -> List[float]:
    discounted = []
    for i, cf in enumerate(cash_flows, start=1):
        pv = cf / ((1 + discount_rate) ** i)
        discounted.append(pv)
    return discounted


def terminal_value(last_cash_flow: float, discount_rate: float, terminal_growth: float) -> float:
    # Perpetuity growth model on next year's cash flow
    if discount_rate <= terminal_growth:
        raise ValueError(
            "Discount rate must be greater than terminal growth rate for Gordon Growth model.")
    tv = last_cash_flow * (1 + terminal_growth) / \
        (discount_rate - terminal_growth)
    return tv


def dcf_valuation(inputs: DCFInputs) -> Tuple[dict, str]:
    # 1) project revenues
    growths = inputs.revenue_growth_rates[: inputs.forecast_periods]
    revenues = project_revenues(inputs.current_revenue, growths)

    # 2) project FCFs
    fcfs = project_free_cash_flows(
        revenues, inputs.profit_margin, inputs.reinvestment_rate)

    # 3) discount projected FCFs
    discounted_fcfs = discount_cash_flows(fcfs, inputs.discount_rate)

    # 4) terminal value using last projected FCF
    last_fcf = fcfs[-1]
    tv = terminal_value(last_fcf, inputs.discount_rate,
                        inputs.terminal_growth_rate)
    # discount terminal value to present
    pv_tv = tv / ((1 + inputs.discount_rate) ** inputs.forecast_periods)

    # 5) enterprise value = sum discounted FCFs + PV of TV
    ev = sum(discounted_fcfs) + pv_tv

    # Pack numeric output
    numeric = {
        'revenues': revenues,
        'fcfs': fcfs,
        'discounted_fcfs': discounted_fcfs,
        'terminal_value': tv,
        'pv_terminal_value': pv_tv,
        'enterprise_value': ev
    }

    # Build explanation step-by-step
    explanation_lines = []
    explanation_lines.append(
        "Valuation method: Discounted Cash Flow (DCF) using projected revenues and a Gordon Growth terminal value.")
    explanation_lines.append("")
    explanation_lines.append("Inputs summary:")
    explanation_lines.append(json.dumps(asdict(inputs), indent=2))
    explanation_lines.append("")

    explanation_lines.append("Step 1 — Revenue projections:")
    for i, (g, rev) in enumerate(zip(growths, revenues), start=1):
        explanation_lines.append(
            f" Year {i}: applied growth {g*100:.2f}% to previous revenue. Projected revenue = {rev:,.2f}.")

    explanation_lines.append("")
    explanation_lines.append("Step 2 — Free Cash Flow (FCF) projections:")
    explanation_lines.append(
        " We calculate FCF as: FCF = Revenue × profit_margin × (1 - reinvestment_rate).")
    for i, (rev, fcf) in enumerate(zip(revenues, fcfs), start=1):
        explanation_lines.append(
            f" Year {i}: FCF = {rev:,.2f} × {inputs.profit_margin:.2%} × (1 - {inputs.reinvestment_rate:.2%}) = {fcf:,.2f}.")

    explanation_lines.append("")
    explanation_lines.append("Step 3 — Discount projected FCFs:")
    explanation_lines.append(
        f" We discount each year's FCF to present value using discount rate = {inputs.discount_rate:.2%} (PV = FCF / (1+rate)^t).")
    for i, (cf, pv) in enumerate(zip(fcfs, discounted_fcfs), start=1):
        explanation_lines.append(
            f" Year {i}: Discounted FCF = {cf:,.2f} / (1 + {inputs.discount_rate:.2%})^{i} = {pv:,.2f}.")

    explanation_lines.append("")
    explanation_lines.append("Step 4 — Terminal value (Gordon Growth):")
    explanation_lines.append(
        " We estimate a terminal value at the end of the explicit forecast using the Gordon Growth model:")
    explanation_lines.append(
        f" TV = Last projected FCF × (1 + terminal_growth) / (discount_rate - terminal_growth)")
    explanation_lines.append(
        f" Last FCF = {last_fcf:,.2f}; terminal growth = {inputs.terminal_growth_rate:.2%}; discount rate = {inputs.discount_rate:.2%}.")
    explanation_lines.append(f" Terminal Value (undiscounted) = {tv:,.2f}.")
    explanation_lines.append(
        f" Discounted terminal value (PV) to today = {pv_tv:,.2f}.")

    explanation_lines.append("")
    explanation_lines.append("Step 5 — Enterprise value:")
    explanation_lines.append(
        " Sum discounted FCFs + PV of terminal value = Enterprise Value (EV).")
    explanation_lines.append(
        f" Sum discounted FCFs = {sum(discounted_fcfs):,.2f}.")
    explanation_lines.append(f" PV(Terminal Value) = {pv_tv:,.2f}.")
    explanation_lines.append(f" Enterprise Value = {ev:,.2f}.")

    explanation_lines.append("")
    explanation_lines.append("Notes and caveats:")
    explanation_lines.append(
        " - This is a simplified DCF designed for clear explanations. In practice you may model NOPAT, depreciation, changes in working capital, and capex separately.")
    explanation_lines.append(
        " - Terminal value is sensitive to terminal_growth and discount_rate; ensure terminal_growth < discount_rate and choose economically plausible growth.")

    explanation = "\n".join(explanation_lines)

    return numeric, explanation


# Example input and run
if __name__ == '__main__':
    # Example assumptions (editable)
    inputs = DCFInputs(
        current_revenue=100_000_000.0,           # 100 million
        revenue_growth_rates=[0.20, 0.15, 0.12, 0.10, 0.08],
        profit_margin=0.18,                       # 18% FCF margin
        # used only for fuller models; present for clarity
        tax_rate=0.25,
        reinvestment_rate=0.20,                   # 20% of generated profit is reinvested
        discount_rate=0.10,                       # 10% discount rate
        terminal_growth_rate=0.03,                # 3% perpetual growth
        forecast_periods=5
    )

    numeric, explanation = dcf_valuation(inputs)

    # Print concise numeric summary
    print("--- DCF Valuation Result (Concise) ---")
    print(f"Enterprise Value: {numeric['enterprise_value']:,.2f}")
    print(f"Terminal Value (undiscounted): {numeric['terminal_value']:,.2f}")

    # Save a JSON of numeric outputs for easy ingestion
    with open('valuation_output.json', 'w') as f:
        json.dump(numeric, f, indent=2)

    print('\n--- Detailed Explanation (truncated to 4000 chars) ---')
    print(explanation[:4000])

    # Also write full explanation to a text file
    with open('valuation_explanation.txt', 'w') as f:
        f.write(explanation)

    # README (brief)
    README = """
README - Valuation Reasoner

Design intent:
 - Provide a transparent, step-by-step DCF reasoning engine that is easy to follow.
 - Keep calculations explicit: revenue projection -> FCF projection -> discounting -> terminal value -> EV.
 - Explanations mirror numeric steps so a reviewer can trace every number back to an assumption.

How to use:
 - Edit the `inputs` block in the `if __name__ == '__main__'` section to try different scenarios.
 - Run `python Valuation_Reasoner.py`. The script prints a concise result, writes `valuation_output.json` and `valuation_explanation.txt`.

Extensions you might add:
 - Model NOPAT, tax shields, capex and working capital changes explicitly.
 - Add a multiples-based approach (EV/EBITDA or P/E) for a hybrid valuation and a reconciliation section.
 - Add sensitivity tables for discount rate and terminal growth.

"""

    with open('README_Valuation_Reasoner.txt', 'w') as f:
        f.write(README)

    print('\nWrote files: valuation_output.json, valuation_explanation.txt, README_Valuation_Reasoner.txt')
