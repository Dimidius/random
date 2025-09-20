import tkinter as tk
from tkinter import ttk

class TheMenu:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("blue.Horizontal.TProgressbar", foreground='blue', background='blue')
        self.style.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
        self.root.title("The Menu")
        self.root.geometry("300x200")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "white")
        self.root.config(bg="white")

        # State 
        self.hunger = 100  # initial hunger level
        self.energy = 100  # initial energy level

        self.hungy = ttk.Progressbar(
            root, orient="horizontal", length=200, mode="determinate", maximum=100, style="green.Horizontal.TProgressbar")
        self.hungy.pack(pady=10, anchor="center")
        self.hungy['value'] = self.hunger

        self.energy_bar = ttk.Progressbar(
            root, orient="horizontal", length=200, style="blue.Horizontal.TProgressbar", mode="determinate", maximum=100)
        self.energy_bar.pack(anchor="center")
        self.energy_bar['value'] = self.energy

        self.root.bind("<Control-f>", lambda event: self.feed())
        self.root.bind("<Control-d>", lambda event: self.invis_bar())
        self.root.bind("<Control-s>", lambda event: self.snacks())
        self.start_x = 0
        self.start_y = 0

        self.decrease_hunger()
        self.energy_bar_stat()

    def center_window_x(self, width, height):
        screen_width = root.winfo_screenwidth()
        current_y = root.winfo_y()  # get current Y position

        x = (screen_width // 2) - (width // 2)
        root.geometry(f'{width}x{height}+{x}+{current_y}')

    def feed(self):
        if self.hunger < 100:
            self.hunger += 10
            self.hungy['value'] = self.hunger
        else:
            print("Hunger is already full.")

    def snacks(self):
        if self.hunger < 100:
            self.hunger += 5
            self.hungy['value'] = self.hunger
            self.energy += 20
            self.energy_bar['value'] = self.energy
        else:
            print("Hunger is already full.")

    def decrease_hunger(self):
        if self.hunger > 0:
            self.hunger -= 1
            self.hungy['value'] = self.hunger
            self.root.after(1000, self.decrease_hunger)

    def energy_bar_stat(self):
        if self.energy > 0:
            self.energy -= 1
            self.energy_bar['value'] = self.energy
            self.root.after(750, self.energy_bar_stat)

    def invis_bar(self):
        if self.hungy.winfo_ismapped() & self.energy_bar.winfo_ismapped():
            self.hungy.pack_forget()
            self.energy_bar.pack_forget()
        else:
            self.hungy.pack(pady=10, anchor="center")
            self.energy_bar.pack(anchor="center")

if __name__ == "__main__":
    root = tk.Tk()
    menu = TheMenu(root)
    TheMenu.center_window_x(root, 300, 200)
    root.mainloop()