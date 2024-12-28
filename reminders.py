import sqlite3
from winotify import Notification
import datetime
import threading
import time

def setup_database():
    """
    Sets up the SQLite database for storing reminders. 
    Drops the `reminders` table if it exists and recreates it.
    """
    print("Setting up database...")
    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()
    # Create reminders table
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
    print("Database setup complete.")

def add_reminder(date, time, text, ampm):
    """
    Adds a new reminder to the database.

    Parameters:
    - date (str): Reminder date in the format 'YYYY-MM-DD'.
    - time (str): Reminder time in the format 'HH:MM'.
    - text (str): Reminder message.
    - ampm (str): Time period ('AM' or 'PM').
    """
    print(f"Adding reminder: {date} {time} {ampm} - {text}")
    conn = sqlite3.connect("reminders.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reminders (date, time, text, ampm) VALUES (?, ?, ?, ?)",
                  (date, time, text, ampm))
    conn.commit()
    conn.close()
    print("Reminder added.")

def convert_to_24hr(time_str, ampm):
    """
    Converts a time string from 12-hour format to 24-hour format.

    Parameters:
    - time_str (str): Time in the format 'HH:MM'.
    - ampm (str): Time period ('AM' or 'PM').

    Returns:
    - str: Time in 24-hour format.
    """
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
    """
    Continuously checks the database for reminders that match the current date and time.
    Sends notifications for due reminders and deletes them from the database.
    """
    while True:
        try:
            now = datetime.datetime.now()
            current_date = now.strftime("%Y-%m-%d")
            current_time = now.strftime("%H:%M")

            conn = sqlite3.connect("reminders.db")
            cursor = conn.cursor()
            
            # Fetch reminders for the current date
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
            time.sleep(30)  # Check every 30 seconds
            
        except Exception as e:
            print(f"Error in check_reminders: {e}")
            time.sleep(30)

def notify_user(text):
    """
    Sends a desktop notification for a reminder.

    Parameters:
    - text (str): Reminder message.
    """
    try:
        print(f"Notifying user: {text}")
        toast = Notification(
            app_id="Reminder",
            title="Reminder",
            msg=text,
            duration="long"
        )
        toast.show()
    except Exception as e:
        print(f"Notification error: {e}")

def validate_datetime(date_str, time_str):
    """
    Validates the format of a date and time string.

    Parameters:
    - date_str (str): Date in the format 'YYYY-MM-DD'.
    - time_str (str): Time in the format 'HH:MM'.

    Returns:
    - bool: True if both date and time are valid, False otherwise.
    """
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        datetime.datetime.strptime(time_str, "%I:%M")
        return True
    except ValueError:
        return False

def submit_reminder(date, time, text, ampm):
    """
    Validates and adds a reminder to the database.

    Parameters:
    - date (str): Reminder date in the format 'YYYY-MM-DD'.
    - time (str): Reminder time in the format 'HH:MM'.
    - text (str): Reminder message.
    - ampm (str): Time period ('AM' or 'PM').

    Raises:
    - ValueError: If any input is invalid or if the reminder is set for a past time.
    """
    if not (date and time and text):
        raise ValueError("All fields are required!")

    if not validate_datetime(date, time):
        raise ValueError("Invalid date or time format!")

    time_24h = convert_to_24hr(time, ampm)
    reminder_datetime = datetime.datetime.strptime(f"{date} {time_24h}", "%Y-%m-%d %H:%M")
    
    if reminder_datetime < datetime.datetime.now():
        raise ValueError("Cannot set reminder for past date/time!")

    add_reminder(date, time, text, ampm)

def start_reminder_checker():
    """
    Starts a background thread to continuously check for due reminders.
    """
    print("Starting reminder checker...")
    thread = threading.Thread(target=check_reminders, daemon=True)
    thread.start()
    print("Reminder checker started.")

if __name__ == "__main__":
    setup_database()
