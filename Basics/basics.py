import tkinter as tk
import winsound

hunger = 5

def countdown_hunger():
    global hunger
    if hunger > 0:
        hunger -= 1
        print(f"Hunger level: {hunger}")
        root.after(1000, countdown_hunger)  # call again in 1 second
    else:
        pet_hungry = tk.Message(root, text="Your pet is hungry!")
        pet_hungry.config(bg='red')
        pet_hungry.pack()
        print("Hunger has reached zero!")
        winsound.PlaySound("Basics\\fart-with-reverb.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

root = tk.Tk()
countdown_hunger()
root.mainloop()
