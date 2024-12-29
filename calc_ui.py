import customtkinter as ctk
from calc_operatinos import CalcOperations
from tkinter import messagebox
from db import DB_connection

currencies = DB_connection.CURRENCY 
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
app = ctk.CTk()
app.geometry("400x600")
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

def open_clac():
     app.mainloop()