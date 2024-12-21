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