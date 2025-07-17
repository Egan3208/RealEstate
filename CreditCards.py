class CreditCard:
    def __init__(self, name, balance, apr=0.20, user_payment=0.0, fees=0):
        self.name = name
        self.balance = balance
        self.apr = apr
        self.user_payment = user_payment
        self.fees = fees

    def monthly_interest(self):
        return (self.apr / 12) * self.balance

    def minimum_payment(self):
        if self.balance <= 0:
            return 0
        return max(25, self.balance * 0.02)

    def planned_payment(self):
        return self.user_payment if self.user_payment > 0.0 else self.minimum_payment()

    def summary(self):
        return {
            'name': self.name,
            'balance': round(self.balance, 2),
            'apr': round(self.apr, 4),
            'minimum_payment': round(self.minimum_payment(), 2),
            'planned_payment': round(self.planned_payment(), 2),
            'monthly_interest': round(self.monthly_interest(), 2),
            'fees': round(self.fees, 2),
            'provider': self.__class__.__name__
        }


class Card_WELF(CreditCard):
    def minimum_payment(self):
        if self.balance <= 0:
            return 0
        combined_balance = self.balance
        interest_charges = self.monthly_interest()
        payment_1 = 40 if combined_balance >= 40 else combined_balance
        payment_2 = combined_balance * 0.035
        payment_3 = interest_charges + self.fees + (combined_balance * 0.01)
        return max(payment_1, payment_2, payment_3, self.user_payment)


class Card_CHAS(CreditCard):
    def minimum_payment(self):
        if self.balance <= 0:
            return 0
        part1 = self.balance if self.balance < 35 else 35
        part2 = (self.balance * 0.01) + self.monthly_interest() + self.fees
        return max(part1, part2, self.user_payment)


class Card_CITI(CreditCard):
    def minimum_payment(self):
        if self.balance <= 0:
            return 0
        part1 = self.balance if self.balance < 25 else 25
        part2 = round(self.balance * 0.01) + self.monthly_interest() + self.fees
        return max(part1, part2, self.user_payment)


class Card_AMEX(CreditCard):
    def minimum_payment(self):
        if self.balance <= 0:
            return 0
        interest = self.monthly_interest()
        option1 = interest + (self.balance * 0.01)
        option2 = self.balance * 0.02
        option3 = 40 if self.balance >= 40 else self.balance
        return max(option1, option2, option3, self.user_payment)

# Define current cards to import
WF_1 = Card_WELF("WF_1", balance=1563.99, apr=0.00, user_payment=0)#142.00)
WF_2 = Card_WELF("WF_2", balance=2462.34, apr=0.1765)
Citi_1 = Card_CITI("Citi_1", balance=2002.35, apr=0.00, user_payment=0)#100.00)
Chase_1 = Card_CHAS("Chase_1", balance=4020.43, apr=0.1849)
Amex_1 = Card_AMEX("Amex_1", balance=11236.98, apr=0.2124)

# List to easily import all
ALL_CARDS = [WF_1, WF_2, Citi_1, Chase_1, Amex_1]