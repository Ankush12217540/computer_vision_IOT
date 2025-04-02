import tkinter as tk
from tkinter import font, messagebox
from PIL import Image, ImageTk, ImageEnhance
import pygame
import subprocess  # To run external scripts

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
    try:
        # Run the computer vision script
        subprocess.run(["python", "C:\\5th Semester\\computer_vision\\People-Count-using-YOLOv8\\test1.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred while running the script:\n{e}")
    else:
        messagebox.showinfo("Task", "Mobile Phone Detection Script Executed!")

def control_motor():
    play_click_sound()
    print("Controlling Motor...")
    messagebox.showinfo("Task", "Motor Control Started!")

def control_fan():
    play_click_sound()
    print("Controlling Fan by Student Presence...")
    messagebox.showinfo("Task", "Fan Control Started!")

# Function to display the About Project window
def show_about_project():
    play_click_sound()
    about_window = tk.Toplevel(root)  # Create a new top-level window
    about_window.title("About the Project")
    about_window.geometry("600x400")

    # Add sample data about the project in this new window
    project_info = """This project is a responsive control panel 
designed for managing various tasks such as:
- Attendance Taking
- Mobile Phone Detection
- Motor Control
- Fan Control by Student Presence

It utilizes Tkinter for the UI, pygame for sound handling, and PIL for image processing."""
    
    label = tk.Label(about_window, text=project_info, font=("Helvetica", 14), padx=20, pady=20, justify="left")
    label.pack()

    # Back to Home button
    back_button = tk.Button(about_window, text="Back to Home", command=about_window.destroy, font=("Helvetica", 14), 
                            bg="#333333", fg="white", relief="flat", bd=3, height=2, width=20)
    back_button.pack(pady=20)

# Exit window on pressing 'Q'
def exit_window(event):
    root.quit()
    pygame.mixer.music.stop()

# Set up the main window
root = tk.Tk()
root.title("Responsive Control Panel")
root.geometry("800x600")

# Load and enhance the background image (brighter background)
bg_image = Image.open("GUI/sciFiBackround.png")  # Replace with your image path
enhancer = ImageEnhance.Brightness(bg_image)
bg_image = enhancer.enhance(1.5)  # Increase brightness

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
buttons = [
    ("Take Attendance", take_attendance, "#4CAF50", 0.1),
    ("Detect Mobile Phone", detect_mobile_phone, "#FF5722", 0.2),
    ("Control Motor", control_motor, "#2196F3", 0.3),
    ("Control Fan by Student Presence", control_fan, "#FFC107", 0.4),
]

# Add buttons to the canvas (aligning them to the left side of the window)
for text, command, color, rely in buttons:
    button = tk.Button(root, text=text, command=command, font=font_style,
                       bg=color, fg="white", relief="flat", bd=3, height=2, width=25)
    button.place(relx=0.1, rely=rely, anchor="w")  # Align to the left side

# Add the About Project button on the right side of the window
about_button = tk.Button(root, text="About the Project", command=show_about_project, font=font_style,
                         bg="#607D8B", fg="white", relief="flat", bd=3, height=2, width=20)
about_button.place(relx=0.9, rely=0.5, anchor="e")  # Place on the right side

# Add message in the lower-left corner
exit_message = tk.Label(root, text="Press 'Q' to exit the window", font=("Helvetica", 14), fg="red", bg="white")
exit_message.place(relx=0.01, rely=0.95, anchor="sw")

# Bind 'Q' key to quit the application
root.bind("q", exit_window)

# Maximize the window
root.state("zoomed")

# Initialize sound system and start background music
init_sound_system()

# Start the Tkinter event loop
root.mainloop()
