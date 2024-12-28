from db import *
import pytest
import pandas as pd

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


def test_history():
    DB.add_history(200, "USD", DB_enums.ADD, "Income")
    DB.add_history(100, "EGP", DB_enums.SUB, "FOOD")
    history = list(DB.get_history())
    assert history[0][1] == 200 
    assert history[1][3] == 'FOOD'


def test_history_filter():
    def df_it(cursor):
        a = pd.DataFrame(
            columns=["time", "amount", "operation", "category", "currency", "transID"]
        )

        def add(x: list):
            a.loc[len(a)] = x

        b = [x for x in map(add,map(lambda z: list(z), cursor))]
        return a

    DB.add_history(100, "EGP", DB_enums.ADD, "FOOD")
    DB.add_history(200, "JPY", DB_enums.ADD, "FOOD")
    DB.add_history(147, "SAR", DB_enums.ADD, "FOOD")
    DB.add_history(625, "EGP", DB_enums.SUB, "HOSPITALITY")
    DB.add_history(891, "USD", DB_enums.SUB, "ENTERTAINMENT")
    DB.add_history(874, "JPY", DB_enums.SUB, "FOOD")

    for i in df_it(DB.get_history()).sort_values("category").reset_index()["category"] == df_it(DB.get_history(order=DB_enums.CATEGORY))['category']:
        assert i

    for j in df_it(DB.get_history()).sort_values("category", ascending=False).reset_index()["category"] == df_it(DB.get_history(order=DB_enums.CATEGORY, ascending=False))['category']:
        assert j

    for k in df_it(DB.get_history()).sort_values("amount").reset_index()["amount"] == df_it(DB.get_history(order=DB_enums.AMOUNT))['amount']:
        assert k

    for l in df_it(DB.get_history()).sort_values("amount", ascending=False).reset_index()["amount"] == df_it(DB.get_history(order=DB_enums.AMOUNT, ascending=False))['amount']:
        assert l

    for m in df_it(DB.get_history()).sort_values("currency").reset_index()["currency"] == df_it(DB.get_history(order=DB_enums.CURRENCY))['currency']:
        assert m

    for n in df_it(DB.get_history()).sort_values("currency", ascending=False).reset_index()["currency"] == df_it(DB.get_history(order=DB_enums.CURRENCY, ascending=False))['currency']:
        assert n

    for o in df_it(DB.get_history()).sort_values("time").reset_index()["time"] == df_it(DB.get_history(order=DB_enums.TIME))['time']:
        assert o 

    for p in df_it(DB.get_history()).sort_values("time", ascending=False).reset_index()["time"] == df_it(DB.get_history(order=DB_enums.TIME, ascending=False))['time']:
        assert p
    
    for q in df_it(DB.get_history())[df_it(DB.get_history())['category'] == 'FOOD'].reset_index()['category'] == df_it(DB.get_history(category="FOOD"))['category']:
        assert q
    
    for r in df_it(DB.get_history())[df_it(DB.get_history())['currency'] == 'EGP'].reset_index()['currency'] == df_it(DB.get_history(currency="EGP"))['currency']:
        assert r


def test_execute():
    DB.execute("SELECT * FROM wallet")
    with pytest.raises(ValueError):
        DB.execute("None")



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

