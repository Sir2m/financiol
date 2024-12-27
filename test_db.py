from db import *
import pytest
import os


name = "test.db"
DB_connection.config(name)
DB = DB_connection()


def test_singleton():
    assert DB_connection() is DB_connection()


def test_standard_queries():
    # as long as it works, it is almost right, checking rightness is in later tests
    DB.create()
    DB.get_history()
    DB.get_flow()
    DB.get_wallet()


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
            



DB_accounts.config("test_acc.db")
DB_acc = DB_accounts()


def test_acc_singleton():
    assert DB_accounts() is DB_accounts()


def test_acc_standard_queries():
    DB_acc.create()


def test_adding():
    DB_acc.add_account("Moh", "5512", "EGP")
    DB_acc.add_account("uya", "5512", "EGP")
    DB_acc.add_account("onm", "5512", "EGP")


def test_uniquness():
    assert DB_acc.uniquness("Moh") == False
    assert DB_acc.uniquness("uya") == False
    assert DB_acc.uniquness("onm") == False
    assert DB_acc.uniquness("lme") == True


def test_login():
    assert DB_acc.login("Moh", "5512") == 1
    assert DB_acc.login("uya", "5512") == 2
    with pytest.raises(ValueError):
        DB_acc.login("onm", "8895")
        DB_acc.login("lme", "5512")
