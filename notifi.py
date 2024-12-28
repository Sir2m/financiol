from winotify import Notification

def notification(title:str, message: str, duration: str | None = "short"):
    try:
        toast = Notification(
            app_id="Financiol",
            title=title,
            msg=message,
            duration=duration
        )
        toast.show()
    except Exception as e:
        print(f"Notification error: {e}")
