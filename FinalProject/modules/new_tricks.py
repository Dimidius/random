import tkinter as tk
from tkinter import ttk
import pywinstyles
from PIL import Image, ImageTk, ImageOps
import random, os, sys, winsound, time, subprocess
try:
    from . import snake
except ImportError:
    import snake


class TrickApp:
    def __init__(self, master):
        self.master = master
        self.tricks_win = None  # keep reference to avoid reopening

    def tricks_menu(self):
        # Check if the window already exists
        if self.tricks_win and self.tricks_win.winfo_exists():
            self.tricks_win.lift()
            return

        # Create a new Toplevel (child window)
        self.tricks_win = tk.Toplevel(self.master)
        self.tricks_win.title("Trick Learning App")
        self.tricks_win.geometry("600x500")
        self.tricks_win.config(bg="#40414a")
        pywinstyles.change_header_color(self.tricks_win, "#2c2d33")

        # EPIC MAINFRAME MOMENT
        main_frame = tk.Frame(self.tricks_win, padx=10, pady=10, bg="#40414a")
        main_frame.pack(expand=True, fill="both")
        main_frame.grid_columnconfigure(0, weight=1)
        
        separator = tk.Frame(main_frame, bg="white", height=2)
        separator.grid(row=1, column=0, sticky="ew", padx=40, pady=(0, 10))

        # --- Title Label ---
        title_label = tk.Label(
            main_frame,
            text="Learn a New Trick!",
            bg="#40414a",
            fg="white",
            font=("Arial", 20, "bold")
        )
        title_label.grid(row=0, column=0, pady=20, sticky="n")

        snake_label = tk.Label(
            main_frame,
            text="Snake",
            bg="#40414a",
            fg="white",
            font=("Arial", 12)
        )
        snake_label.grid(row=2, column=0, pady=20)

        snake_btn = tk.Button(
            main_frame,
            text="SNAKE",
            command=lambda: subprocess.Popen([sys.executable, "FinalProject/modules/snake.py"])
        )
        snake_btn.grid(row=3, column=0, pady=20)

    def close_tricks_menu(self):
        if self.tricks_win and self.tricks_win.winfo_exists():
            self.tricks_win.destroy()
        self.tricks_win = None

# if __name__ == "__main__":
#     app = TrickApp()
