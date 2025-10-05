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

    foods = [
        {"name": "Apple", "hunger_restore": 5},
        {"name": "Sandwich", "hunger_restore": 15},
        {"name": "Pizza", "hunger_restore": 25},
    ]

    snacks = [
        {"name": "Giffies", "hunger_restore": 2, "energy_restore": 5},
        {"name": "Chocolate Preztels", "hunger_restore": 5, "energy_restore": 10},
        {"name": "Dick", "energy_restore": 20},
    ]

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
            self.energy = 100
            self.hunger = 100
            self.name_label.config(text="TriSarahTops")

    def feed_food(self, food_name: str):
        """Feed the pet a specific type of food."""
        if getattr(self, "feeding", False):
            return
        self.feeding = True
        self.root.after(1500, lambda: setattr(self, "feeding", False))

        for food in self.foods:
            if food["name"] == food_name:
                self.hunger = min(100, self.hunger + food["hunger_restore"])
                msg = tk.Label(self.container, text=f"*Nom nom!* ({food['name']})", fg="orange", bg="white")
                msg.pack()
                self.root.after(1500, msg.destroy)
                self.update_menu_bars()
                self.save_state()
                return

    def feed_snack(self, snack_name: str):
        """Feed the pet a specific type of snack."""
        if getattr(self, "feeding", False):
            return
        self.feeding = True
        self.root.after(1500, lambda: setattr(self, "feeding", False))

        for snack in self.snacks:
            if snack["name"] == snack_name:
                if "hunger_restore" in snack:
                    self.hunger = min(100, self.hunger + snack["hunger_restore"])
                if "energy_restore" in snack:
                    self.energy = min(100, self.energy + snack["energy_restore"])

                msg = tk.Label(self.container, text=f"*Crunch crunch!* ({snack['name']})", fg="orange", bg="white")
                msg.pack()
                self.root.after(1500, msg.destroy)
                self.update_menu_bars()
                self.save_state()
                return

    def open_menu(self):
        if hasattr(self, "menu_win") and self.menu_win.winfo_exists():
            self.menu_win.lift()
            return

        self.menu_win = tk.Toplevel(self.root)
        self.menu_win.title("Pet Menu")
        self.menu_win.geometry("400x350")
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

        tk.Label(self.menu_win, text="Feed Pet", bg="#40414a", fg="white", font=("Arial", 12)).pack(pady=(20, 10))

        button_frame = tk.Frame(self.menu_win, bg="#40414a")
        button_frame.pack(pady=5)

        # Two columns — foods on left, snacks on right
        food_buttons = [
            ("Apple: +5 Hunger", lambda: self.feed_food("Apple")),
            ("Sandwich: +15 Hunger", lambda: self.feed_food("Sandwich")),
            ("Pizza: +25 Hunger", lambda: self.feed_food("Pizza"))
        ]
        snack_buttons = [
            ("Giffies: +2H, +5E", lambda: self.feed_snack("Giffies")),
            ("Choc. Pretzels: +5H, +10E", lambda: self.feed_snack("Chocolate Preztels")),
            ("Dick: +20 Energy", lambda: self.feed_snack("Dick"))
        ]

        for i, (text, cmd) in enumerate(food_buttons):
            tk.Button(button_frame, text=text, command=cmd, width=20, background="#666773").grid(row=i, column=0, padx=5, pady=5)
        for i, (text, cmd) in enumerate(snack_buttons):
            tk.Button(button_frame, text=text, command=cmd, width=22, background="#666773").grid(row=i, column=1, padx=5, pady=5)

    def update_menu_bars(self):
        if hasattr(self, "menu_win") and self.menu_win.winfo_exists():
            self.hunger_bar["value"] = self.hunger
            self.energy_bar["value"] = self.energy
        self.root.after(500, self.update_menu_bars)

    def __init__(self, root: tk.Tk):
        self.root = root
        self._configure_window()

        # Load sprites
        self.image_right = Image.open(resource_path("FinalProject/files/TriSarahTopsL.png"))
        self.image_left = ImageOps.mirror(self.image_right)

        self.pet_width, self.pet_height = self.image_right.size
        self.img = ImageTk.PhotoImage(self.image_right)

        # --- Container setup ---
        self.container_height = self.pet_height + 40
        self.container_width = self.pet_width + 60
        self.container = tk.Frame(root, bg="white", width=self.container_width, height=self.container_height)
        self.container.pack_propagate(False)
        self.container.pack(side="bottom", anchor="s")

        self.name_label = tk.Label(
            self.container,
            text="TriSarahTops",
            font=("Arial", 14),
            fg="green",
            bg="white",
            border=0)
        self.name_label.pack(side="top", anchor="n", fill="x")

        self.label = tk.Label(
            self.container,
            image=self.img,
            bg="white",
            height=self.pet_height,
            width=self.pet_width
        )
        self.label.pack(side="bottom")

        self.root.update_idletasks()
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.screen_w, self.screen_h = screen_w, screen_h
        offset_from_bottom = 100  # lift above taskbar, or positive to move lower
        self.root.geometry(f"+{screen_w // 2}+{screen_h - self.container_height + offset_from_bottom}")


        # States
        self.walking = False
        self.sitting = False
        self.direction = 0
        self.hunger = 100
        self.energy = 100

        self.load_state()
        self._bind_events()
        self.animate()
        self.schedule_behavior()
        self.decrease_hunger()
        self.decrease_energy()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.update_menu_bars()

    def _configure_window(self):
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "white")

    def _bind_events(self):
        self.label.bind("<Button-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.do_drag)
        self.label.bind("<ButtonRelease-1>", self.stop_drag)
        self.root.bind("<Button-3>", lambda e: self.on_close())
        self.root.bind("<Control-n>", lambda event: self.rename())
        self.root.bind("<Control-t>", lambda event: self.trick())
        self.root.bind("<Control-m>", lambda event: self.open_menu())
        self.root.bind("<Control-s>", lambda event: self.sit())

    def set_sprite(self):
        if self.direction == 1:
            image = self.image_right
        elif self.direction == -1:
            image = self.image_left
        else:
            image = self.image_right
        self.img = ImageTk.PhotoImage(image)
        self.label.config(image=self.img)
        self.label.image = self.img

    def start_drag(self, event):
        self.walking = False
        self.sitting = False
        self.x, self.y = event.x, event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + event.x - self.x
        y = self.screen_h - self.container_height  # stick to bottom
        self.root.geometry(f"+{x}+{y}")

    def stop_drag(self, event):
        if not self.sitting:
            self.walking = True

    def sit(self):
        self.sitting = not self.sitting
        if self.sitting:
            self.walking = False
            self.direction = 0
            self.root.after(3000, lambda: setattr(self, "energy", self.energy + 5))
        else:
            self.schedule_behavior()

    def decrease_hunger(self):
        if self.hunger > 0:
            self.hunger -= 1
            self.root.after(8000, self.decrease_hunger)
        else:
            if self.hunger <= 30:
                self.hungry = True
                pet_hungry = tk.Message(self.container, text="I'm hungry!", bg="white", fg="red", font=("Arial", 12))
                pet_hungry.pack()
                winsound.PlaySound(resource_path("FinalProject/files/fart-with-reverb.wav"),
                                   winsound.SND_ASYNC | winsound.SND_FILENAME)

    def decrease_energy(self):
        if self.energy > 0:
            self.energy -= 1
            self.root.after(6000, self.decrease_energy)

    def animate(self):
        if self.walking and self.direction != 0:
            step = self.direction * self.STEP_SIZE
            x = self.root.winfo_x() + step
            y = self.screen_h - self.container_height

            if x <= 0:
                x, self.direction = 0, 1
                self.set_sprite()
            elif x >= self.screen_w - self.pet_width:
                x, self.direction = self.screen_w - self.pet_width, -1
                self.set_sprite()

            self.root.geometry(f"+{x}+{y}")
        self.root.after(self.ANIMATION_INTERVAL, self.animate)

    def schedule_behavior(self):
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
            self.root.after(2000, self.sit)
        else:
            print("Not enough energy to perform trick.")

    def backflip(self, angle=0):
        if angle <= 180:
            rotated_image = self.image_right.rotate(angle)
            self.img = ImageTk.PhotoImage(rotated_image)
            self.label.config(image=self.img)
            self.label.image = self.img
            self.root.after(50, lambda: self.backflip(angle + 30))
        else:
            self.set_sprite()

    def rename(self):
        self.name_label.pack_forget()
        self.name_entry = tk.Entry(
            self.container,
            font=("Arial", 14),
            fg="green",
            bg="white",
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
            self.save_state()
        self.name_entry.pack_forget()
        self.name_label.pack(side="top", anchor="n", fill="x")

    def on_close(self):
        self.save_state()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    DeskPet(root)
    root.mainloop()
