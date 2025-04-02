import tkinter as tk
from tkinter import font
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance

# Functions corresponding to each button's task
def take_attendance():
    print("Taking Attendance...")
    messagebox.showinfo("Task", "Attendance Taking Started!")

def detect_mobile_phone():
    print("Detecting Mobile Phone...")
    messagebox.showinfo("Task", "Mobile Phone Detection Started!")

def control_motor():
    print("Controlling Motor...")
    messagebox.showinfo("Task", "Motor Control Started!")

def control_fan():
    print("Controlling Fan by Student Presence...")
    messagebox.showinfo("Task", "Fan Control Started!")

# Set up the main window
root = tk.Tk()
root.title("Responsive Control Panel")
root.geometry("800x600")

# Load and enhance the background image
bg_image = Image.open("GUI\image.jpg")  # Replace with your image path
enhancer = ImageEnhance.Brightness(bg_image)
bg_image = enhancer.enhance(0.5)  # Reduce brightness for better contrast

# Create a Canvas for the background and UI elements
canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Function to resize the background image dynamically
def resize_bg(event):
    global bg_photo
    resized_bg = bg_image.resize((event.width, event.height), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(resized_bg)
    canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Bind resizing to the background image
root.bind("<Configure>", resize_bg)

# Custom Fonts
font_style = tk.font.Font(family="Helvetica", size=16, weight="bold")

# Create Buttons
def on_enter(e):
    e.config(bg="#66ccff", fg="black", relief="raised")

def on_leave(e):
    e.config(bg="#333333", fg="white", relief="flat")

buttons = [
    ("Take Attendance", take_attendance, 0.2),
    ("Detect Mobile Phone", detect_mobile_phone, 0.4),
    ("Control Motor", control_motor, 0.6),
    ("Control Fan by Student Presence", control_fan, 0.8),
]

# Add buttons to the canvas
for text, command, rely in buttons:
    button = tk.Button(root, text=text, command=command, font=font_style,
                       bg="#333333", fg="white", relief="flat", bd=3, height=2, width=25)
    button.place(relx=0.5, rely=rely, anchor="center")
    button.bind("<Enter>", lambda e, btn=button: on_enter(btn))
    button.bind("<Leave>", lambda e, btn=button: on_leave(btn))

# Maximize the window
root.state("zoomed")

# Start the Tkinter event loop
root.mainloop()
