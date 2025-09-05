import tkinter as tk
from tkinter import messagebox
from time import time

title = "Hey Baby!"
love = "I love you so fucking much!"

class LuvApp():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, love)
    root.destroy()
    root.after(900000) 

LuvApp()