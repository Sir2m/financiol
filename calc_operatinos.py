import financiol.db as db

class CalcOperations:

    @staticmethod
    def partitioning(value: int | float, percent: int | float, slope: bool | None = True, full: bool | None = True) -> int | float:        
        percent /= 100
        change = value * percent
        
        if not full:
            return change
        
        if slope:
            final = value + change
        else:
            final = value - change
        
        return final 

    @staticmethod
    def calc_interest(principal: int | float, rate: int | float, periods: int = 1, installments: bool | None = False) -> int | float:
        if periods < 1:
            raise ValueError("There is nothing called NEGATIVE PERIODS!!")
        
        rate /= 100

        if installments:
            result = principal * ((rate * ((1+rate) ** periods))/(((1+rate) ** periods) - 1))
        else:
            result = principal * ((1 + rate) ** periods)

        return result
    
    @staticmethod
    def currency_exchange(from_currency : str , to_currency : str, amount : int | float) -> int | float :
        currency = db.DB_connection.CURRENCY
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        try:
          f_currency = 1 / currency[from_currency]  
        except:
            raise ValueError(f"{from_currency}: This is not a currency!")
        
        try:
            t_currency = currency[to_currency]
        except:
            raise ValueError(f"{to_currency}: This is not a currency!")
        rate = t_currency * f_currency
        changing = amount * rate 

        return changing