from datetime import datetime

class Wallet:
    # needing singlton?
    # adding db changes
    # reading from db at __init__??
    # adding logger
    # treating currency

    def __init__(self, amount: int | float):
        self.amount = amount
    
    @property
    def amount(self):
        return self.__amount
    
    @amount.setter
    def amount (self, amount: int | float):
        self.__amount = amount
    
    def transaction(self, amount: int | float):
        self.amount += amount
    # def deposit(self, amount: int | float):
    #     self.amount += amount
    
    # def withdraw(self, amount: int | float):
    #     self.amount -= amount


class Transaction:
    def __init__(self, amount: int | float, name: str, category: str | None = None):
        ...
    ...


class Deposit(Transaction):
    def __init__(self, amount: int | float, name: str = "deposit", category: str | None = None):
        super().__init__(name, amount, category)


class Withdraw(Transaction):
    def __init__(self, amount: int | float, name: str = "deposit", category: str | None = None):
        super().__init__(name, amount, category)


class Flow(Transaction):
    def __init__(self, name: str, amount: int | float, period: datetime, category: str | None = None):
        super().__init__(name, amount, category)
        self.data = period


class Expenses(Flow):
    def __init__(self, name, amount, period, category = None):
        super().__init__(name, amount, period, category)


class Income(Flow):
    def __init__(self, name, amount, period, category = None):
        super().__init__(name, amount, period, category)

 