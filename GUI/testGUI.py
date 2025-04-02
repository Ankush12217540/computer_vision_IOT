import tkinter as tk
from tkinter import font
import random
from tkinter import messagebox
# Functions corresponding to each button's task
def take_attendance():
    print("Taking Attendance...")  # Your actual function call here
    messagebox.showinfo("Task", "Attendance Taking Started!")

def detect_mobile_phone():
    print("Detecting Mobile Phone...")  # Your actual function call here
    messagebox.showinfo("Task", "Mobile Phone Detection Started!")

def control_motor():
    print("Controlling Motor...")  # Your actual function call here
    messagebox.showinfo("Task", "Motor Control Started!")

def control_fan():
    print("Controlling Fan by Student Presence...")  # Your actual function call here
    messagebox.showinfo("Task", "Fan Control Started!")

# Set up the main window
root = tk.Tk()
root.title("Sci-Fi Control Panel")
root.geometry("800x600")  # Initial window size

# Custom Fonts
font_style = tk.font.Font(family="Helvetica", size=16, weight="bold")

# Create a Canvas for the dynamic background animation
canvas = tk.Canvas(root, width=800, height=600, bg='black')
canvas.pack(fill="both", expand=True)

# Create moving lines for a sci-fi look
def draw_moving_lines():
    canvas.delete("lines")  # Clear previous lines
    for _ in range(5):  # Create multiple moving lines
        x1 = random.randint(0, 800)
        y1 = random.randint(0, 600)
        x2 = random.randint(0, 800)
        y2 = random.randint(0, 600)
        
        canvas.create_line(x1, y1, x2, y2, fill=random.choice(['cyan', 'magenta', 'lime', 'blue']),
                            width=2, tags="lines")

# Create a color changing effect on the background
def change_background_color():
    colors = ['#1b1b1b', '#202020', '#1a1a1a', '#333333']
    canvas.config(bg=random.choice(colors))
    root.after(500, change_background_color)  # Change color every 500ms

# Sci-Fi glow effect for buttons
def on_enter(e):
    e.config(bg="#66ccff")  # Light blue color on hover
    e.config(fg="black")
    e.config(relief="raised")

def on_leave(e):
    e.config(bg="#333333")  # Dark background when not hovered
    e.config(fg="white")
    e.config(relief="flat")

# Create Buttons with Subtle Hover Effects
attendance_button = tk.Button(root, text="Take Attendance", command=take_attendance, font=font_style,
                              bg="#333333", fg="white", relief="flat", bd=3, height=2, width=30)
attendance_button.place(relx=0.5, rely=0.1, anchor="center")

mobile_button = tk.Button(root, text="Detect Mobile Phone", command=detect_mobile_phone, font=font_style,
                          bg="#333333", fg="white", relief="flat", bd=3, height=2, width=30)
mobile_button.place(relx=0.5, rely=0.25, anchor="center")

motor_button = tk.Button(root, text="Control Motor", command=control_motor, font=font_style,
                         bg="#333333", fg="white", relief="flat", bd=3, height=2, width=30)
motor_button.place(relx=0.5, rely=0.4, anchor="center")

fan_button = tk.Button(root, text="Control Fan by Student Presence", command=control_fan, font=font_style,
                       bg="#333333", fg="white", relief="flat", bd=3, height=2, width=30)
fan_button.place(relx=0.5, rely=0.55, anchor="center")

# Bind hover effects to buttons
attendance_button.bind("<Enter>", lambda e: on_enter(attendance_button))
attendance_button.bind("<Leave>", lambda e: on_leave(attendance_button))

mobile_button.bind("<Enter>", lambda e: on_enter(mobile_button))
mobile_button.bind("<Leave>", lambda e: on_leave(mobile_button))

motor_button.bind("<Enter>", lambda e: on_enter(motor_button))
motor_button.bind("<Leave>", lambda e: on_leave(motor_button))

fan_button.bind("<Enter>", lambda e: on_enter(fan_button))
fan_button.bind("<Leave>", lambda e: on_leave(fan_button))

# Start the animation and background color change
def animate():
    draw_moving_lines()  # Draw moving lines
    change_background_color()  # Change background color
    root.after(100, animate)  # Call animate again after 100ms

# Start the animation loop
animate()

# Start the Tkinter event loop
root.mainloop()
