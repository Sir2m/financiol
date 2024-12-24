import sqlite3
from tkinter import Tk, Label, Entry, Button, messagebox, ttk, StringVar
from winotify import Notification
import datetime
import threading
import time

class DateEntry(Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<KeyRelease>', self.format_date)
        self.last_text = ''

    def format_date(self, event):
        text = self.get()
        if text == self.last_text:
            return
        
        text = ''.join(filter(str.isdigit, text))
        formatted = ''
        
        if len(text) > 0:
            formatted = text[:4]
            if len(text) > 4:
                formatted += '-' + text[4:6]
            if len(text) > 6:
                formatted += '-' + text[6:8]
            
            formatted = formatted[:10]
        
        if formatted != self.get():
            self.delete(0, 'end')
            self.insert(0, formatted)
        
        self.last_text = formatted

class TimeEntry(Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<KeyRelease>', self.format_time)
        self.last_text = ''

    def format_time(self, event):
        text = self.get()
        if text == self.last_text:
            return
        
        text = ''.join(filter(str.isdigit, text))
        formatted = ''
        
        # Add colon after first two digits
        if len(text) >= 2:
            formatted = f"{text[:2]}:{text[2:4]}"
        else:
            formatted = text
            
        if formatted != self.get():
            self.delete(0, 'end')
            self.insert(0, formatted)
        
        self.last_text = formatted

def setup_database():
    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS reminders")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            text TEXT,
            ampm TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_reminder(date, time, text, ampm):
    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reminders (date, time, text, ampm) VALUES (?, ?, ?, ?)",
                  (date, time, text, ampm))
    conn.commit()
    conn.close()

def convert_to_24hr(time_str, ampm):
    try:
        time_obj = datetime.datetime.strptime(time_str, "%I:%M")
        if ampm == "PM" and time_obj.hour != 12:
            time_obj = time_obj.replace(hour=time_obj.hour + 12)
        elif ampm == "AM" and time_obj.hour == 12:
            time_obj = time_obj.replace(hour=0)
        return time_obj.strftime("%H:%M")
    except ValueError:
        return time_str

def check_reminders():
    while True:
        try:
            now = datetime.datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H:%M")

            conn = sqlite3.connect("reminders.db")
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, text, time, ampm 
                FROM reminders 
                WHERE date = ?
            """, (current_date,))
            
            reminders = cursor.fetchall()

            for reminder in reminders:
                reminder_24h = convert_to_24hr(reminder[2], reminder[3])
                if reminder_24h == current_time:
                    notify_user(reminder[1])
                    cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder[0],))
                    conn.commit()

            conn.close()
            time.sleep(30)
            
        except Exception as e:
            print(f"Error in check_reminders: {e}")
            time.sleep(30)

def notify_user(text):
    try:
        toast = Notification(
            app_id="Reminder",
            title="Reminder",
            msg=text,
            duration="long"
        )
        toast.show()
    except Exception as e:
        print(f"Notification error: {e}")
        messagebox.showinfo("Reminder", text)

def validate_datetime(date_str, time_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        datetime.datetime.strptime(time_str, "%I:%M")
        return True
    except ValueError:
        return False

def submit_reminder():
    date = date_entry.get().strip()
    time = time_entry.get().strip()
    text = text_entry.get().strip()
    ampm = time_period.get()

    if not (date and time and text):
        messagebox.showerror("Error", "All fields are required!")
        return

    if not validate_datetime(date, time):
        messagebox.showerror("Error", "Invalid date or time format!")
        return

    time_24h = convert_to_24hr(time, ampm)
    reminder_datetime = datetime.datetime.strptime(f"{date} {time_24h}", "%Y-%m-%d %H:%M")
    
    if reminder_datetime < datetime.datetime.now():
        messagebox.showerror("Error", "Cannot set reminder for past date/time!")
        return

    add_reminder(date, time, text, ampm)
    messagebox.showinfo("Success", "Reminder added successfully!")
    
    date_entry.delete(0, 'end')
    time_entry.delete(0, 'end')
    text_entry.delete(0, 'end')

# Initialize application
setup_database()

# Create main window
root = Tk()
root.title("Reminder")
root.resizable(False, False)

# Create and configure a main frame with padding
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky="nsew")

# Date Entry
Label(main_frame, text="Date (YYYY-MM-DD):", padx=5).grid(row=0, column=0, pady=5, sticky="e")
date_entry = DateEntry(main_frame, width=25)
date_entry.grid(row=0, column=1, columnspan=2, pady=5, padx=5, sticky="w")

# Time Entry with AM/PM
Label(main_frame, text="Time:", padx=5).grid(row=1, column=0, pady=5, sticky="e")
time_frame = ttk.Frame(main_frame)
time_frame.grid(row=1, column=1, columnspan=2, pady=5, sticky="w")

time_entry = TimeEntry(time_frame, width=10)
time_entry.grid(row=0, column=0, padx=(5,10))

time_period = StringVar(value="AM")
am_radio = ttk.Radiobutton(time_frame, text="AM", variable=time_period, value="AM")
pm_radio = ttk.Radiobutton(time_frame, text="PM", variable=time_period, value="PM")
am_radio.grid(row=0, column=1, padx=2)
pm_radio.grid(row=0, column=2, padx=2)

# Reminder Text
Label(main_frame, text="Reminder Text:", padx=5).grid(row=2, column=0, pady=5, sticky="e")
text_entry = Entry(main_frame, width=25)
text_entry.grid(row=2, column=1, columnspan=2, pady=5, padx=5, sticky="w")

# Add Button
Button(main_frame, text="Add Reminder", command=submit_reminder, width=20).grid(row=3, column=0, columnspan=3, pady=10)

# Start background thread
thread = threading.Thread(target=check_reminders, daemon=True)
thread.start()

root.mainloop()