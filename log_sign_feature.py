import customtkinter as ctk
import testingjson
from db import *

db = DB_accounts()

def res_lab(app):
    result_label = ctk.CTkLabel(master=app, text="")
    result_label.pack(pady=6, padx=10)
    return result_label

def log_in(app):
    app.geometry("300x450")
    app.title("Login & Sign Up")

    result_label = res_lab(app)

    def login_user():
        username = login_box.get()
        password = password_box.get()
        try:
            id, y, primary_currency = db.login(username, password)
            result_label.configure(text=f"Login successfull", text_color="green")
            testingjson.Meta_data().set_new_account(False, id, primary_currency, username)

            DB_connection.config(f"user{id}db.db") # PUT WAHT YOU WANT TO LOGIN HERE ///////////////////////////////////////////
            login_frame.pack_forget()
        except ValueError as s :
            result_label.configure(text=str(s), text_color="red") # wrong password
    

    def switch_to_signup():  # switch to the Sign-Up frame 
        login_frame.pack_forget()
        sign_up(app)

    login_frame = ctk.CTkFrame(master=app)
    login_frame.pack(pady=20, padx=30)

    login_label = ctk.CTkLabel(master=login_frame, text="Login", font=("Arial", 16))
    login_label.pack(pady=12, padx=10)

    login_box = ctk.CTkEntry(master=login_frame, placeholder_text="Username")
    login_box.pack(pady=12, padx=10)

    password_box = ctk.CTkEntry(master=login_frame, placeholder_text="Password", show="*")
    password_box.pack(pady=12, padx=10)

    login_button = ctk.CTkButton(master=login_frame, text="Login", command=login_user)
    login_button.pack(pady=12, padx=10)

    login_question_label = ctk.CTkLabel(master=login_frame, text="Don't have an account?")
    login_question_label.pack(pady=6, padx=10)

    signup_switch_button = ctk.CTkButton(master=login_frame, text="Sign Up", command=switch_to_signup)
    signup_switch_button.pack(pady=6, padx=10)


def sign_up(app):
    signup_frame = ctk.CTkFrame(master=app)
    signup_frame.pack(pady=20, padx=30)

    result_label =  res_lab(app)

    def register_user():  # registeration function
        username = username_box.get()
        if db.uniquness(username):
            signup_frame.pack_forget()
            set_amount_frame.pack(pady=20, padx=30)
            result_label.configure(text="Registration successful", text_color="green")

        else:
            result_label.configure(text="Username already taken", text_color="red")


    def switch_to_login():  # switch to the Login frame
        signup_frame.pack_forget()
        log_in(app)


    def set_amount():
        amount = set_amount_box.get()
        username = username_box.get()
        password = password_box_reg.get()
        primary_currency = currency_entry.get()

        db.add_account(username, password, primary_currency)
        id, y, z = db.login(username, password)
        testingjson.Meta_data().set_new_account(False, id, primary_currency, username)

        DB_connection.config(f"user{id}db.db")
        dbc = DB_connection()
        dbc.add_wallet(primary_currency,amount)
        set_amount_frame.pack_forget() # /////////////////////////////////////////////////////////////////////////////////////



    signup_label = ctk.CTkLabel(master=signup_frame, text="Sign Up", font=("Arial", 16))
    signup_label.pack(pady=12, padx=10)

    username_box = ctk.CTkEntry(master=signup_frame, placeholder_text="Username")
    username_box.pack(pady=12, padx=10)

    password_box_reg = ctk.CTkEntry(master=signup_frame, placeholder_text="Password", show="*")
    password_box_reg.pack(pady=12, padx=10)

    register_button = ctk.CTkButton(master=signup_frame, text="Register", command=register_user)
    register_button.pack(pady=12, padx=10)

    signup_question_label = ctk.CTkLabel(master=signup_frame, text="Already have an account?")
    signup_question_label.pack(pady=6, padx=10)

    login_switch_button = ctk.CTkButton(master=signup_frame, text="Login", command=switch_to_login)
    login_switch_button.pack(pady=6, padx=10)
    
    #set_amount frame
    set_amount_frame = ctk.CTkFrame(master=app)

    set_currency_label = ctk.CTkLabel(master=set_amount_frame, text="Set primary currency", font=("Arial", 16))
    set_currency_label.pack(pady=12, padx=10)

    currency_entry = ctk.CTkEntry(master=set_amount_frame, placeholder_text="Primary Currency")
    currency_entry.pack(pady=12, padx=10)

    set_amount_label = ctk.CTkLabel(master=set_amount_frame, text="Set Amount", font=("Arial", 16))
    set_amount_label.pack(pady=12, padx=10)

    set_amount_box = ctk.CTkEntry(master=set_amount_frame , placeholder_text="Amount")
    set_amount_box.pack(pady=12 , padx=10)

    set_amount_button = ctk.CTkButton(master=set_amount_frame,text="START",command=set_amount)
    set_amount_button.pack(pady=12 , padx=10)
