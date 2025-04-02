import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import pygame  # Import pygame for audio playback
import subprocess  # To execute the second script

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Function to play background music
def play_background_music():
    pygame.mixer.music.load("GUI/music3.mp3")  # Load the music file
    pygame.mixer.music.play(-1, 0.0)  # Play music in a loop (-1 means infinite loop)

# Function to stop background music
def stop_background_music():
    pygame.mixer.music.stop()

# Function to play click sound
def play_click_sound():
    click_sound = pygame.mixer.Sound("GUI/click.mp3")  # Load the click sound
    click_sound.play()  # Play the click sound once

# Redirect to second page
def redirect_to_tab():
    play_click_sound()  # Play click sound when redirecting
    login_frame.place_forget()  # Hide the login form
    tab_frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Show the second tab/page

# Back to login
def back_to_login():
    play_click_sound()  # Play click sound when going back to login
    tab_frame.place_forget()  # Hide the second page
    login_frame.place(relx=0.001, rely=0.2, relwidth=0.2, relheight=0.5)  # Show the login form

# Skip login and go directly to second page (testGUI3.py)
def skip_login():
    play_click_sound()  # Play click sound when skipping
    stop_background_music()  # Stop the background music
    login_frame.place_forget()  # Hide the login form
    # Run the second script (testGUI3.py) in the background
    subprocess.Popen(["python", "GUI/testGUI5.py"])

# Login action
def login_action():
    play_click_sound()  # Play click sound when login is attempted
    username = username_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "password":
        stop_background_music()  # Stop the background music
        # login_frame.place_forget()  # Hide the login form
        # Run the second script (testGUI3.py)
        subprocess.Popen(["python", "GUI/testGUI5.py"])
        root.quit()  # Close the current GUI
    else:
        print("Login Failed")  # Log failure


# Function to add rounded corners to the image
def add_rounded_corners(image_path, radius=30):
    img = Image.open(image_path)
    img = img.convert("RGBA")  # Ensure image is in RGBA mode

    # Create a mask for rounded corners
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), img.size], radius, fill=255)

    # Apply the mask to the image
    img.putalpha(mask)
    return img

# Create main window
root = tk.Tk()
root.title("Advanced Computer Vision Project")
root.geometry("1200x800")  # Set initial window size
root.resizable(True, True)

# Load the background image
bg_image = Image.open("GUI/sciFiBackround2.jpg")
bg_photo = ImageTk.PhotoImage(bg_image)

# Set the background
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Fill entire screen

# Load the logo with rounded corners
logo_image = add_rounded_corners("GUI/lpuLogo.jpg", radius=50)  # Ensure your logo has transparency (PNG)
logo_photo = ImageTk.PhotoImage(logo_image)

# Create the logo label and position it in the top-right corner
logo_label = tk.Label(root, image=logo_photo, bg="white")
logo_label.place(x=root.winfo_width() - logo_image.width - 20, y=20)

# Update the position of the logo after the window is resized
def update_logo_position(event):
    logo_label.place(x=root.winfo_width() - logo_image.width - 14, y=20)

root.bind("<Configure>", update_logo_position)

# Login Frame
login_frame = tk.Frame(root, bg="#ffffff", bd=3, relief="ridge")
login_frame.place(relx=0.001, rely=0.2, relwidth=0.2, relheight=0.5)

# Login Form Elements
login_title = tk.Label(login_frame, text="Login", font=("Helvetica", 20, "bold"), bg="white", fg="#4a90e2")
login_title.pack(pady=15)

username_label = tk.Label(login_frame, text="Username:", font=("Helvetica", 12), bg="white")
username_label.pack(pady=10)
username_entry = tk.Entry(login_frame, font=("Helvetica", 12), bd=2, relief="solid")
username_entry.pack(pady=5, ipadx=10, fill="x", padx=20)

password_label = tk.Label(login_frame, text="Password:", font=("Helvetica", 12), bg="white")
password_label.pack(pady=10)
password_entry = tk.Entry(login_frame, font=("Helvetica", 12), bd=2, relief="solid", show="*")
password_entry.pack(pady=5, ipadx=10, fill="x", padx=20)

login_button = tk.Button(
    login_frame, text="Login", font=("Helvetica", 14, "bold"), bg="#4a90e2", fg="white",
    activebackground="#3a78c3", activeforeground="white", bd=0, cursor="hand2", command=login_action
)
login_button.pack(pady=20, ipadx=10, ipady=5)

# Add a Skip Login Button to jump directly to the second page (testGUI3.py)
skip_button = tk.Button(
    login_frame, text="Skip Login", font=("Helvetica", 14, "bold"), bg="#e94e77", fg="white",
    activebackground="#d93f67", activeforeground="white", bd=0, cursor="hand2", command=skip_login
)
skip_button.pack(pady=20, ipadx=10, ipady=5)

# Message just below the form
exit_message = tk.Label(root, text="Press 'Q' to exit the window", font=("Helvetica", 18, "bold"), fg="black", bg="red")
exit_message.place(relx=0.85, rely=0.91, anchor="center")

# Blink function to make the message blink
def blink_label():
    current_color = exit_message.cget("fg")
    # Toggle between black and red
    new_color = "red" if current_color == "black" else "black"
    exit_message.config(fg=new_color)
    root.after(500, blink_label)  # Repeat the blinking every 500ms

# Bind the Q key to close the window
def exit_window(event):
    root.quit()

root.bind("q", exit_window)

# Tab Frame (Second Page)
tab_frame = tk.Frame(root, bg="#1a1a1a")

# Tab Content
tab_label = tk.Label(tab_frame, text="Welcome to the Project Dashboard!", font=("Helvetica", 20, "bold"), bg="#1a1a1a", fg="white")
tab_label.pack(pady=20)

back_button = tk.Button(
    tab_frame, text="Back to Login", font=("Helvetica", 14), bg="#4a90e2", fg="white",
    activebackground="#3a78c3", activeforeground="white", bd=0, cursor="hand2", command=back_to_login
)
back_button.pack(pady=20, ipadx=10, ipady=5)

# Start playing the music when the application runs
play_background_music()

# Start the blinking effect for the exit message
blink_label()

# Run the application
root.mainloop()
