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
                        "user_name": "",
                        "other_users": {}
                    }
                json.dump(x, file, indent=3)
            load_data()
        self.__theme = self.__data['theme']
        self.__currency = self.__data['currency']
        self.__id = self.__data['user_id']
        self.__name = self.__data['user_name']


    def __new__(cls):
        if cls.__data is None: 
            cls.__data = super(Meta_data, cls).__new__(cls)
        return cls.__data


    def save(self):
        self.__data['theme'] = self.__theme
        self.__data['currency'] = self.__currency
        self.__data['user_id'] = self.__id
        self.__data['user_name'] = self.__name
        with open(self.PATH, 'w') as file:
            json.dump(self.__data, file, indent=4)


    def get_data(self):
        return [self.__theme, self.__currency, self.__id, self.__name]


    def theme_change(self):
        x = {
            "light": "dark",
            "dark": "light"
        }
        self.__theme = x[self.__theme]


    def change_account(self, remember, id):
        if remember:
            self.__data['other_users'][self.__id] = {
                "theme": self.__theme,
                "currency": self.__currency,
                "user_name": self.__name
            }

        new = self.__data['other_users'][id]
        self.__id = id
        self.__theme = new["theme"]
        self.__currency = new["currency"]
        self.__name = new['user_name']


    def set_new_account(self, remember, id, currency, user_name):
        if remember:
            self.__data['other_users'][self.__id] = {
                "theme": self.__theme,
                "currency": self.__currency,
                "user_name": self.__name
            }

        self.__id = id
        self.__theme = "light"
        self.__currency = currency
        self.__name = user_name
    
    
    def log_out(self):
        self.__id = ""
        self.__theme = "light"
        self.__currency = ""
        self.__name = ""