#!/usr/bin/env python3
"""Buy vs rent analysis tool for first-time home buyers.

Compares the total net cost of buying a home versus renting over a chosen
holding period, including mortgage amortization, taxes, insurance,
maintenance, closing costs, home appreciation, rent increases, and
investment opportunity cost.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass
class Inputs:
    home_price: float
    down_payment_pct: float
    mortgage_rate: float
    loan_term_years: int
    years_in_home: int
    property_tax_rate: float
    home_insurance_annual: float
    maintenance_rate: float
    hoa_monthly: float
    buy_closing_cost_pct: float
    sell_cost_pct: float
    home_appreciation_rate: float
    monthly_rent: float
    renters_insurance_monthly: float
    rent_increase_rate: float
    investment_return_rate: float


@dataclass
class Results:
    net_buy_cost: float
    net_rent_cost: float
    difference: float
    future_home_value: float
    remaining_loan_balance: float
    equity_after_sale: float


def annual_to_monthly(rate: float) -> float:
    return (1 + rate) ** (1 / 12) - 1


def remaining_balance(principal: float, monthly_rate: float, term_months: int, paid_months: int) -> float:
    if monthly_rate == 0:
        return max(principal * (term_months - paid_months) / term_months, 0)
    payment = principal * (monthly_rate * (1 + monthly_rate) ** term_months) / ((1 + monthly_rate) ** term_months - 1)
    return principal * (1 + monthly_rate) ** paid_months - payment * (((1 + monthly_rate) ** paid_months - 1) / monthly_rate)


def analyze(inp: Inputs) -> Results:
    months = inp.years_in_home * 12
    down_payment = inp.home_price * inp.down_payment_pct
    loan_principal = inp.home_price - down_payment

    mortgage_m = annual_to_monthly(inp.mortgage_rate)
    inv_m = annual_to_monthly(inp.investment_return_rate)
    rent_growth_m = annual_to_monthly(inp.rent_increase_rate)

    term_months = inp.loan_term_years * 12
    if mortgage_m == 0:
        mortgage_payment = loan_principal / term_months
    else:
        mortgage_payment = loan_principal * (mortgage_m * (1 + mortgage_m) ** term_months) / ((1 + mortgage_m) ** term_months - 1)

    monthly_tax = inp.home_price * inp.property_tax_rate / 12
    monthly_maintenance = inp.home_price * inp.maintenance_rate / 12
    monthly_home_insurance = inp.home_insurance_annual / 12

    buy_upfront = down_payment + (inp.home_price * inp.buy_closing_cost_pct)

    total_buy_cash_out = buy_upfront
    rent_cost_total = 0.0
    invest_balance = buy_upfront

    rent_now = inp.monthly_rent
    for _ in range(months):
        owner_monthly = mortgage_payment + monthly_tax + monthly_maintenance + monthly_home_insurance + inp.hoa_monthly
        renter_monthly = rent_now + inp.renters_insurance_monthly

        total_buy_cash_out += owner_monthly
        rent_cost_total += renter_monthly

        monthly_savings_if_renting = owner_monthly - renter_monthly
        invest_balance = invest_balance * (1 + inv_m) + max(monthly_savings_if_renting, 0)

        rent_now *= (1 + rent_growth_m)

    future_home_value = inp.home_price * ((1 + inp.home_appreciation_rate) ** inp.years_in_home)
    loan_balance = max(remaining_balance(loan_principal, mortgage_m, term_months, months), 0)
    sale_cost = future_home_value * inp.sell_cost_pct
    equity_after_sale = future_home_value - loan_balance - sale_cost

    net_buy_cost = total_buy_cash_out - equity_after_sale
    net_rent_cost = rent_cost_total - invest_balance
    difference = net_buy_cost - net_rent_cost

    return Results(
        net_buy_cost=net_buy_cost,
        net_rent_cost=net_rent_cost,
        difference=difference,
        future_home_value=future_home_value,
        remaining_loan_balance=loan_balance,
        equity_after_sale=equity_after_sale,
    )


def parse_args() -> Inputs:
    p = argparse.ArgumentParser(description="Buy vs rent calculator for first-time home buyers")
    p.add_argument("--home-price", type=float, required=True)
    p.add_argument("--down-payment-pct", type=float, default=0.10, help="e.g., 0.10 for 10%%")
    p.add_argument("--mortgage-rate", type=float, default=0.065, help="annual nominal rate, e.g., 0.065")
    p.add_argument("--loan-term-years", type=int, default=30)
    p.add_argument("--years-in-home", type=int, default=7)
    p.add_argument("--property-tax-rate", type=float, default=0.012)
    p.add_argument("--home-insurance-annual", type=float, default=1800)
    p.add_argument("--maintenance-rate", type=float, default=0.01)
    p.add_argument("--hoa-monthly", type=float, default=0)
    p.add_argument("--buy-closing-cost-pct", type=float, default=0.03)
    p.add_argument("--sell-cost-pct", type=float, default=0.06)
    p.add_argument("--home-appreciation-rate", type=float, default=0.03)
    p.add_argument("--monthly-rent", type=float, required=True)
    p.add_argument("--renters-insurance-monthly", type=float, default=20)
    p.add_argument("--rent-increase-rate", type=float, default=0.03)
    p.add_argument("--investment-return-rate", type=float, default=0.05)
    a = p.parse_args()
    return Inputs(**vars(a))


def money(v: float) -> str:
    return f"${v:,.0f}"


def main() -> None:
    inp = parse_args()
    r = analyze(inp)
    print("\n=== Buy vs Rent Analysis ===")
    print(f"Net cost to BUY over {inp.years_in_home} years: {money(r.net_buy_cost)}")
    print(f"Net cost to RENT over {inp.years_in_home} years: {money(r.net_rent_cost)}")

    if r.difference < 0:
        print(f"Buying is better by {money(abs(r.difference))} (lower net cost).")
    else:
        print(f"Renting is better by {money(abs(r.difference))} (lower net cost).")

    print("\nDetails:")
    print(f"Projected home value: {money(r.future_home_value)}")
    print(f"Remaining loan balance: {money(r.remaining_loan_balance)}")
    print(f"Estimated equity after sale costs: {money(r.equity_after_sale)}")


if __name__ == "__main__":
    main()
