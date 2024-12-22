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
    def calc_interest(principal: int | float, rate: int | float, periods: int, installments: bool | None = True) -> int | float:
        rate /= 100

        if installments:
            result = principal * ((rate * ((1+rate) ** periods))/(((1+rate) ** periods) - 1))
        else:
            result = principal * ((1 + rate) ** periods)

        return result
    