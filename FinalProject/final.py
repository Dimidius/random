import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
import random, os, sys, winsound, time
import json
import pywinstyles

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class DeskPet:
    STEP_SIZE = 2
    ANIMATION_INTERVAL = 50  # ms
    BEHAVIOR_MIN_MS = 1000
    BEHAVIOR_MAX_MS = 4000

    SAVE_FILE = resource_path("FinalProject/files/pet_state.json")

    def save_state(self):
        """Save current state to JSON file."""
        state = {
            "energy": self.energy,
            "hunger": self.hunger,
            "name": self.name_label.cget("text"),
        }
        with open(self.SAVE_FILE, "w") as f:
            json.dump(state, f)

    def load_state(self):
        """Load saved state from JSON file, if it exists."""
        try:
            with open(self.SAVE_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    raise ValueError("Empty JSON file")
                state = json.loads(content)

            self.energy = state.get("energy", 100)
            self.hunger = state.get("hunger", 100)
            self.name_label.config(text=state.get("name", "TriSarahTops"))

        except (FileNotFoundError, ValueError, json.JSONDecodeError):
            # Defaults if no save file or if JSON is invalid/empty
            self.energy = 100
            self.hunger = 100
            self.name_label.config(text="TriSarahTops")


    def open_menu(self):
        if hasattr(self, "menu_win") and self.menu_win.winfo_exists():
            self.menu_win.lift()
            return

        self.menu_win = tk.Toplevel(self.root)
        self.menu_win.title("Pet Menu")
        self.menu_win.geometry("300x300")
        self.menu_win.attributes("-topmost", True)
        self.menu_win.config(bg="#40414a")
        pywinstyles.change_header_color(self.menu_win, "#2c2d33")

        tk.Label(self.menu_win, text="Hunger", bg="#40414a", fg="white", font=("Arial", 12)).pack(pady=(20, 0))
        self.hunger_bar = ttk.Progressbar(self.menu_win, length=200, maximum=100)
        self.hunger_bar.pack(pady=5)
        self.hunger_bar['value'] = self.hunger

        tk.Label(self.menu_win, text="Energy", bg="#40414a", fg="white", font=("Arial", 12)).pack(pady=(20, 0))
        self.energy_bar = ttk.Progressbar(self.menu_win, length=200, maximum=100)
        self.energy_bar.pack(pady=5)
        self.energy_bar['value'] = self.energy

        tk.Label(self.menu_win, text="Feed Pet", bg="#40414a", fg="white", font=("Arial", 12)).pack(pady=(20, 0))

        tk.Button(self.menu_win, text="Apple: +5 Hunger", command=lambda: self.feed_food(5), width=20, background="#666773").pack(pady=5)
        tk.Button(self.menu_win, text="Sandwich: +15 Hunger", command=lambda: self.feed_food(15), width=20, background="#666773").pack(pady=5)
        tk.Button(self.menu_win, text="Pizza: +25 Hunger", command=lambda: self.feed_food(25), width=20, background="#666773").pack(pady=5)



    def update_menu_bars(self):
        # Only update if the menu exists and is open
        if hasattr(self, "menu_win") and self.menu_win.winfo_exists():
            self.hunger_bar["value"] = self.hunger
            self.energy_bar["value"] = self.energy

        # Always keep looping every second, regardless of menu state
        self.root.after(500, self.update_menu_bars)

    def __init__(self, root: tk.Tk):
        self.root = root
        self._configure_window()

        # Load sprites
        self.image_right = Image.open(resource_path("FinalProject/files/TriSarahTopsL.png"))
        self.image_left = ImageOps.mirror(self.image_right)

        self.pet_width, self.pet_height = self.image_right.size
        self.img = ImageTk.PhotoImage(self.image_right)

        # --- Container (bigger than sprite so label can fit) ---
        self.container_height = self.pet_height + 40  # 40px extra space for name label
        self.container_width = self.pet_width + 60
        self.container = tk.Frame(root, bg="white", width=self.container_width, height=self.container_height)
        self.container.pack_propagate(False)  # don't shrink to contents
        self.container.pack()

        self.name_label = tk.Label(
            self.container,
            text="TriSarahTops",
            font=("Arial", 14),
            fg="green",
            bg="white",
            border=0)   
        self.name_label.pack(side="top", anchor="n", fill="x")

        # Sprite image inside container (sticks to bottom)
        self.label = tk.Label(
            self.container,
            image=self.img,
            bg="white",
            height=self.pet_height,
            width=self.pet_width
        )
        self.label.pack(side="bottom")

        screen_w, screen_h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.screen_w, self.screen_h = screen_w, screen_h
        self.root.geometry(f"+{screen_w // 2}+{screen_h - self.container_height}")

        # States
        self.walking = False
        self.sitting = False
        self.direction = 0 # 1=right, 0 = idle,-1=left
        self.hunger = 100
        self.energy = 100

        self.load_state()

        # Bind Events
        self._bind_events()

        # Start behaviors
        self.animate()
        self.schedule_behavior()
        self.decrease_hunger()
        self.decrease_energy()

        # Save on exit
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.update_menu_bars()  # Start updating menu bars if open

    def _configure_window(self):
        """Set up transparent, undecorated always-on-top window."""
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "white")

    def _bind_events(self):
        """Attach mouse and keyboard interactions."""
        self.label.bind("<Button-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.do_drag)
        self.label.bind("<ButtonRelease-1>", self.stop_drag)
        self.root.bind("<Control-f>", lambda event: self.feed())
        self.root.bind("<Control-s>", lambda event: self.snacks())
        self.root.bind("<Control-d>", lambda event: self.toggle_bars())
        self.root.bind("<Button-3>", lambda e: self.root.destroy())
        self.root.bind("<Control-n>", lambda event: self.rename())
        self.root.bind("<Control-t>", lambda event: self.trick())
        self.root.bind("<Control-m>", lambda event: self.open_menu())

    def set_sprite(self):
        """Update sprite image based on direction and state."""
        if self.direction == 1:
            image = self.image_right
        elif self.direction == -1:
            image = self.image_left
        else:
            image = self.image_right  # idle defaults to facing right

        self.img = ImageTk.PhotoImage(image)
        self.label.config(image=self.img)
        self.label.image = self.img  # prevent garbage collection


    def start_drag(self, event):
        self.walking = False
        self.sitting = False
        self.x, self.y = event.x, event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + event.x - self.x
        y = self.screen_h - self.container_height # stick to bottom
        self.root.geometry(f"+{x}+{y}")

    def stop_drag(self, event):
        if not self.sitting:
            self.walking = True

    def sit(self):
        self.sitting = not self.sitting
        if self.sitting:
            self.walking = False
            self.direction = 0
        else:
            self.schedule_behavior()    

    def decrease_hunger(self):
        if self.hunger > 0:
            self.hunger -= 1
            self.root.after(8000, self.decrease_hunger)  # decrease hunger every 8 seconds
        else:
            if self.hunger <= 30:
                self.hungry = True
                pet_hungy = tk.Message(self.container, text="I'm hungry!", bg="white", fg="red", font=("Arial", 12))
                pet_hungy.pack()
                winsound.PlaySound(resource_path("FinalProject/files/fart-with-reverb.wav"), 
                    winsound.SND_ASYNC | winsound.SND_FILENAME)


    def decrease_energy(self):
        if self.energy > 0:
            self.energy -= 1
            self.root.after(6000, self.decrease_energy)  # decrease energy every 6 seconds

    def animate(self):
        if self.walking and self.direction != 0:
            step = self.direction * self.STEP_SIZE
            x = self.root.winfo_x() + step
            y = self.screen_h - self.container_height

            # Bounce at edges
            if x <= 0:
                x, self.direction = 0, 1
                self.set_sprite()
            elif x >= self.screen_w - self.pet_width:
                x, self.direction = self.screen_w - self.pet_width, -1
                self.set_sprite()

            self.root.geometry(f"+{x}+{y}")

        self.root.after(self.ANIMATION_INTERVAL, self.animate)

    def schedule_behavior(self):
        """Randomly change behavior unless sitting."""
        if self.sitting:
            return

        choice = random.choice(["left", "right", "stop"])
        if choice == "left":
            self.direction, self.walking = -1, True
        elif choice == "right":
            self.direction, self.walking = 1, True
        else:
            self.direction, self.walking = 0, False

        self.set_sprite()
        interval = random.randint(self.BEHAVIOR_MIN_MS, self.BEHAVIOR_MAX_MS)
        self.root.after(interval, self.schedule_behavior)

    def trick(self):
        if self.energy >= 20:
            self.energy -= 20
            self.sitting = True
            self.walking = False
            self.backflip()
            self.root.after(2000, self.sit)  # sit for 2 seconds
        else:
            print("Not enough energy to perform trick.")

    def backflip(self, angle=0):
        if angle <= 180:
            rotated_image = self.image_right.rotate(angle)
            self.img = ImageTk.PhotoImage(rotated_image)
            self.label.config(image=self.img)
            self.label.image = self.img

            # Schedule next frame
            self.root.after(50, lambda: self.backflip(angle + 30))
        else:
            # Reset back to normal sprite
            self.set_sprite()

    def rename(self):
        self.name_label.pack_forget()
        self.name_entry = tk.Entry(
            self.container,
            font=("Arial", 14),
            fg="green",
            bg="white",   # matches transparent window
            border=0,
            justify="center"
        )
        self.name_entry.insert(0, self.name_label.cget("text"))
        self.name_entry.focus_set()
        self.name_entry.bind("<Return>", self.finish_rename)
        self.name_entry.pack(side="top", anchor="n", fill="x")

    def finish_rename(self, event):
        new_name = self.name_entry.get().strip()
        if new_name:
            self.name_label.config(text=new_name)
            self.save_state()  # save immediately when name changes
        self.name_entry.pack_forget()
        self.name_label.pack(side="top", anchor="n", fill="x")


    def on_close(self):
        """Save state before closing."""
        self.save_state()
        self.root.destroy()

    
if __name__ == "__main__":
    root = tk.Tk()
    DeskPet(root)
    root.mainloop()