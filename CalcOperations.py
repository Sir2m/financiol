from abc import ABC, abstractmethod

class CalcOperations(ABC):
    @abstractmethod
    def get_total(self):
        pass

class DiscountCalc(CalcOperations):
    def __init__(self):
        self.price = float(input('Enter the price: '))
        self.discount = float(input('Enter the discount percentage: '))
    def get_total(self):
        total = self.price - (self.price / 100) * self.discount
        print(f'The total price after discount is {total:.2f}')

class TaxCalc(CalcOperations):
    def __init__(self):
        self.amount = float(input('Enter the amount: '))
        self.tax = float(input('Enter the tax percentage: '))
    def get_total(self):
        total = self.amount + (self.amount / 100) * self.tax
        print(f'The total price after tax is {total:.2f}')

class NetGross(CalcOperations):
    def __init__(self):
        self.salary = float(input('Enter your salary: '))
        self.tax_percentage = float(input('Enter your tax percentage: '))

    def get_total(self):
        total = self.salary - (self.salary / 100) * self.tax_percentage
        print(f'Your total salary after taxes is {total:.2f}')

DiscountCalc().get_total()
TaxCalc().get_total()
NetGross().get_total()