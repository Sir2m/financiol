import sqlite3
import requests
from enum import Enum
from werkzeug.security import check_password_hash, generate_password_hash

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
    # CURRENCY = requests.get("https://open.er-api.com/v6/latest").json()['rates']

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
            name TEXT NOT NULL,
            flowID INTEGER PRIMARY KEY NOT NULL UNIQUE,
            time TIME NOT NULL,
            amount INTEGER NOT NULL,
            category TEXT,
            operation TEXT NOT NULL,
            price_currency TEXT NOT NULL,
            pay_currency TEXT,
            FOREIGN KEY (price_currency) REFERENCES wallet(currency)
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
        self.__db.execute(f"INSERT INTO wallet (currency, amount) VALUES (?, ?)", (currency, amount))
    

    def edit_wallet(self, curr: str, amount: int | float, slope: DB_enums | None = DB_enums.ADD, set: bool | None = False) -> None:
        # submits a Flow transaction, dealing with both expenses and income
        def execute(final):
            self.__db.execute("UPDATE wallet SET amount = ? WHERE currency = ?", (final, curr))
        if set:
            execute(amount)
            return
        
        origin =  self.__db.execute("SELECT amount FROM wallet WHERE currency = ?", (curr,))
        origin = list(origin)[0][0]
        if slope == DB_enums.ADD:
            execute(origin + amount)
        elif slope == DB_enums.SUB:
            execute(origin - amount)
        else:
            raise ValueError("Wrong enum!")
    

    def get_wallet(self, currency: str | None = None):
        s = "SELECT * FROM wallet"
        if currency:
            s += f" WHERE Currency = \"{currency}\""
        s += ";"
        return dict(self.__db.execute(s))
    

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
        
        s += ") VALUES (?, ?, ?"
        col = [amount, currency, operation]

        if category:
            s+= ",?"
            col.append(category)
        
        s += ");"     
        self.__db.execute(s, col)
    
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
            s += f" ORDER BY {order} {ascending}"
        
        s += ";"
        
        return self.__db.execute(s)
    
    def add_flow(self, name: str, time, amount: int, price_currency: str, pay_currency:str | None = None, category: str | None = None, operation: DB_enums | None = DB_enums.ADD) -> None:
        s = """INSERT INTO flow (name, amount, time, pay_currency, price_currency, operation"""
        
        if not pay_currency:
            pay_currency = price_currency

        if category:
            s += ", category"
        
        s += f") VALUES ({name}, {amount}, {time}, {pay_currency}, {price_currency}, {operation}"

        if category:
            s+= f", {category}"
        
        s += ");"

        self.__db.execute(s)
    
    def get_flow(self, name: str | None = None, operation: DB_enums | None = None, category: str | None = None, pay_currency: str | None = None, price_currency: str | None = None, order: DB_enums | None = None, ascending: bool | None = True):
        
        s = "SELECT name, time, amount, operation, category, pay_currency, price_currency FROM flow"

        if category or pay_currency or price_currency or name or operation:
            s += " WHERE "
        
        if category:
            s += f"category='{category}'"
        
        if pay_currency:
            if category:
                s += " AND "
            s += f"currency='{pay_currency}'"
        
        if price_currency:
            if category or pay_currency:
                s += " AND "
            s += f"currency='{price_currency}'"


        if name:
            if category or pay_currency or price_currency:
                s += " AND "
            s += f"name={name}"
        
        if operation:
            if category or pay_currency or price_currency or name:
                s += " AND "
            operation = DB_connection.enumap(operation)
            s += f"operation={operation}"
        
        if order:
            order =  DB_connection.enumap(order)
            if ascending:
                ascending = "ASC"
            else:
                ascending = "DESC"
            s += f" ORDER BY {order} {ascending}"
        
        s += ";"
        
        return self.__db.execute(s)

    def flow_hist(self):
        ...
    

class DB_accounts:
    PATH = "accounts.db"
    __instance = None

    def __init__(self):
        self.__db = sqlite3.connect(self.PATH)


    def __new__(cls):
        if cls.__instance is None: 
            cls.__instance = super(DB_accounts, cls).__new__(cls)
        return cls.__instance


    def __del__(self):
        self.__db.commit()
        self.__db.close()

    
    # just made for the tests
    @classmethod
    def config(cls, path: str):
        # a way to check that it is genuine path?
        cls.PATH = path


    def create(self):
        self.__db.execute("""CREATE TABLE accounts (
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            userID INTEGER NOT NULL UNIQUE PRIMARY KEY,
            primary_currency NOT NULL
            );""")
    
    def uniquness(self, username: str):
        unique = list(self.__db.execute(f"SELECT username FROM accounts WHERE username='{username}'"))
        
        if len(unique) != 0:
            return False
        
        return True

    def add_account(self, username: str, password: str, currency: str):
        self.__db.execute("INSERT INTO accounts (username, password, primary_currency) VALUES (?, ?, ?)", (username, generate_password_hash(password), currency))

    def login(self, username: str, password: str):
        y = list(self.__db.execute(f"SELECT password, userID FROM accounts WHERE username = '{username}'"))
        if y and check_password_hash(y[0][0], password):
            return y[0][1]
        else:
            raise ValueError("Wrong Password!")
