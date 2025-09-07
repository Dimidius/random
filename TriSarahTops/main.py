import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import random
import winsound


class TriSarahTopsApp:
    """A simple desktop pet that walks, sits, and can be dragged around."""

    # Constants
    STEP_SIZE = 2
    ANIMATION_INTERVAL = 50  # ms
    BEHAVIOR_MIN_MS = 1000
    BEHAVIOR_MAX_MS = 4000

    def __init__(self, root: tk.Tk):
        self.root = root
        self._configure_window()

        # Load sprites
        self.image_right = Image.open("TriSarahTops/TriSarahTopsL.png")
        self.image_left = ImageOps.mirror(self.image_right)

        self.pet_width, self.pet_height = self.image_right.size
        self.img = ImageTk.PhotoImage(self.image_right)

        # --- Container (bigger than sprite so label can fit) ---
        self.container_height = self.pet_height + 40  # 40px extra space for hunger label
        self.container_width = self.pet_width + 40
        self.container = tk.Frame(root, bg="white", width=self.container_width, height=self.container_height)
        self.container.pack_propagate(False)  # don’t shrink to contents
        self.container.pack()

        # Hunger label (goes in the extra space above pet)
        self.hunger_label = tk.Label(
            self.container,
            text=f"Hunger: 3",
            font=("Arial", 14),
            fg="green",
            bg="black"
        )
        self.hunger_label.pack(side="top", anchor="n")

        # Sprite image inside container (sticks to bottom)
        self.label = tk.Label(
            self.container,
            image=self.img,
            bg="white",
            height=self.pet_height,
            width=self.pet_width
        )
        self.label.pack(side="bottom")

        # Place at bottom center
        screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
        self.screen_w, self.screen_h = screen_w, screen_h
        self.root.geometry(f"+{screen_w // 2}+{screen_h - self.container_height}")

        # State
        self.walking = False
        self.sitting = False
        self.direction = 0  # -1 = left, 0 = idle, 1 = right
        self.hungry = False
        self.hunger = 10  # initial hunger level

        # Bind events
        self._bind_events()

        # Start loops
        self.animate()
        self.schedule_behavior()
        self.decrease_hunger()

    # --- Window setup ---------------------------------------------------------

    def _configure_window(self):
        """Set up transparent, undecorated always-on-top window."""
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "white")

    def _bind_events(self):
        """Attach mouse and keyboard interactions."""
        self.label.bind("<ButtonPress-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.do_drag)
        self.label.bind("<ButtonRelease-1>", self.end_drag)

        self.label.bind("<Control-Button-1>", self.toggle_sit)
        self.label.bind("<Button-3>", lambda e: self.root.destroy())

    # --- Image handling -------------------------------------------------------

    def set_sprite(self):
        """Update sprite based on current direction/state."""
        if self.direction > 0:
            image = self.image_right
        elif self.direction < 0:
            image = self.image_left
        else:
            image = self.image_right  # default idle

        self.img = ImageTk.PhotoImage(image)
        self.label.configure(image=self.img)
        self.label.image = self.img  # prevent GC

    # --- Dragging -------------------------------------------------------------

    def start_drag(self, event):
        self.walking = False
        self.x, self.y = event.x, event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + event.x - self.x
        y = self.screen_h - self.container_height  # stick to bottom with full container
        self.root.geometry(f"+{x}+{y}")

    def end_drag(self, event):
        if not self.sitting:
            self.walking = True

    # --- States ---------------------------------------------------------------

    def toggle_sit(self, event=None):
        """Toggle between sitting and normal behavior."""
        self.sitting = not self.sitting
        if self.sitting:
            self.walking = False
            self.direction = 0
        else:
            self.schedule_behavior()

    # --- Hunger system --------------------------------------------------------

    def update_hunger_label(self):
        self.hunger_label.config(text=f"Hunger: {self.hunger}")

    def decrease_hunger(self):
        if self.hunger > 0:
            self.hunger -= 1
            self.update_hunger_label()
            self.root.after(1000, self.decrease_hunger)  # test: every 1 sec
        else:
            if not self.hungry:  # only trigger once
                self.hungry = True
                self.update_hunger_label()
                self.hide_timer()
                pet_hungry = tk.Message(self.container, text="Your pet is hungry!", bg="red")
                pet_hungry.pack()
                winsound.PlaySound("TriSarahTops/fart-with-reverb.wav",
                                   winsound.SND_FILENAME | winsound.SND_ASYNC)
                
    def hide_timer(self):
        self.hunger_label.pack_forget()

    # --- Animation ------------------------------------------------------------

    def animate(self):
        """Move pet smoothly when walking."""
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

    # --- Behavior -------------------------------------------------------------

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

if __name__ == "__main__":
    root = tk.Tk()
    TriSarahTopsApp(root)
    root.mainloop()
