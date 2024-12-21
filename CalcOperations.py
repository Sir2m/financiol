class CalcOperations:

     def DiscountCalc():  # calc total price after discount
         price = float(input('Enter the price: '))
         discount = float(input('Enter the discount percentage: '))
         total = price - (price / 100) * discount
         print(f'The total price after discount is {total:.2f}')

     
     def TaxCalc():   # calc total price after taxs
         amount = float(input('Enter the amount: '))
         tax = float(input('Enter the tax percentage: '))
         total = amount + (amount / 100) * tax
         print(f'The total price after tax is {total:.2f}')

     
     def NetGross():  # calc the total salary after taxs
         salary = float(input('Enter your salary: '))
         tax_percentage = float(input('Enter your tax percentage: '))
         total = salary - (salary / 100) * tax_percentage
         print(f'Your total salary after taxes is {total:.2f}')
