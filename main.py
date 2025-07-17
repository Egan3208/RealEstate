# Extending the classes as requested
# Importing necessary modules
from typing import List
import math
from CreditCards import ALL_CARDS
from CapitalAccounts import ALL_ACCOUNTS


class FinancialStatus:
    def __init__(self, employer_income, fixed_expenses, credit_cards=None, capital_accounts=None):
        self.employer_income = employer_income
        self.fixed_expenses = fixed_expenses
        self.credit_cards = credit_cards if credit_cards else ALL_CARDS
        self.capital_accounts = capital_accounts if capital_accounts else ALL_ACCOUNTS

    def total_credit_card_debt(self):
        return sum(card.balance for card in self.credit_cards)

    def total_minimum_payments(self):
        return sum(card.minimum_payment() for card in self.credit_cards)

    def total_planned_payments(self):
        return sum(card.planned_payment() for card in self.credit_cards)
    
    def total_monthly_debt(self):
        return self.fixed_expenses + self.total_planned_payments()

    def monthly_cash_flow(self):
        return self.employer_income - self.total_monthly_debt()

    def dti_ratio(self):
        return self.total_monthly_debt() / self.employer_income

    def total_liquid_accounts(self):
        return sum(acc.balance for acc in self.capital_accounts if acc.is_liquid_account())

    def total_retirement_accounts(self):
        return sum(acc.balance for acc in self.capital_accounts if acc.is_retirement_account())
    
    def total_accounts(self):
        return (self.total_liquid_accounts() + self.total_retirement_accounts())

    def summary(self):
        return {
            'total_liquid_accounts': self.total_liquid_accounts(),
            'total_retirement_accounts': self.total_retirement_accounts(),
            'total_accounts': self.total_accounts(),
            'employer_income': self.employer_income,
            'fixed_expenses': self.fixed_expenses,
            'total_credit_card_debt': self.total_credit_card_debt(),
            'total_planned_credit_payments': self.total_planned_payments(),
            'monthly_cash_flow': self.monthly_cash_flow(),
            'dti_ratio': self.dti_ratio()
        }

    def __repr__(self):
        return (f"<FinancialStatus liquid=${self.total_liquid_accounts()}, retirement=${self.total_retirement_accounts()}, "
                f"CC_debt=${self.total_credit_card_debt()}, income=${self.employer_income}/mo>")


class Property:
    def __init__(self, name, selling_price, current_rent_per_unit, num_units, appraised_rent_per_unit=None):
        self.name = name
        self.selling_price = selling_price
        self.current_rent_per_unit = current_rent_per_unit
        self.appraised_rent_per_unit = appraised_rent_per_unit or current_rent_per_unit
        self.num_units = num_units


class PropertyFinder:
    def __init__(self, financial_status):
        self.financial_status = financial_status

    def estimate_price_by_down_payment(self, down_payment_percent=0.035, closing_cost_percent=0.03, reserve_months=3, piti_estimate=0):
        liquid_cash = self.financial_status.total_liquid_accounts()
        reserve_requirement = piti_estimate * reserve_months
        total_upfront_needed = (down_payment_percent + closing_cost_percent) * 1 + reserve_requirement  # multiplier
        if total_upfront_needed <= 0:
            return 0
        est_price = (liquid_cash - reserve_requirement) / (down_payment_percent + closing_cost_percent)
        return max(est_price, 0)

    def estimate_price_by_dti(self, dti_limit=0.43, apr=0.07, loan_term_years=30, monthly_taxes_insurance=0):
        max_housing_payment = self.financial_status.employer_income * dti_limit - monthly_taxes_insurance
        monthly_rate = apr / 12
        total_payments = loan_term_years * 12
        if monthly_rate == 0:
            loan_amount = max_housing_payment * total_payments
        else:
            loan_amount = max_housing_payment * (1 - math.pow(1 + monthly_rate, -total_payments)) / monthly_rate
        return max(loan_amount, 0)

    def fha_self_sufficiency_test(self, property, piti_estimate):
        gross_rent = property.appraised_rent_per_unit * property.num_units
        net_rent = gross_rent * 0.75
        return net_rent >= piti_estimate

    def cash_on_cash_return(self, property, down_payment_percent=0.035, annual_expenses=0):
        annual_income = property.appraised_rent_per_unit * property.num_units * 12
        annual_cash_flow = annual_income - annual_expenses
        investment = property.selling_price * (down_payment_percent + 0.03)  # down + closing costs
        return (annual_cash_flow / investment) if investment > 0 else 0

    def break_even_rent(self, property, piti_estimate, annual_expenses):
        total_annual_cost = piti_estimate * 12 + annual_expenses
        return (total_annual_cost / 12) / property.num_units if property.num_units > 0 else 0


class Portfolio:
    def __init__(self):
        self.properties: List = []

    def add_property(self, property):
        self.properties.append(property)

    def analyze_portfolio(self, property_finder, piti_estimates: dict, annual_expenses: dict):
        results = {}
        for prop in self.properties:
            piti = piti_estimates.get(prop.name, 0)
            expenses = annual_expenses.get(prop.name, 0)
            results[prop.name] = {
                "self_sufficiency": property_finder.fha_self_sufficiency_test(prop, piti),
                "cash_on_cash_return": property_finder.cash_on_cash_return(prop, annual_expenses=expenses),
                "break_even_rent_per_unit": property_finder.break_even_rent(prop, piti, expenses)
            }
        return results


# Example usage:
my_finances = FinancialStatus(employer_income=8583, fixed_expenses=256)
finder = PropertyFinder(my_finances)
prop1 = Property(name="Main St Fourplex", selling_price=800000, current_rent_per_unit=2000, num_units=4)
prop2 = Property(name="Oak St Duplex", selling_price=450000, current_rent_per_unit=1500, num_units=2)
portfolio = Portfolio()
portfolio.add_property(prop1)
portfolio.add_property(prop2)
piti_estimates = {"Main St Fourplex": 5000, "Oak St Duplex": 2500}
annual_expenses = {"Main St Fourplex": 10000, "Oak St Duplex": 5000}
analysis = portfolio.analyze_portfolio(finder, piti_estimates, annual_expenses)

# import pandas as pd
# import ace_tools as tools

# # Example DataFrame to display
# data = {
#     "Property": ["Main St Fourplex", "Oak St Duplex"],
#     "Selling Price": [800000, 450000],
#     "Current Rent/Unit": [2000, 1500],
#     "Units": [4, 2],
#     "PITI Estimate": [5000, 2500],
#     "Annual Expenses": [10000, 5000]
# }
# df = pd.DataFrame(data)
# tools.display_dataframe_to_user(name="Property Portfolio Overview", dataframe=df)
