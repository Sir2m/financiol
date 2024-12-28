import customtkinter as ctk
from tkinter import filedialog, messagebox
import json

class ThemeManager:
    def __init__(self, parent_window):
        self.parent = parent_window
        
        # Default theme settings for customtkinter
        self.default_theme = {
            "bg_color": "#ffffff",
            "fg_color": "#000000",
            "button_color": "#1e90ff",
            "button_hover": "#1c86ee",
            "entry_color": "#f0f0f0",
            "text_color": "#000000",
        }
        self.current_theme = self.default_theme.copy()
    
    def apply_theme_to_widget(self, widget):
        if isinstance(widget, ctk.CTkLabel):
            widget.configure(
                fg_color=self.current_theme["bg_color"],
                text_color=self.current_theme["text_color"]
            )
        elif isinstance(widget, ctk.CTkEntry):
            widget.configure(
                fg_color=self.current_theme["entry_color"],
                text_color=self.current_theme["text_color"]
            )
        elif isinstance(widget, ctk.CTkButton):
            widget.configure(
                fg_color=self.current_theme["button_color"],
                hover_color=self.current_theme["button_hover"],
                text_color=self.current_theme["text_color"]
            )
        elif isinstance(widget, ctk.CTkFrame):
            widget.configure(fg_color=self.current_theme["bg_color"])
    
    def apply_theme_to_window(self, window):
        if isinstance(window, (ctk.CTk, ctk.CTkToplevel)):
            window.configure(fg_color=self.current_theme["bg_color"])
        
        for widget in window.winfo_children():
            self.apply_theme_to_widget(widget)
            if isinstance(widget, ctk.CTkFrame):
                self.apply_theme_to_window(widget)
    
    def load_theme(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            title="Select Theme File"
        )
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    new_theme = json.load(file)
                    if all(key in new_theme for key in self.default_theme.keys()):
                        self.current_theme = new_theme
                        self.apply_theme_to_window(self.parent)
                        messagebox.showinfo("Success", "Theme loaded!")
                    else:
                        raise ValueError("Invalid theme format")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load theme: {str(e)}")
    
    def reset_theme(self):
        self.current_theme = self.default_theme.copy()
        self.apply_theme_to_window(self.parent)
        messagebox.showinfo("Success", "Theme reset to default!")

