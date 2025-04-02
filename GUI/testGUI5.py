import tkinter as tk
from tkinter import font, messagebox
from PIL import Image, ImageTk, ImageEnhance
import pygame
import subprocess
import webbrowser

# Initialize the sound system
def init_sound_system():
    pygame.mixer.init()
    pygame.mixer.music.load("GUI/music.mp3")  # Background music
    pygame.mixer.music.play(loops=-1)  # Loop the background music

# Play click sound
def play_click_sound():
    click_sound = pygame.mixer.Sound("GUI/click.mp3")  # Replace with your click sound file
    click_sound.play()

# Functions for each task
def take_attendance():
    play_click_sound()
    try:
        subprocess.run(["python", "face_recognition/main.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")
    else:
        messagebox.showinfo("Task", "Attendance Taking Started!")
    
    

def detect_mobile_phone():
    play_click_sound()
    try:
        subprocess.run(["python", "People-Count-using-YOLOv8/Mobile.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")
    else:
        messagebox.showinfo("Task", "Mobile Phone Detection Executed Successfully!")

def control_motor():
    play_click_sound()
    try:
        subprocess.run(["python", "People-Count-using-YOLOv8/fist_open_close2.py"], check=True)
        messagebox.showinfo("Motor Control", "Motor Control Started!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred while running the motor control script:\n{e}")

def control_fan():
    play_click_sound()
    try:
        subprocess.run(["python", "People-Count-using-YOLOv8/palm_distance.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")
    else:
        messagebox.showinfo("Task", "Fan Control Started!")

def total_students():
    play_click_sound()
    try:
        # Run the script to count students
        result = subprocess.check_output(
            ["python", "People-Count-using-YOLOv8/total_student.py"], text=True
        )
        student_count = result.strip()  # Assume script returns the count as output
        messagebox.showinfo("Total Students", f"Total Students Detected: {student_count}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

def present_students():
    play_click_sound()
    messagebox.showinfo("Present Students", "Present Students: 45")  # Replace with dynamic calculation if needed

def blynk():
    play_click_sound()
    try:
        subprocess.run(["python", "C:\\path_to_blynk_script\\blynk_control.py"], check=True)  # Replace with your Blynk script path
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred while running the Blynk script:\n{e}")
    else:
        messagebox.showinfo("Blynk", "Blynk Control Script Executed!")

# Sidebar toggle
def toggle_sidebar():
    play_click_sound()
    if sidebar_frame.winfo_ismapped():
        sidebar_frame.place_forget()
    else:
        sidebar_frame.place(x=0, y=0, relheight=1)

# Exit window on pressing 'Q'
def exit_window(event):
    root.quit()
    pygame.mixer.music.stop()

def blink_exit_message():
    current_color = exit_message.cget("fg")
    next_color = "red" if current_color == "white" else "white"
    exit_message.config(fg=next_color)
    root.after(500, blink_exit_message)

def blink_toggle_button():
    current_color = toggle_button.cget("bg")
    next_color = "#FF4500" if current_color == "#555555" else "#555555"
    toggle_button.config(bg=next_color)
    root.after(500, blink_toggle_button)

# Main window setup
root = tk.Tk()
root.title("Responsive Control Panel")
root.geometry("800x600")
root.state("zoomed")  # Open in full-screen

# Background image
bg_image = Image.open("GUI/sciFiBackround.png")
enhancer = ImageEnhance.Brightness(bg_image)
bg_image = enhancer.enhance(1.5)

canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

def resize_bg(event):
    global bg_photo
    resized_bg = bg_image.resize((event.width, event.height), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(resized_bg)
    canvas.create_image(0, 0, anchor="nw", image=bg_photo)

root.bind("<Configure>", resize_bg)

# Sidebar frame
sidebar_frame = tk.Frame(root, bg="#333333", width=250)

title_label = tk.Label(
    sidebar_frame, text="FEATURE", font=("Helvetica", 18, "bold underline"), fg="white", bg="#333333"
)
title_label.pack(pady=20)

buttons = [
    ("Take Attendance", take_attendance, "#4CAF50"),
    ("Detect Mobile Phone", detect_mobile_phone, "#FF5722"),
    ("Control Motor", control_motor, "#2196F3"),
    ("Control Fan", control_fan, "#FFC107"),
    ("Total Students", total_students, "#8E44AD"),
    ("Present Students", present_students, "#16A085"),
    ("Blynk", blynk, "#E67E22"),
]

for text, command, color in buttons:
    button = tk.Button(
        sidebar_frame,
        text=text,
        command=command,
        font=("Helvetica", 16, "bold"),
        bg=color,
        fg="white",
        relief="flat",
        bd=3,
        height=2,
        width=20,
    )
    button.pack(pady=10, padx=70)

toggle_button = tk.Button(
    root, text="☰", command=toggle_sidebar, font=("Helvetica", 18), bg="#555555", fg="white", relief="flat", bd=3, height=2, width=3
)
toggle_button.place(x=10, y=10)

exit_message = tk.Label(root, text="Press 'Q' to exit the window", font=("Helvetica", 14), fg="red", bg="white")
exit_message.place(relx=0.99, rely=0.95, anchor="se")

root.bind("q", exit_window)

init_sound_system()

# Start blinking effects
blink_exit_message()
blink_toggle_button()

root.mainloop()
