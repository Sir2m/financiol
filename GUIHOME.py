import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import testingjson
import db
from reminders import submit_reminder, setup_database, start_reminder_checker
import pandas as pd 
import charts
from calc_operatinos import CalcOperations
import notifi

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class ThemeManager:
    def __init__(self, parent_window, customtkinter_mode=False):
        self.parent = parent_window
        self.customtkinter_mode = customtkinter_mode
         # Default theme for CustomTkinter widgets every thing here should be changable in the json file or so i hope 
        self.default_theme = {
            "CTk": {
                "fg_color": ["#f2f2f2", "#2b2b2b"],
            },
            "CTkFrame": {
                "fg_color": ["#ebebeb", "#242424"],
                "top_fg_color": ["#f2f2f2", "#2b2b2b"]
            },
            "CTkButton": {
                "fg_color": ["#3b8ed0", "#1f6aa5"],
                "hover_color": ["#36719f", "#144870"],
                "text_color": ["#ffffff", "#ffffff"],
                "border_color": ["#3b8ed0", "#1f6aa5"]
            },
            "CTkLabel": {
                "fg_color": "transparent",
                "text_color": ["#000000", "#ffffff"]
            },
            "CTkSwitch": {
                "fg_color": ["#939ba2", "#4a4d50"],
                "progress_color": ["#3b8ed0", "#1f6aa5"],
                "button_color": ["#ffffff", "#ffffff"],
                "button_hover_color": ["#f0f0f0", "#0f0f0f"],
                "text_color": ["#000000", "#ffffff"]
            }
        }

        self.current_theme = self.default_theme.copy()
    # the next 3 functions are for the theme manager to apply the theme to the window
    def apply_theme(self, widget):
        widget_type = widget.__class__.__name__
        if widget_type in self.current_theme:
            widget.configure(**self.current_theme[widget_type])
        for child in widget.winfo_children():
            self.apply_theme(child)

    def apply_theme_to_window(self):
        self.apply_theme(self.parent)

    def load_theme_from_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            title="Select Theme File"
        )

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    new_theme = json.load(file)
                    if self.validate_theme(new_theme):
                        self.current_theme = new_theme
                        self.apply_theme_to_window()
                        return True
                    else:
                        messagebox.showerror("Error", "Invalid theme structure.")
                        return False
            except Exception as e:
                messagebox.showerror("Error", f"Error loading theme: {str(e)}")
                return False
        return False

    def validate_theme(self, theme_dict):
        required_widgets = {
            "CTk": ["fg_color"],
            "CTkFrame": ["fg_color"],
            "CTkButton": ["fg_color", "hover_color", "text_color", "border_color"],
            "CTkLabel": ["fg_color", "text_color"],
            "CTkSwitch": ["fg_color", "progress_color", "button_color", "button_hover_color", "text_color"]
        }
        for widget, keys in required_widgets.items():
            if widget not in theme_dict:
                return False
            for key in keys:
                if key not in theme_dict[widget]:
                    return False
        return True

    def reset_theme(self):
        self.current_theme = self.default_theme.copy()
        self.apply_theme_to_window()
# this function is called when the user clicks the change theme button
def change_theme_callback(theme_manager):
    success = theme_manager.load_theme_from_file()
    if success:
        messagebox.showinfo("Success", "Theme applied successfully!")
# this is the main class for the home page itself
class HomePage(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.json = testingjson.Meta_data()
        self.meta = self.json.get_data()
        self.acount = db.DB_accounts()
        if self.meta[2]:
            db.DB_connection.config(f"user{self.meta[2]}db.db")
            self.__db = db.DB_connection()
            self.home_page()
        else:
            self.log_in()


    def res_lab(self):
        result_label = ctk.CTkLabel(master=self, text="")
        result_label.grid(row=0, column=0, pady=6, padx=10)
        result_label.grid(row=0, column=0, pady=4, padx=6)
        return result_label
    
    def center_frame(self, frame):
        frame.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        for i in range(3):
            frame.rowconfigure(i, weight=1)
            frame.columnconfigure(0, weight=1)

    def log_in(self):
        self.geometry("300x450")
        self.title("Login & Sign Up")

        result_label = self.res_lab()

        def login_user():
            username = login_box.get()
            password = password_box.get()
            try:
                id, y, primary_currency = self.acount.login(username, password)
                result_label.configure(text="Login successful", text_color="green")
                self.json.set_new_account(False, id, primary_currency, username)
                db.DB_connection.config(f"user{id}db.db")  # PUT WHAT YOU WANT TO LOGIN HERE ///////////////////////////////////////////
                self.__db = db.DB_connection()
                login_frame.grid_forget()
                self.home_page()
            except ValueError as s:
                result_label.configure(text=str(s), text_color="red")  # wrong password

        def switch_to_signup():  # switch to the Sign-Up frame
            login_frame.grid_forget()
            self.sign_up()

        login_frame = ctk.CTkFrame(master=self)
        login_frame.grid(row=1, column=0, pady=20, padx=30)

        login_label = ctk.CTkLabel(master=login_frame, text="Login", font=("Arial", 16))
        login_label.grid(row=0, column=0, pady=12, padx=10)

        login_box = ctk.CTkEntry(master=login_frame, placeholder_text="Username")
        login_box.grid(row=1, column=0, pady=12, padx=10)

        password_box = ctk.CTkEntry(master=login_frame, placeholder_text="Password", show="*")
        password_box.grid(row=2, column=0, pady=12, padx=10)

        login_button = ctk.CTkButton(master=login_frame, text="Login", command=login_user)
        login_button.grid(row=3, column=0, pady=12, padx=10)

        login_question_label = ctk.CTkLabel(master=login_frame, text="Don't have an account?")
        login_question_label.grid(row=4, column=0, pady=6, padx=10)

        signup_switch_button = ctk.CTkButton(master=login_frame, text="Sign Up", command=switch_to_signup)
        signup_switch_button.grid(row=5, column=0, pady=6, padx=10)

    def sign_up(self):
        signup_frame = ctk.CTkFrame(master=self)
        signup_frame.grid(row=1, column=0, pady=20, padx=30)

        result_label = self.res_lab()

        def register_user():  # registration function
            username = username_box.get()
            if self.acount.uniquness(username):
                signup_frame.grid_forget()
                set_amount_frame.grid(row=1, column=0, pady=20, padx=30)
                result_label.configure(text="Registration successful", text_color="green")
            else:
                result_label.configure(text="Username already taken", text_color="red")

        def switch_to_login():  # switch to the Login frame
            signup_frame.grid_forget()
            self.log_in()

        def set_amount():
            amount = set_amount_box.get()
            username = username_box.get()
            password = password_box_reg.get()
            primary_currency = currency_entry.get()

            self.acount.add_account(username, password, primary_currency)
            id, y, z = self.acount.login(username, password)
            self.json.set_new_account(False, id, primary_currency, username)

            db.DB_connection.config(f"user{id}db.db")
            self.__db = db.DB_connection()
            self.__db.add_wallet(primary_currency, amount)
            set_amount_frame.grid_forget()
            self.home_page()  # /////////////////////////////////////////////////////////////////////////////////////

        signup_label = ctk.CTkLabel(master=signup_frame, text="Sign Up", font=("Arial", 16))
        signup_label.grid(row=0, column=0, pady=12, padx=10)

        username_box = ctk.CTkEntry(master=signup_frame, placeholder_text="Username")
        username_box.grid(row=1, column=0, pady=12, padx=10)

        password_box_reg = ctk.CTkEntry(master=signup_frame, placeholder_text="Password", show="*")
        password_box_reg.grid(row=2, column=0, pady=12, padx=10)

        register_button = ctk.CTkButton(master=signup_frame, text="Register", command=register_user)
        register_button.grid(row=3, column=0, pady=12, padx=10)

        signup_question_label = ctk.CTkLabel(master=signup_frame, text="Already have an account?")
        signup_question_label.grid(row=4, column=0, pady=6, padx=10)

        login_switch_button = ctk.CTkButton(master=signup_frame, text="Login", command=switch_to_login)
        login_switch_button.grid(row=5, column=0, pady=6, padx=10)

        # set_amount frame
        set_amount_frame = ctk.CTkFrame(master=self)

        set_currency_label = ctk.CTkLabel(master=set_amount_frame, text="Set primary currency", font=("Arial", 16))
        set_currency_label.grid(row=0, column=0, pady=12, padx=10)

        currency_entry = ctk.CTkOptionMenu(master=set_amount_frame, values=list(db.DB_connection.CURRENCY.keys()))
        currency_entry.grid(row=1, column=0, pady=12, padx=10)

        set_amount_label = ctk.CTkLabel(master=set_amount_frame, text="Set Amount", font=("Arial", 16))
        set_amount_label.grid(row=2, column=0, pady=12, padx=10)

        set_amount_box = ctk.CTkEntry(master=set_amount_frame, placeholder_text="Amount")
        set_amount_box.grid(row=3, column=0, pady=12, padx=10)

        set_amount_button = ctk.CTkButton(master=set_amount_frame, text="START", command=set_amount)
        set_amount_button.grid(row=4, column=0, pady=12, padx=10)



    def home_page(self):
        notifi.notification("Welcome", "Hello and welcomne to the app", "long")
        # Initialize the database and start the reminder checker
        setup_database()
        start_reminder_checker()

        self.title("Financiol")
        self.geometry("750x750")
        self.minsize(600, 400)

        self.base_width = 600
        self.base_height = 400

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        for i in range(7):
            self.main_frame.grid_rowconfigure(i, weight=1)

        # theme, currency, id, name = self.meta.get_data()
        # data = self.db_u.get_wallet(currency)
        self.amount_label = ctk.CTkLabel(
            self.main_frame, 
            text=f"Amount: ${self.__db.get_wallet(f'{self.json.get_data()[1]}')[self.json.get_data()[1]]} {self.json.get_data()[1]}",
            font=("Arial", self.calculate_font_size())
        )
        self.amount_label.grid(row=0, column=0, pady=10, sticky="nsew")
        # this is the list of buttons that will be displayed on the home page
        self.buttons = []
        button_texts = [
            "Add/Subtract Amount",
            "Transaction History",
            "Graph History",
            "Open Calculator",
            "Add Reminder"  # New button added here
        ]
        button_functions = [
            self.add_subtract_amount,
            self.history,
            self.graphs,
            self.open_calc,
            self.add_reminder
        ]
        # this is the frame that will hold the buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, rowspan=5, sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=0)
        self.button_frame.grid_columnconfigure(2, weight=1)
        # this loop creates the buttons and adds them to the button frame
        for i, text in enumerate(zip(button_texts, button_functions)):
            button = ctk.CTkButton(
                self.button_frame,
                text=text[0],
                corner_radius=20,
                height=self.calculate_button_height(),
                width=self.calculate_button_width(),
                command=text[1]  # Link the button to the add_reminder method
            )

            button.grid(row=i, column=1, pady=10)
            self.buttons.append(button)
        # this is the settings button that will open the settings menu
        self.settings_button = ctk.CTkButton(
            self.main_frame,
            text="Settings",
            corner_radius=20,
            command=self.toggle_settings_menu,
            width=self.calculate_button_width() // 2
        )
        self.settings_button.grid(row=6, column=0, pady=10, sticky="ne", padx=20)

        self.setup_settings_frame()
        self.bind("<Configure>", self.on_resize)
    # this function sets up the settings menu
    def setup_settings_frame(self):
        def log_out():
            del self.__db
            self.json.log_out()
            self.main_frame.grid_forget()
            self.settings_frame.grid_remove()
            self.log_in()
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid_columnconfigure(0, weight=1)
        # this is the dark mode switch
        self.mode_switch = ctk.CTkSwitch(
            self.settings_frame,
            text="Dark Mode",
            command=self.toggle_mode
        )
        self.mode_switch.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        # this is the change theme button
        self.theme_button = ctk.CTkButton(
            self.settings_frame,
            text="Change Theme",
            corner_radius=20,
            command=lambda: change_theme_callback(self.theme_manager)
        )
        self.theme_button.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        # this is the logout button
        self.logout_button = ctk.CTkButton(
            self.settings_frame,
            text="Logout",
            corner_radius=20,
            command=log_out
        )
        self.logout_button.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
        # this is the close settings button
        self.close_settings_button = ctk.CTkButton(
            self.settings_frame,
            text="Close Settings",
            corner_radius=20,
            command=self.toggle_settings_menu
        )
        self.close_settings_button.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

        self.settings_visible = False
        self.settings_frame.grid_remove()

        self.theme_manager = ThemeManager(self, customtkinter_mode=True)
    # this function calculates the font size for the amount label
    def calculate_font_size(self):
        window_height = self.winfo_height()
        return max(24, int(window_height * 0.06))
    # these two functions calculate the size of the buttons based on the window
    def calculate_button_width(self):
        window_width = self.winfo_width()
        return int(window_width * 0.25 * 0.7)  # Reduce width by 30%

    def calculate_button_height(self):
        window_height = self.winfo_height()
        return int(window_height * 0.08 * 0.7)  # Reduce height by 30%
    # this function toggles the settings menu
    def toggle_settings_menu(self):
        if self.settings_visible:
            self.settings_frame.grid_remove()
        else:
            self.settings_frame.grid(row=0, column=0, sticky="ne", padx=20, pady=20)
        self.settings_visible = not self.settings_visible
    # this function toggles the appearance mode
    def toggle_mode(self):
        self.json.theme_change()
        if self.mode_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
    # this function is called when the window is resized
    def on_resize(self, event):
        if event.widget != self:
            return

        self.amount_label.configure(font=("Arial", self.calculate_font_size()))
        button_height = self.calculate_button_height()
        button_width = self.calculate_button_width()
        # this loop resizes the buttons
        for button in self.buttons:
            button.configure(height=button_height, width=button_width)

        self.settings_button.configure(height=button_height, width=button_width // 2)
    
    # this function is called when the user clicks the add reminder button (do the same with calculator)
    def add_reminder(self):
        # Create a new window for adding a reminder
        reminder_window = ctk.CTkToplevel(self)
        reminder_window.title("Add Reminder")
        reminder_window.geometry("300x200")

        # Date entry
        date_label = ctk.CTkLabel(reminder_window, text="Date (YYYY-MM-DD):")
        date_label.pack(pady=5)
        date_entry = ctk.CTkEntry(reminder_window)
        date_entry.pack(pady=5)

        # Time entry
        time_label = ctk.CTkLabel(reminder_window, text="Time (HH:MM):")
        time_label.pack(pady=5)
        time_entry = ctk.CTkEntry(reminder_window)
        time_entry.pack(pady=5)

        # AM/PM entry
        ampm_label = ctk.CTkLabel(reminder_window, text="AM/PM:")
        ampm_label.pack(pady=5)
        ampm_entry = ctk.CTkEntry(reminder_window)
        ampm_entry.pack(pady=5)

        # Reminder text entry
        text_label = ctk.CTkLabel(reminder_window, text="Reminder Text:")
        text_label.pack(pady=5)
        text_entry = ctk.CTkEntry(reminder_window)
        text_entry.pack(pady=5)

        # Submit button
        submit_button = ctk.CTkButton(
            reminder_window,
            text="Submit",
            command=lambda: self.submit_reminder(
                date_entry.get(),
                time_entry.get(),
                text_entry.get(),
                ampm_entry.get(),
                reminder_window
            )
        )
        submit_button.pack(pady=10)

    def submit_reminder(self, date, time, text, ampm, window):
        try:
            submit_reminder(date, time, text, ampm)
            messagebox.showinfo("Success", "Reminder added successfully!")
            window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def add_subtract_amount(self):
        def work(operation):
            category = category_entry.get()
            currency = currency_entry.get()
            amount = amount_entry.get()
            self.__db.add_history(amount, currency, operation, category)
            self.__db.edit_wallet(currency, int(amount), operation)
        
        def add():
            work(db.DB_enums.ADD)
        
        def sub():
            work(db.DB_enums.SUB)
        # Create a new window for adding or subtracting amount
        amount_window = ctk.CTkToplevel(self)
        amount_window.title("Add/Subtract Amount")
        amount_window.geometry("500x600")

        # Category entry
        category_label = ctk.CTkLabel(amount_window, text="Category:")
        category_label.pack(pady=5)
        category_entry = ctk.CTkEntry(amount_window)
        category_entry.pack(pady=5)
        # Details entry
        details_label = ctk.CTkLabel(amount_window, text="Details:")
        details_label.pack(pady=5)
        details_entry = ctk.CTkEntry(amount_window)
        details_entry.pack(pady=5)

        # Currency entry
        currency_label = ctk.CTkLabel(amount_window, text="Currency:")
        currency_label.pack(pady=5)
        currency_entry = ctk.CTkEntry(amount_window)
        currency_entry.pack(pady=5)

        # Amount entry
        amount_label = ctk.CTkLabel(amount_window, text="Amount:")
        amount_label.pack(pady=5)
        amount_entry = ctk.CTkEntry(amount_window)
        amount_entry.pack(pady=5)

        # Submit button
        add_button = ctk.CTkButton(amount_window, text="Add", command=add)
        add_button.pack(pady=10)

        sub_button = ctk.CTkButton(amount_window, text="Subtract", command=sub)
        sub_button.pack(pady=10)
    
    def history(self):
        amount_window = ctk.CTkToplevel(self)
        amount_window.title("History Table")
        amount_window.geometry("500x600")
         # Fetch history and convert it into a DataFrame
        cursor = self.__db.get_history()  
        df = self.df_it(cursor) 
        
        # Create a scrollable frame
        frame = ctk.CTkFrame(master=amount_window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Text widget to display DataFrame
        text_widget = ctk.CTkTextbox(master=frame, width=460, height=500)
        text_widget.pack(fill="both", expand=True)

        # Insert DataFrame content into the Text widget
        text_widget.insert("1.0", df.to_string(index=False))  # Format DataFrame to string without index
        text_widget.configure(state="disabled")  # Disable editing

        # Close button
        close_button = ctk.CTkButton(master=amount_window, text="Close", command=amount_window.destroy)
        close_button.pack(pady=10)

    def df_it(self, cursor):
        a = pd.DataFrame(
            columns=["time", "amount", "operation", "category", "currency", "transID"]
        )

        def add(x: list):
            a.loc[len(a)] = x

        b = [x for x in map(add, map(lambda z: list(z), cursor))]
        return a
    
    def graphs(self):
        theme = "dark" if ctk.get_appearance_mode() == "dark" else "light"
        charts.generate_graphs(self.__db, theme)  # Pass the current theme to the function
    
    def open_calc(self):
        currencies = db.DB_connection.CURRENCY 
        curr_list = list(currencies.keys())

        # Function to handle sale calculation
        def do_sale():
            value = float(sale_value_entry.get())
            percent = float(s_percent_entry.get())
            slope = 0
            full = s_change_var.get() == 0
            result = CalcOperations.partitioning(value, percent, slope, full)
            messagebox.showinfo("Sale Result", f"Result: {result:.2f}")

        # Function to handle tax calculation
        def do_Tax():
            value = float(tax_value_entry.get())
            percent = float(t_percent_entry.get())
            slope = 1
            full = t_change_var.get() == 0
            result = CalcOperations.partitioning(value, percent, slope, full)
            messagebox.showinfo("Tax Result", f"Result: {result:.2f}")    

        # Function to handle interest calculation
        def do_calc_interest():
            principal = float(principal_entry.get())
            rate = float(rate_entry.get())
            periods = int(period_entry.get())
            installments = installments_var.get() == 1
            result = CalcOperations.calc_interest(principal, rate, periods, installments)
            messagebox.showinfo("Interest Calculation Result", f"Result: {result:.2f}")

        # Function to handle currency exchange
        def do_currency_exchange():
            from_currency = from_currency_menu.get()
            to_currency = to_currency_menu.get()
            amount = float(amount_entry.get())
            result = CalcOperations.currency_exchange(from_currency, to_currency, amount)
            messagebox.showinfo("Currency Exchange Result", f" {amount} {from_currency} equall :{result:.2f} {to_currency}")


        # open sales
        def open_sale():
            calc_frame.grid_forget()
            sale_frame.grid(row=1, column=0, pady=20, padx=30)

        # open taxs
        def open_tax():
            calc_frame.grid_forget()
            tax_frame.grid(row=1, column=0, pady=20, padx=30)

        # open interest
        def open_interest():
            calc_frame.grid_forget()
            interest_frame.grid(row=1, column=0, pady=20, padx=30)    

        # open currency exchange
        def open_exchange():
            calc_frame.grid_forget()
            currency_frame.grid(row=1, column=0, pady=20, padx=30)

        # back to calc from sale
        def back_from_sale():
            sale_frame.grid_forget()
            calc_frame.grid(row=1, column=0, pady=20, padx=30)

        def back_from_tax():
            tax_frame.grid_forget()
            calc_frame.grid(row=1, column=0, pady=20, padx=30)    

        # back to calc from interest
        def back_from_inter():
            interest_frame.grid_forget()
            calc_frame.grid(row=1, column=0, pady=20, padx=30)

        # back to calc from currency exchange
        def back_from_curr():
            currency_frame.grid_forget()
            calc_frame.grid(row=1, column=0, pady=20, padx=30)    

        # Initialize the main window
        app =  ctk.CTkToplevel(self)
        app.geometry("500x600")
        app.title("Financial Calculations")

        # calculations frame
        calc_frame = ctk.CTkFrame(master=app)
        calc_frame.grid(row=1, column=0, pady=20, padx=30)

        sale_button = ctk.CTkButton(master=calc_frame,text="sales calc" , command=open_sale)
        sale_button.grid(row=0, column=0, pady=10, padx=20)
        
        tax_button = ctk.CTkButton(master=calc_frame,text="taxs calc" , command=open_tax)
        tax_button.grid(row=1, column=0, pady=10, padx=20)

        inter_button =  ctk.CTkButton(master=calc_frame,text="interest calc" , command=open_interest)
        inter_button.grid(row=2, column=0, pady=10, padx=20)

        curr_button = ctk.CTkButton(master=calc_frame,text="currency exchange" , command=open_exchange)
        curr_button.grid(row=3, column=0, pady=10, padx=20)

        
        # Frame for sale Calculation
        sale_frame = ctk.CTkFrame(master=app)

        sale_label = ctk.CTkLabel(master=sale_frame, text="sales Calculation", font=("Arial", 16))
        sale_label.grid(row=0, column=0, pady=10)

        sale_value_entry = ctk.CTkEntry(master=sale_frame,placeholder_text="enter value")
        sale_value_entry.grid(row=1, column=0, pady=5)

        s_percent_entry = ctk.CTkEntry(master=sale_frame, placeholder_text="percent")
        s_percent_entry.grid(row=2, column=0, pady=5)

        s_change_var = ctk.IntVar()
        s_change_check = ctk.CTkCheckBox(master=sale_frame, text="return change", variable=s_change_var)
        s_change_check.grid(row=3, column=0, pady=5)

        sale_button = ctk.CTkButton(master=sale_frame, text="Calculate sale", command=do_sale)
        sale_button.grid(row=4, column=0, pady=10)

        back_button = ctk.CTkButton(master=sale_frame ,text="Back",command=back_from_sale)
        back_button.grid(row=5, column=0, pady=5)



        # Frame for tax Calculation
        tax_frame = ctk.CTkFrame(master=app)

        tax_label = ctk.CTkLabel(master=tax_frame, text="Tax Calculation", font=("Arial", 16))
        tax_label.grid(row=0, column=0, pady=10)

        tax_value_entry = ctk.CTkEntry(master=tax_frame,placeholder_text="enter value")
        tax_value_entry.grid(row=1, column=0, pady=5)

        t_percent_entry = ctk.CTkEntry(master=tax_frame, placeholder_text="percent")
        t_percent_entry.grid(row=2, column=0, pady=5)

        t_change_var = ctk.IntVar()
        t_change_check = ctk.CTkCheckBox(master=tax_frame,text="return change", variable=t_change_var)
        t_change_check.grid(row=3, column=0, pady=5)

        tax_button = ctk.CTkButton(master=tax_frame, text="Calculate Tax", command=do_Tax)
        tax_button.grid(row=4, column=0, pady=10)

        back_button = ctk.CTkButton(master=tax_frame ,text="Back",command=back_from_tax)
        back_button.grid(row=5, column=0, pady=5)



        # Frame for Interest Calculation
        interest_frame = ctk.CTkFrame(master=app)

        interest_label = ctk.CTkLabel(master=interest_frame, text="Interest Calculation", font=("Arial", 16))
        interest_label.grid(row=0, column=0, pady=10)

        principal_entry = ctk.CTkEntry(master=interest_frame,placeholder_text="principal")
        principal_entry.grid(row=1, column=0, pady=5)

        rate_entry = ctk.CTkEntry(master=interest_frame,placeholder_text="Rate")
        rate_entry.grid(row=2, column=0, pady=5)

        period_entry = ctk.CTkEntry(master=interest_frame,placeholder_text="period")
        period_entry.grid(row=3, column=0, pady=5)

        installments_var = ctk.IntVar()
        installments_check = ctk.CTkCheckBox(master=interest_frame, text="Installments", variable=installments_var)
        installments_check.grid(row=4, column=0, pady=5)

        interest_button = ctk.CTkButton(master=interest_frame, text="Calculate Interest", command=do_calc_interest)
        interest_button.grid(row=5, column=0, pady=10)

        back_button = ctk.CTkButton(master=interest_frame ,text="Back",command=back_from_inter)
        back_button.grid(row=6, column=0, pady=5)



        # Frame for Currency Exchange
        currency_frame = ctk.CTkFrame(master=app)

        currency_label = ctk.CTkLabel(master=currency_frame, text="Currency Exchange", font=("Arial", 16))
        currency_label.grid(row=0, column=0, pady=10)

        from_currency_label = ctk.CTkLabel(master=currency_frame, text="From Currency")
        from_currency_label.grid(row=1, column=0, pady=5)
        from_currency_menu = ctk.CTkOptionMenu(master=currency_frame,values=curr_list)
        from_currency_menu.grid(row=2, column=0, pady=5)

        to_currency_label = ctk.CTkLabel(master=currency_frame, text="To Currency")
        to_currency_label.grid(row=3, column=0, pady=5)
        to_currency_menu = ctk.CTkOptionMenu(master=currency_frame,values=curr_list)
        to_currency_menu.grid(row=4, column=0, pady=5)

        amount_entry = ctk.CTkEntry(master=currency_frame,placeholder_text="Amount")
        amount_entry.grid(row=5, column=0, pady=5)

        currency_button = ctk.CTkButton(master=currency_frame, text="Exchange Currency", command=do_currency_exchange)
        currency_button.grid(row=6, column=0, pady=5)

        back_button = ctk.CTkButton(master=currency_frame ,text="Back",command=back_from_curr)
        back_button.grid(row=7, column=0, pady=5)
        
# this is the main function that runs the home page
if __name__ == "__main__":
     self = HomePage()
     self.mainloop()
