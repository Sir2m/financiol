import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import testingjson
import db

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
    meta = testingjson.Meta_data()
    db_u = db.DB_connection()
    def __init__(self):
        super().__init__()

        self.title("Financiol")
        self.geometry("700x550")
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

        theme, currency, id, name = self.meta.get_data()
        data = self.db_u.get_wallet(currency)
        self.amount_label = ctk.CTkLabel(
            self.main_frame, 
            text=f"Amount: ${data[currency]}",
            font=("Arial", self.calculate_font_size())
        )
        self.amount_label.grid(row=0, column=0, pady=10, sticky="nsew")
        # this is the list of buttons that will be displayed on the home page
        self.buttons = []
        button_texts = [
            "Add Amount",
            "Subtract Amount",
            "Transaction History",
            "Graph History",
            "Open Calculator"
        ]
        # this is the frame that will hold the buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, rowspan=5, sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=0)
        self.button_frame.grid_columnconfigure(2, weight=1)
        # this loop creates the buttons and adds them to the button frame
        for i, text in enumerate(button_texts):
            button = ctk.CTkButton(
                self.button_frame,
                text=text,
                corner_radius=20,
                height=self.calculate_button_height(),
                width=self.calculate_button_width()
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
            corner_radius=20
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
        return int(window_width * 0.25)

    def calculate_button_height(self):
        window_height = self.winfo_height()
        return int(window_height * 0.08)
    # this function toggles the settings menu
    def toggle_settings_menu(self):
        if self.settings_visible:
            self.settings_frame.grid_remove()
        else:
            self.settings_frame.grid(row=0, column=0, sticky="ne", padx=20, pady=20)
        self.settings_visible = not self.settings_visible
    # this function toggles the appearance mode
    def toggle_mode(self):
        self.meta.theme_change()
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
# this is the main function that runs the home page
if __name__ == "__main__":
    app = HomePage()
    app.mainloop()
