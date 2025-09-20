import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
import random, os, sys, winsound, time

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

