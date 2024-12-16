import sqlite3

class DB_connection:
    PATH = "db.db"
    __instance = None

    def __init__(self):
        self.__db = sqlite3.connect(self.PATH)


    def __new__(cls):
        if cls.__instance is None: 
            cls.__instance = super(DB_connection, cls).__new__(cls)
        return cls.__instance


    @classmethod
    def config(cls, path: str):
        # a way to check that it is genuine path?
        cls.PATH = path
    
    def create(self):
        # for creating the tables if there is no tables already (new user)
        ...
    
    def transaction(self):
        # for changing the data in the new worth table (is adding to the history table too violates solid principals? 🤔)
        ...
    
    def sub_periodic(self):
        # submits a periodic transaction, dealing with both expenses and income
        ...
