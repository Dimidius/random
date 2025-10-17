import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
import random, os, sys, winsound, time
import json
import pywinstyles
from winotify import Notification, audio
from modules import new_tricks as tr
from modules import snake

# Let's make a button on the menu that opens a trick learning window where you can teach your pet tricks
# Let's also make a button next to that which opens a trick performing window where you can make your pet perform tricks it has learned
# Performing tricks costs energy, and learning tricks costs hunger
# If the pet is too hungry or too low on energy, it can't learn or perform tricks
# Add mini games to earn money to buy food and snacks for your pet
# Add a money system to buy food and snacks for your pet (Money is dabloons >:))
# Mini games: Chrome Dino Game, Tetris, Space Invaders, Snake, Atari Breakout



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

    pet_hungry = Notification(
        app_id="DeskPet",
        title="Your pet is hungry!",
        msg="Feed your pet to keep it happy and healthy.")

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
        self.menu_win.geometry("600x400")
        self.menu_win.config(bg="#40414a")
        pywinstyles.change_header_color(self.menu_win, "#2c2d33")

        status_frame = tk.Frame(self.menu_win, bg="#40414a")
        status_frame.pack(pady=(20, 10))

        bars_frame = tk.Frame(status_frame, bg="#40414a")
        bars_frame.grid(row=0, column=0, padx=10)

        tk.Label(bars_frame, text="Hunger", bg="#40414a", fg="white", font=("Arial", 12)).pack(pady=(0, 2))
        self.hunger_bar = ttk.Progressbar(bars_frame, length=150, maximum=100)
        self.hunger_bar.pack(pady=2)
        self.hunger_bar["value"] = self.hunger

        tk.Label(bars_frame, text="Energy", bg="#40414a", fg="white", font=("Arial", 12)).pack(pady=(10, 2))
        self.energy_bar = ttk.Progressbar(bars_frame, length=150, maximum=100)
        self.energy_bar.pack(pady=2)
        self.energy_bar["value"] = self.energy

        learn_frame = tk.Frame(status_frame, bg="#40414a")
        learn_frame.grid(row=0, column=1, padx=10)

        tk.Label(learn_frame, text="Learn New Tricks", bg="#40414a", fg="white", font=("Arial", 12)).pack()
        self.learn_button = tk.Button(
            learn_frame,
            text="Learn Tricks",
            command=self.open_tricks_window,
            width=15,
            background="#666773",
            fg="white"
        )
        self.learn_button.pack(pady=(10, 0))
        
        tk.Label(learn_frame, text="Perform Learned Tricks", bg="#40414a", fg="white", font=("Arial", 12)).pack(pady=(5, 0))
        self.tricks_btn = tk.Button(
            learn_frame,
            text="Tricks",
            state="disabled",
            width=15,
            background="#666773",
            fg="white"
        )
        self.tricks_btn.pack(pady=(10, 0))

        # --- Food and Snack Buttons Section ---
        food_snack_frame = tk.Frame(self.menu_win, bg="#40414a")
        food_snack_frame.pack(pady=20)

        # Left: Food buttons
        food_frame = tk.LabelFrame(food_snack_frame, text="Foods", fg="white", bg="#40414a", font=("Arial", 12, "bold"))
        food_frame.grid(row=0, column=0, padx=20)

        food_buttons = [
            ("Apple (+5 Hunger)", lambda: self.feed_food("Apple")),
            ("Sandwich (+15 Hunger)", lambda: self.feed_food("Sandwich")),
            ("Pizza (+25 Hunger)", lambda: self.feed_food("Pizza"))
        ]

        for i, (text, cmd) in enumerate(food_buttons):
            tk.Button(food_frame, text=text, command=cmd, width=20, background="#666773", fg="white").pack(pady=5)


        # Right: Snack buttons
        snack_frame = tk.LabelFrame(food_snack_frame, text="Snacks", fg="white", bg="#40414a", font=("Arial", 12, "bold"))
        snack_frame.grid(row=0, column=1, padx=20)

        snack_buttons = [
            ("Giffies (+2H, +5E)", lambda: self.feed_snack("Giffies")),
            ("Choc. Pretzels (+5H, +10E)", lambda: self.feed_snack("Chocolate Preztels")),
            ("Dick (+20 Energy)", lambda: self.feed_snack("Dick"))
        ]

        for i, (text, cmd) in enumerate(snack_buttons):
            tk.Button(snack_frame, text=text, command=cmd, width=20, background="#666773", fg="white").pack(pady=5)

    def open_tricks_window(self):
        # Create one instance of TrickApp if it doesn't exist
        if not hasattr(self, "tricks_app"):
            self.tricks_app = tr.TrickApp(self.root)
        self.tricks_app.tricks_menu()

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
        offset_from_bottom = 0 # lift above taskbar, or positive to move lower 
        self.root.geometry(f"+{screen_w // 2}+{screen_h - self.container_height + offset_from_bottom}")


        # States
        self.walking = False
        self.sitting = False
        self.sleeping = False
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
        # self.root.bind("<Control-t>", lambda event: self.trick())
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

    def sleep(self):
        """Put the pet to sleep when energy is low."""
        if not self.sleeping and self.energy < 10:
            self.sleeping = True
            self.walking = False
            self.sitting = False
            self.direction = 0
            self.set_sprite()

            msg = tk.Label(self.container, text="💤 Sleeping...", fg="blue", bg="white")
            msg.pack()
            self.root.after(10000, msg.destroy)

            self._regain_energy()
            print(f"Entering sleep mode at energy={self.energy}")

    def _regain_energy(self):
        """Regain energy slowly while sleeping."""
        if not self.sleeping:
            return
        if self.energy < 100:
            self.energy += 2
            self.update_menu_bars()
            self.root.after(1000, self._regain_energy)
            print(f"Regaining energy... {self.energy}")
        else:
            self.wake_up()

    def wake_up(self):
        """Wake up when energy is full."""
        self.sleeping = False
        self.walking = True
        msg = tk.Label(self.container, text="☀️ I'm awake!", fg="green", bg="white")
        msg.pack()
        self.root.after(1500, msg.destroy)
        self.schedule_behavior()

    def decrease_hunger(self):
        if self.hunger > 0:
            self.hunger -= 1
            self.root.after(120000, self.decrease_hunger)
        else:
            if self.hunger <= 30:
                self.hungry = True
                self.pet_hungry.show()

    def decrease_energy(self):
        if self.sleeping:
            return  # don't drain energy while sleeping

        if self.energy > 0:
            self.energy -= 1
            self.update_menu_bars()
            self.root.after(100000, self.decrease_energy)
        else:
            self.energy = 0

        # NEW: If energy is critically low, start sleeping
        if self.energy <= 10 and not self.sleeping:
            self.sleep()

    def animate(self):
        if self.sleeping:
            self.root.after(self.ANIMATION_INTERVAL, self.animate)
            return

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
        if self.sleeping:
            return
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

    # def trick(self):
    #     if self.sleeping:
    #         return
    #     if self.energy >= 40:
    #         self.energy -= 20
    #         self.sitting = True
    #         self.walking = False
    #         self.backflip()
    #         self.root.after(2000, self.sit)
    #     else:
    #         print("Not enough energy to perform trick.")

    # def backflip(self, angle=0):
    #     if angle <= 180:
    #         rotated_image = self.image_right.rotate(angle)
    #         self.img = ImageTk.PhotoImage(rotated_image)
    #         self.label.config(image=self.img)
    #         self.label.image = self.img
    #         self.root.after(50, lambda: self.backflip(angle + 30))
    #     else:
    #         self.set_sprite()

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
