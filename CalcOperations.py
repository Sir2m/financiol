class CalcOperations:

    @staticmethod
    def partitioning(value: int | float, percent: int | float, slope: bool | None = True, full: bool | None = True) -> int | float:
        if percent > 1:
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
    def calc_interest(principal: int | float, rate: int | float, periods: int, compound: bool | None = True, total_amount: bool | None = True) -> int | float:
        
        if rate > 1:
            rate /= 100

        if compound:
            # A = P * (1 + r)^(t)
            total = principal * ((1 + rate) ** periods)
        else:
            # A = P * (1 + rt)
            total = principal * (1 + rate * periods)

        if not total_amount:
            return total - principal  # Return only the interest
        else:
            return total      
    