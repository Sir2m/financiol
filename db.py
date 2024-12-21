import sqlite3
import requests


class DB_connection:
    PATH = "db.db"
    __instance = None
    CURRENCY = requests.get("https://open.er-api.com/v6/latest").json()['rates']

    def __init__(self):
        self.__db = sqlite3.connect(self.PATH)


    def __new__(cls):
        if cls.__instance is None: 
            cls.__instance = super(DB_connection, cls).__new__(cls)
        return cls.__instance


    def __del__(self):
        self.__db.commit()
        self.__db.close()

    @classmethod
    def config(cls, path: str):
        # a way to check that it is genuine path?
        cls.PATH = path
    
    def create(self):
        # for creating the tables if there is no tables already (new user)
        self.__db.execute("""CREATE TABLE wallet (
            Currency TEXT NOT NULL PRIMARY KEY UNIQUE,
            Amount INTEGER NOT NULL
            );""")
        
        self.__db.execute("""CREATE TABLE flow (
            FlowID INTEGER PRIMARY KEY NOT NULL UNIQUE,
            Time TIME NOT NULL,
            Amount INTEGER NOT NULL,
            Category TEXT,
            Type TEXT NOT NULL,
            Currency TEXT NOT NULL,
            FOREIGN KEY (Currency) REFERENCES wallet(Currency)
            );""")

        self.__db.execute("""CREATE TABLE history (
            Time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            Operation TEXT NOT NULL,
            Amount INTEGER NOT NULL,
            Category TEXT,
            Currency TEXT NOT NULL,
            TransID INTEGER,
            FOREIGN KEY (Currency) REFERENCES wallet(Currency),
            FOREIGN KEY (TransID) REFERENCES flow(FlowID)
            );""")

    
    def add_wallet(self, curr: str, amount: int | float) -> None:
        self.__db.execute(f"INSERT INTO wallet VALUES (\"{curr}\", {amount});")
    

    def edit_wallet(self, curr: str, amount: int | float, slope: bool | None = True, set: bool | None = False) -> None:
        # submits a Flow transaction, dealing with both expenses and income
        def execute(final):
            self.__db.execute(f"UPDATE wallet SET Amount = {final} WHERE Currency = {curr};")
        
        if set:
            execute(amount)
            return
        
        origin =  self.__db.execute(f"SELECT Amount FROM wallet WHERE curr = \"{curr}\";")
        origin = list(origin)[0][0]

        if slope:
            execute(origin + amount)
        else:
            execute(origin - amount)
    

    def get_wallet(self, curr: str):
        return dict(self.__db.execute(f"SELECT * FROM wallet WHERE Currency = \"{curr}\";"))