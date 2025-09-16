import tkinter as tk

class DinoPetApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("DinoPet")
        self.root.geometry("400x300")

        self.label = tk.Label(self, text="Welcome to DinoPet!")
        self.label.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    DinoPetApp(root)
    root.mainloop()