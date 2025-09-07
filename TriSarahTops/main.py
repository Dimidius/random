import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import random

class TriSarahTopsApp:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  
        self.root.wm_attributes("-topmost", True)  
        self.root.wm_attributes("-transparentcolor", "white")  

        self.pet_image = Image.open("TriSarahTops/TriSarahTopsL.png")  
        self.img = ImageTk.PhotoImage(self.pet_image)

        self.label = tk.Label(root, image=self.img, bg="white")
        self.label.pack()

        self.pet_width = self.pet_image.width
        self.pet_height = self.pet_image.height

        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()

        self.root.geometry(f"+{self.screen_w//2}+{self.screen_h - self.pet_height}")

        self.walking = True
        self.direction = 0  

        self.label.bind("<ButtonPress-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)
        self.label.bind("<ButtonRelease-1>", self.end_move)

        self.sitting = False
        self.label.bind("<Control-Button-1>", self.toggle_sit)

        self.label.bind("<Button-3>", lambda e: root.destroy())

        self.animate()
        self.toggle_behavior()



    def set_image(self, direction):
        if direction > 0:  # Right
            img = self.pet_image  
        elif direction < 0: # Left
            img = ImageOps.mirror(self.pet_image)  
        else:  
            img = self.pet_image

        self.img = ImageTk.PhotoImage(img)
        self.label.configure(image=self.img)
        self.label.image = self.img  

    def start_move(self, event):
        self.walking = False  
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = self.root.winfo_x() + event.x - self.x
        y = self.screen_h - self.pet_height
        self.root.geometry(f"+{x}+{y}")

    def end_move(self, event):
        self.walking = True

    def toggle_sit(self, event):
        self.sitting = not self.sitting
        if self.sitting:
            self.walking = False
            self.direction = 0
        else:
            self.toggle_behavior()

    def animate(self):
        if self.walking and self.direction != 0:
            x = self.root.winfo_x() + self.direction
            y = self.screen_h - self.pet_height

            if x < 0:
                x = 0
                self.direction = 2 
                self.set_image(self.direction)
            elif x > self.screen_w - self.pet_width:
                x = self.screen_w - self.pet_width
                self.direction = -2  
                self.set_image(self.direction)
            self.root.geometry(f"+{x}+{y}")
        self.root.after(50, self.animate)

    def toggle_behavior(self):
        if self.sitting:
            return
        
        choice = random.choice(["left", "right", "stop"])
        if choice == "left":
            self.direction = -2
            self.walking = True
            self.set_image(self.direction)
        elif choice == "right":
            self.direction = 2
            self.walking = True
            self.set_image(self.direction)
        else:
            self.direction = 0
            self.walking = False

        interval = random.randint(1000, 4000)
        self.root.after(interval, self.toggle_behavior)


if __name__ == "__main__":
    root = tk.Tk()
    app = TriSarahTopsApp(root)
    root.mainloop()
