class CapitalAccount:
    def __init__(self, name, account_type, balance=0.0, annual_yield=0.0, notes=""):
        self.name = name
        self.account_type = account_type.lower()  # e.g., 'checking', 'savings', '401k', 'rothira'
        self.balance = balance
        self.annual_yield = annual_yield  # as decimal, e.g., 0.02 for 2%
        self.notes = notes

    def monthly_yield(self):
        return self.balance * (self.annual_yield / 12)

    def is_liquid_account(self):
        return self.account_type in ["checking", "savings"]

    def is_retirement_account(self):
        return not self.is_liquid_account()

    def summary(self):
        return {
            'name': self.name,
            'type': self.account_type,
            'balance': round(self.balance, 2),
            'annual_yield': round(self.annual_yield, 4),
            'monthly_yield': round(self.monthly_yield(), 2),
            'is_liquid': self.is_liquid_account(),
            'is_retirement': self.is_retirement_account(),
            'notes': self.notes
        }

    def __repr__(self):
        return f"<CapitalAccount {self.name} ({self.account_type}): ${self.balance:.2f}, {self.annual_yield*100:.2f}% yield>"

# Define accounts
Barclays = CapitalAccount("High Yield Savings", "savings", balance=50_047, annual_yield=0.042)
WF_checking = CapitalAccount("WF Checking", "checking", balance=3_303.05, annual_yield=0.0)
WF_gifts = CapitalAccount("WF Gifts", "checking", balance=1_017.97, annual_yield=0.0)
WF_rent = CapitalAccount("WF Rent", "checking", balance=2_735.89, annual_yield=0.0)
UMB_checking_1 = CapitalAccount("UMB Checking 1", "checking", balance=20.00, annual_yield=0.0)
UMB_checking_2 = CapitalAccount("UMB Checking 2", "checking", balance=800.15, annual_yield=0.0)
k401 = CapitalAccount("Employer 401k", "401k", balance=49_167, annual_yield=0.10)
etrade_roth_ira = CapitalAccount("Personal Roth IRA", "rothIRA", balance=13_676.14, annual_yield=0.0656)
etrade_brokerage = CapitalAccount("Personal Roth IRA", "brokerage", balance=64.98, annual_yield=0.00)

# List for easy import
ALL_ACCOUNTS = [Barclays, WF_checking, WF_gifts, WF_rent, UMB_checking_1, UMB_checking_2, k401, etrade_roth_ira, etrade_brokerage]