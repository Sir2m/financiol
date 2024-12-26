from db import *
import pytest
import os


@pytest.fixture
def db():
    name = "test.db"
    DB_connection.config(name)
    return


def test_singleton(db):
    assert DB_connection() is DB_connection()


def test_standard_queries():
    # as long as it works, it is almost right, checking rightness is in later tests
    x = DB_connection()
    x.create()
    x.get_history()
    x.get_flow()
    x.get_wallet()


DB = DB_connection()
def test_wallet_add():
    DB.add_wallet("JPY",1000)
    DB.add_wallet("USD",500)
    DB.add_wallet("SAR",800)
    wallet = DB.get_wallet()
    assert wallet['JPY'] == 1000
    assert wallet['USD'] == 500
    assert wallet['SAR'] == 800


def test_wallet_edit_add():
    DB.edit_wallet("JPY",500,DB_enums.ADD)
    wallet = DB.get_wallet()
    assert wallet['JPY'] == 1500


def test_wallet_edit_sub():
    DB.edit_wallet("USD",200,DB_enums.SUB)
    wallet = DB.get_wallet()
    assert wallet['USD'] == 300


def test_wallet_edit_set():
    DB.edit_wallet("SAR",1000,set=True)
    wallet = DB.get_wallet()
    assert wallet['SAR'] == 1000


def test_wallet_get():
    wallet = dict(DB.get_wallet())
    assert wallet == {"JPY":1500 , "USD" : 300 , "SAR" : 1000 }
            
