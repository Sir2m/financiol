import db 

class CalcOperations:

    @staticmethod
    def partitioning(value: int | float, percent: int | float, slope: bool | None = True, full: bool | None = True) -> int | float:        
        percent /= 100
        change = value * percent
        
        if not full:
            return change
        if slope:
            final = value + change         #taxs
        else:
            final = value - change         #sales

        return final 


    @staticmethod
    def calc_interest(principal: int | float, rate: int | float, periods: int = 1, installments: bool | None = False) -> int | float:
        if periods < 0:
            raise ValueError(" periode can't be NEGATIVE ")
        
        rate /= 100

        if installments:
            result = principal * ((rate * ((1+rate) ** periods))/(((1+rate) ** periods) - 1))
        else:
            result = principal * ((1 + rate) ** periods)

        return result
    


    @staticmethod
    def currency_exchange(from_currency : str , to_currency : str, amount : int | float) -> int | float :
        currency = db.DB_connection.CURRENCY

        f_currency = 1 / currency[from_currency]   # from_currency / USD  
        t_currency = currency[to_currency]    # USD / to_currency   
        rate = t_currency * f_currency         # from_currency / to_currency   
        changing = amount * rate                                                      
        
        return changing    