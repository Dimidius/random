import tkinter as tk
from tkinter import ttk

class TheMenu:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("The Menu")
        self.root.geometry("300x200")
        self.root.overrideredirect(True)
        
        # State 
        self.hunger = 100  # initial hunger level
        
        self.label = tk.Label(root, text="The Menu", font=("Arial", 24))
        self.label.pack(expand=True)

        self.button = tk.Button(root, text="Close", command=self.root.destroy)
        self.button.pack(pady=20)

        # Click and drag to move window
        self.root.bind("<ButtonPress-1>", self.on_press)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<ButtonRelease-1>", self.on_release)
        self.start_x = 0
        self.start_y = 0

        self.hungy = ttk.Progressbar(
            root, orient="horizontal", length=200, mode="determinate", maximum=100
        )
        self.hungy.pack(pady=10)
        self.hungy['value'] = self.hunger

        self.decrease_hunger()

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
    
    def on_drag(self, event):
        new_x = self.root.winfo_x() + event.x - self.start_x
        new_y = self.root.winfo_y() + event.y - self.start_y
        self.root.geometry(f"+{new_x}+{new_y}")

    def on_release(self, event):
        pass

    def decrease_hunger(self):
        if self.hunger > 0:
            self.hunger -= 1
            self.hungy['value'] = self.hunger
            self.root.after(1000, self.decrease_hunger)  

if __name__ == "__main__":
    root = tk.Tk()
    menu = TheMenu(root)
    root.mainloop()