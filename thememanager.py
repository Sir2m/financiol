import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

class ThemeManager:
    def __init__(self, parent_window):
        """
        Initialize the ThemeManager.
        
        Args:
            parent_window: The parent tkinter window/frame where theme manager will be integrated
        """
        self.parent = parent_window
        
        # Default theme settings
        self.default_theme = {
            "background": "#ffffff",
            "foreground": "#000000",
            "button_bg": "#e1e1e1",
            "button_fg": "#000000",
            "entry_bg": "#ffffff",
            "entry_fg": "#000000",
            "label_bg": "#ffffff",
            "label_fg": "#000000"
        }
        
        self.current_theme = self.default_theme.copy()
    
    def create_theme_frame(self):
        """Create and return a frame with theme controls"""
        theme_frame = tk.Frame(self.parent)
        
        # Theme controls
        tk.Button(theme_frame, text="Load Theme", 
                 command=self.load_theme).pack(side=tk.LEFT, padx=5)
        tk.Button(theme_frame, text="Reset Theme", 
                 command=self.reset_theme).pack(side=tk.LEFT, padx=5)
        
        return theme_frame
    
    def apply_theme_to_widget(self, widget):
        """
        Apply theme to a specific widget based on its type.
        
        Args:
            widget: The tkinter widget to apply theme to
        """
        if isinstance(widget, tk.Label):
            widget.configure(
                bg=self.current_theme["label_bg"],
                fg=self.current_theme["label_fg"]
            )
        elif isinstance(widget, tk.Entry):
            widget.configure(
                bg=self.current_theme["entry_bg"],
                fg=self.current_theme["entry_fg"]
            )
        elif isinstance(widget, tk.Button):
            widget.configure(
                bg=self.current_theme["button_bg"],
                fg=self.current_theme["button_fg"]
            )
        elif isinstance(widget, tk.Frame):
            widget.configure(bg=self.current_theme["background"])
    
    def apply_theme_to_window(self, window):
        """
        Apply theme to an entire window and its widgets recursively.
        
        Args:
            window: The tkinter window/frame to apply theme to
        """
        # Apply theme to the window itself
        if isinstance(window, tk.Tk) or isinstance(window, tk.Toplevel):
            window.configure(bg=self.current_theme["background"])
        
        self.apply_theme_to_widget(window)
        
        # Apply theme to all child widgets recursively
        for widget in window.winfo_children():
            self.apply_theme_to_widget(widget)
            if isinstance(widget, tk.Frame):
                self.apply_theme_to_window(widget)
    
    def load_theme(self):
        """Load theme from a JSON file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            title="Select Theme File"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    new_theme = json.load(file)
                    # Validate theme data
                    if all(key in new_theme for key in self.default_theme.keys()):
                        self.current_theme = new_theme
                        self.apply_theme_to_window(self.parent)
                        messagebox.showinfo("Success", "Theme loaded")
                    else:
                        raise ValueError("Invalid theme format")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load theme: {str(e)}")
    
    def reset_theme(self):
        """Reset theme to default"""
        self.current_theme = self.default_theme.copy()
        self.apply_theme_to_window(self.parent)
        messagebox.showinfo("Success", "Theme reset to default!")
    
    def get_current_theme(self):
        """Return the current theme dictionary"""
        return self.current_theme.copy()
    
    def set_theme(self, theme_dict):
        """
        Set a new theme programmatically.
        
        Args:
            theme_dict: Dictionary containing theme colors
        
        Returns:
            bool: True if theme was applied successfully, False otherwise
        """
        try:
            if all(key in theme_dict for key in self.default_theme.keys()):
                self.current_theme = theme_dict.copy()
                self.apply_theme_to_window(self.parent)
                return True
            return False
        except Exception:
            return False