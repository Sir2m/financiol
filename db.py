import sqlite3
import requests
from enum import Enum

class DB_enums(Enum):
    ADD = 1
    SUB = 2
    TIME = 10
    CATEGORY = 11
    AMOUNT = 12
    CURRENCY = 13
    

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
    

    @staticmethod
    def enumap(enu: DB_enums):
        match enu:
            case DB_enums.TIME:
                return "time"
            case DB_enums.CATEGORY:
                return "category"
            case DB_enums.AMOUNT:
                return "amount"
            case DB_enums.CURRENCY:
                return "currency"
            case DB_enums.ADD:
                return "WITH"
            case DB_enums.SUB:
                return "DEPO"
    
    def create(self):
        # for creating the tables if there is no tables already (new user)
        self.__db.execute("""CREATE TABLE wallet (
            currency TEXT NOT NULL PRIMARY KEY UNIQUE,
            amount INTEGER NOT NULL
            );""")
        
        self.__db.execute("""CREATE TABLE flow (
            name TEXT NOT NUL,
            flowID INTEGER PRIMARY KEY NOT NULL UNIQUE,
            time TIME NOT NULL,
            amount INTEGER NOT NULL,
            category TEXT,
            operation TEXT NOT NULL,
            currency TEXT NOT NULL,
            FOREIGN KEY (Currency) REFERENCES wallet(Currency)
            );""")

        self.__db.execute("""CREATE TABLE history (
            time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            operation TEXT NOT NULL,
            amount INTEGER NOT NULL,
            category TEXT,
            currency TEXT NOT NULL,
            transID INTEGER,
            FOREIGN KEY (Currency) REFERENCES wallet(Currency),
            FOREIGN KEY (TransID) REFERENCES flow(FlowID)
            );""")

    
    def add_wallet(self, currency: str, amount: int | float) -> None:
        self.__db.execute(f"INSERT INTO wallet VALUES (\"{currency}\", {amount});")
    

    def edit_wallet(self, curr: str, amount: int | float, slope: DB_enums | None = DB_enums.ADD, set: bool | None = False) -> None:
        # submits a Flow transaction, dealing with both expenses and income
        def execute(final):
            self.__db.execute(f"UPDATE wallet SET Amount = {final} WHERE Currency = {curr};")
        
        if set:
            execute(amount)
            return
        
        origin =  self.__db.execute(f"SELECT Amount FROM wallet WHERE curr = \"{curr}\";")
        origin = list(origin)[0][0]

        if slope == DB_enums.ADD:
            execute(origin + amount)
        elif slope == DB_enums.SUB:
            execute(origin - amount)
        else:
            raise ValueError("Wrong enum!")
    

    def get_wallet(self, curr: str):
        return dict(self.__db.execute(f"SELECT * FROM wallet WHERE Currency = \"{curr}\";"))
    

    def add_history(self, amount: int | float, currency: str, operation: DB_enums | None = DB_enums.ADD, category: str | None = None):
        if operation == DB_enums.ADD:
            operation = "WITH"
        elif operation == DB_enums.SUB:
            operation = "DEPO"
        else:
            raise ValueError("What kind of operation is this?!")
        
        s = """INSERT INTO history (amount, currency, operation"""
        
        if category:
            s += ", category"
        
        s += f") VALUES ({amount}, {currency}, {operation}"

        if category:
            s+= f", {category}"
        
        s += ");"

        self.__db.execute(s)
    
    def get_history(self, category: str | None = None, currency: str | None = None, name: str | None = None, order: DB_enums | None = DB_enums.TIME, ascending: bool | None = True):
        
        s = "SELECT history.time, history.amount, history.operation, history.category, history.currency, flow.name FROM history LEFT JOIN flow ON history.transID = flow.flowID"

        if category or currency or name:
            s += " WHERE "
        
        if category:
            s += f"history.category='{category}'"
        
        if currency:
            if category:
                s += " AND "
            s += f"history.currency='{currency}'"
        
        if name:
            if category or currency:
                s += " AND "
            s += f"flow.name={name}"
        
        if order:
            order = f"history.{DB_connection.enumap(order)}"
            if ascending:
                ascending = "ASC"
            else:
                ascending = "DESC"
            s += f"ORDER BY {order} {ascending}"
        
        s += ";"
        
        return self.__db.execute(s)
    
    def add_flow(self, name: str, time, amount: int, currency: str, category: str | None = None, operation: DB_enums | None = DB_enums.ADD) -> None:
        s = """INSERT INTO flow (name, amount, time, currency, operation"""
        
        if category:
            s += ", category"
        
        s += f") VALUES ({name}, {amount}, {time}, {currency}, {operation}"

        if category:
            s+= f", {category}"
        
        s += ");"

        self.__db.execute(s)
    
    def get_flow(self, name: str | None = None, operation: DB_enums | None = None, category: str | None = None, currency: str | None = None, order: DB_enums | None = None, ascending: bool | None = True):
        
        s = "SELECT name, time, amount, operation, category, currency FROM flow"

        if category or currency or name or operation:
            s += " WHERE "
        
        if category:
            s += f"category='{category}'"
        
        if currency:
            if category:
                s += " AND "
            s += f"currency='{currency}'"
        
        if name:
            if category or currency:
                s += " AND "
            s += f"name={name}"
        
        if operation:
            if category or currency or name:
                s += " AND "
            operation = DB_connection.enumap(operation)
            s += f"operation={operation}"
        
        if order:
            order =  DB_connection.enumap(order)
            if ascending:
                ascending = "ASC"
            else:
                ascending = "DESC"
            s += f"ORDER BY {order} {ascending}"
        
        s += ";"
        
        return self.__db.execute(s)

    def flow_hist(self):
        ...