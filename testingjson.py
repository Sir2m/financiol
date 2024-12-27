import json

class Meta_data:
    __data = None
    PATH = "preference.json"

    def __init__(self):
        def load_data():
            with open(self.PATH, 'r') as file:
                self.__data = json.load(file)

        try:
            load_data()
        except:
            with open(self.PATH, 'w') as file:
                x = {
                        "theme": "light",
                        "currency": "",
                        "user_id": "",
                        "other_users": {}
                    }
                json.dump(x, file, indent=3)
            load_data()
        self.__theme = self.__data['theme']
        self.__currency = self.__data['currency']
        self.__id = self.__data['user_id']
        print(self.__theme)


    def __new__(cls):
        if cls.__data is None: 
            cls.__data = super(Meta_data, cls).__new__(cls)
        return cls.__data


    def __del__(self):
        self.__data['theme'] = self.__theme
        self.__data['currency'] = self.__currency
        self.__data['user_id'] = self.__id
        with open(self.PATH, 'w') as file:
            json.dump(self.__data, file, indent=4)


    def theme_change(self):
        x = {
            "light": "dark",
            "dark": "light"
        }
        self.__theme = x[self.__theme]


    def set_base_currency(self, currency:str):
        self.__currency = currency


    def change_account(self, remember, id):
        if remember:
            self.__data['other_users'][self.__id] = {
                "theme": self.__theme,
                "currency": self.__currency,
            } 
        new = self.__data['other_users'][id]
        self.__id = id
        self.__theme = new["theme"]
        self.__currency = new["currency"]


    def set_new_account(self, remember, id, currency):
        if remember:
            self.__data['other_users'][self.__id] = {
                "theme": self.__theme,
                "currency": self.__currency,
            }

        self.__id = id
        self.__theme = "light"
        self.__currency = currency