from db import *
import pytest
import os


@pytest.fixture
def test_db():
    name = "test.db"
    DB_connection.config(name)
    return


def test_singleton(test_db):
    assert DB_connection() is DB_connection()

def test_standard_queries():
    # as long as it works, it is almost right, checking rightness is in later tests
    x = DB_connection()
    x.create()
    x.get_history()
    x.get_flow()
    x.get_wallet()