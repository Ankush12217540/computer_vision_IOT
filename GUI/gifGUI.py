import tkinter as tk
from tkinter import font, messagebox
from PIL import Image, ImageTk
import pygame

# Initialize the sound system
def init_sound_system():
    pygame.mixer.init()
    pygame.mixer.music.load("GUI/music.mp3")  # Background music
    pygame.mixer.music.play(loops=-1)  # Loop the background music

# Play click sound
def play_click_sound():
    click_sound = pygame.mixer.Sound("GUI/click.mp3")  # Replace with your click sound file
    click_sound.play()

# Functions corresponding to each button's task
def take_attendance():
    play_click_sound()
    print("Taking Attendance...")
    messagebox.showinfo("Task", "Attendance Taking Started!")

def detect_mobile_phone():
    play_click_sound()
    print("Detecting Mobile Phone...")
    messagebox.showinfo("Task", "Mobile Phone Detection Started!")

def control_motor():
    play_click_sound()
    print("Controlling Motor...")
    messagebox.showinfo("Task", "Motor Control Started!")

def control_fan():
    play_click_sound()
    print("Controlling Fan by Student Presence...")
    messagebox.showinfo("Task", "Fan Control Started!")

# Set up the main window
root = tk.Tk()
root.title("GIF Background Control Panel")
root.geometry("800x600")

# Load the GIF and extract all frames
gif_path = "GUI/gif5.gif"  # Replace with your GIF file path
gif_image = Image.open(gif_path)

# Extract frames from the GIF
frames = []
try:
    while True:
        frame = gif_image.copy()
        frames.append(frame)  # Store the frames
        gif_image.seek(gif_image.tell() + 1)  # Move to the next frame
except EOFError:
    pass  # End of GIF reached

# Function to resize the frames and display GIF frames
def animate_gif():
    global frames
    window_width = root.winfo_width()  # Get the current window width
    window_height = root.winfo_height()  # Get the current window height
    
    resized_frames = []
    for frame in frames:
        # Resize each frame to fill the entire window (full-screen)
        resized_frame = frame.resize((window_width, window_height), Image.ANTIALIAS)
        resized_frames.append(ImageTk.PhotoImage(resized_frame))
    
    # Create an iterator for cycling through the resized frames
    frame_iter = iter(resized_frames)
    
    # Create the animation by cycling through the frames
    def update_frame():
        current_frame = next(frame_iter)  # Get the next frame
        canvas.create_image(0, 0, anchor="nw", image=current_frame)  # Display the frame
        canvas.image = current_frame  # Keep a reference to avoid garbage collection
        root.after(100, update_frame)  # Update every 100ms (adjust for desired speed)
    
    update_frame()

# Create a Canvas for the GIF background and UI elements
canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

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

# Start the GIF animation
animate_gif()

# Initialize sound system and start background music
init_sound_system()

# Start the Tkinter event loop
root.mainloop()
