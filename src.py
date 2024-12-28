import db
import testingjson
import customtkinter as ctk

json = testingjson.Meta_data()
meta = json.get_data()

app = ctk.CTk()

if meta[2]:
    app.geometry("300x450")
    app.title("Hey There")
else:
    app.geometry("300x450")
    app.title("Login & Sign Up")
    
    result_label = ctk.CTkLabel(master=app, text="")
    result_label.pack(pady=6, padx=10)

app.mainloop()
json.save()