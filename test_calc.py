from calc_operatinos import CalcOperations
import pytest


def test_parti():
    assert CalcOperations.partitioning(100, 10) == 110
    assert CalcOperations.partitioning(100, 10, slope=False) == 90
    assert CalcOperations.partitioning(100, 10, full=False) == 10 
    assert CalcOperations.partitioning(100, 10, slope=False, full=False) == 10


def test_int():
    assert round(CalcOperations.calc_interest(100, 10)) == 110
    assert round(CalcOperations.calc_interest(100, 10, 10)) == 259
    assert round(CalcOperations.calc_interest(100, 1, 5, True)) == 21
    
    with pytest.raises(ValueError):
        CalcOperations.calc_interest(100, 10, -10) # error checking, value error


def test_curr():
    assert CalcOperations.currency_exchange("USD", "Egp", 20) == CalcOperations.currency_exchange("uSd", 'egP', 20)
    
    with pytest.raises(ValueError):
        CalcOperations.currency_exchange("aaa", "eGP", 100)
    
    with pytest.raises(ValueError):
        CalcOperations.currency_exchange("UsD", "bbb", 100)