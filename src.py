import db
import testingjson
import log_sign_feature
import customtkinter as ctk

json = testingjson.Meta_data()
meta = json.get_data()

app = ctk.CTk()

if meta[2]:
    db.DB_connection.config(f"user{meta[2]}db.db")
else:
    log_sign_feature.log_in(app)

app.geometry("300x450")
app.title("Hey There")

app.mainloop()
json.save()