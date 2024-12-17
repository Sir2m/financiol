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
        self.__db.execute("""CREATE TABLE Wallet (
            Currency TEXT NOT NULL PRIMARY KEY UNIQUE,
            Amount INTEGER NOT NULL
            );""")
        
        self.__db.execute("""CREATE TABLE Flow (
            FlowID INTEGER PRIMARY KEY NOT NULL UNIQUE,
            Time TIME NOT NULL,
            Amount INTEGER NOT NULL,
            Category TEXT,
            Type TEXT NOT NULL,
            Currency TEXT NOT NULL,
            FOREIGN KEY (Currency) REFERENCES Wallet(Currency)
            );""")

        self.__db.execute("""CREATE TABLE History (
            Time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            Operation TEXT NOT NULL,
            Amount INTEGER NOT NULL,
            Category TEXT,
            Currency TEXT NOT NULL,
            TransID INTEGER,
            FOREIGN KEY (Currency) REFERENCES Wallet(Currency),
            FOREIGN KEY (TransID) REFERENCES Flow(FlowID)
            );""")

    
    def transaction(self):
        # for changing the data in the new worth table (is adding to the history table too violates solid principals? 🤔)
        ...
    
    def set_flow(self):
        # submits a Flow transaction, dealing with both expenses and income
        ...
