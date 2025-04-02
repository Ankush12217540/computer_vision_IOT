import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import os
import pygame

# Initialize pygame mixer for sound effects
pygame.mixer.init()

def play_click_sound():
    """Plays a click sound when a button is clicked."""
    try:
        click_sound = pygame.mixer.Sound("GUI/click.mp3")  # Update with your sound file path
        click_sound.play()
    except pygame.error:
        print("Click sound file not found!")

# Create the main window
root = tk.Tk()
root.title("Project Contributors")
root.geometry("1200x800")

# Set background image
def set_background_image(image_path):
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return None
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((1200, 800), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

set_background_image("GUI/background.jpg")  # Update with your background image path

# Contributor data
contributors = [
    {
        "name": "Student 1",
        "role": "Team Lead",
        "contribution": "Oversaw the entire project.",
        "details": "Led the team, ensured timely delivery, and coordinated all tasks.",
        "image": "GUI/contributor/ankush1.jpg"
    },
    {
        "name": "Student 2",
        "role": "Developer",
        "contribution": "Developed the core functionality.",
        "details": "Implemented project logic, including algorithms and backend systems.",
        "image": "GUI/contributor/ankush2.jpg"
    },
    {
        "name": "Student 3",
        "role": "Designer",
        "contribution": "Created the UI/UX design.",
        "details": "Designed the interface to ensure it was intuitive and visually appealing.",
        "image": "GUI/contributor/ankush3.jpg"
    },
    {
        "name": "Student 4",
        "role": "Tester",
        "contribution": "Ensured the quality of the project.",
        "details": "Rigorously tested the application for bugs and usability issues.",
        "image": "GUI/contributor/ankush4.jpg"
    }
]

# Fonts
header_font = font.Font(family="Helvetica", size=20, weight="bold")
card_font = font.Font(family="Helvetica", size=14)

# Header
header_label = tk.Label(
    root,
    text="Contributors to the Project",
    font=header_font,
    bg="#ffffff",
    fg="#333333"
)
header_label.pack(pady=20)

# Function to open detailed information window
def show_details(contributor):
    play_click_sound()
    details_window = tk.Toplevel(root)
    details_window.title(f"Details of {contributor['name']}")
    details_window.geometry("800x600")
    details_window.configure(bg="#ffffff")

    img = resize_image(contributor["image"], size=(250, 250))
    if img:
        img_label = tk.Label(details_window, image=img, bg="white")
        img_label.image = img
        img_label.pack(pady=20)

    name_label = tk.Label(details_window, text=contributor["name"], font=("Helvetica", 18, "bold"), bg="white", fg="#333333")
    name_label.pack()
    role_label = tk.Label(details_window, text=f"Role: {contributor['role']}", font=("Helvetica", 16), bg="white", fg="#666666")
    role_label.pack()
    details_label = tk.Label(details_window, text=contributor["details"], font=card_font, bg="white", fg="#444444", wraplength=600, justify="left")
    details_label.pack(pady=20)

    close_button = tk.Button(details_window, text="Close", command=lambda: [play_click_sound(), details_window.destroy()],
                              font=("Helvetica", 14), bg="#333333", fg="white", relief="flat", height=2, width=10)
    close_button.pack(pady=20)

# Function to dynamically resize images
def resize_image(image_path, size=(150, 150)):
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return None
    img = Image.open(image_path)
    img = img.resize(size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)

# Image Slider functionality
class ImageSlider(tk.Frame):
    def __init__(self, parent, images, contributors, delay=3000):
        super().__init__(parent)
        self.parent = parent
        self.images = images
        self.contributors = contributors
        self.delay = delay
        self.current_image_index = 0

        # Create a label to display the image
        self.image_label = tk.Label(self)
        self.image_label.pack(pady=20)

        # Name and role labels
        self.name_label = tk.Label(self, font=("Helvetica", 14, "bold"), bg="white", fg="#333333")
        self.name_label.pack()
        self.role_label = tk.Label(self, font=("Helvetica", 12), bg="white", fg="#666666")
        self.role_label.pack()

        # View Details button
        self.details_button = tk.Button(self, text="View Details", command=self.open_details, font=("Helvetica", 12), bg="#333333", fg="white", relief="flat", height=2, width=12)
        self.details_button.pack(pady=10)

        # Next and Previous buttons
        self.prev_button = tk.Button(self, text="Previous", command=self.show_previous_image)
        self.prev_button.pack(side="left", padx=20)

        self.next_button = tk.Button(self, text="Next", command=self.show_next_image)
        self.next_button.pack(side="right", padx=20)

        self.pack()

        # Initial display of the image
        self.display_image()

        # Auto change image after a certain delay
        self.after(self.delay, self.auto_change_image)

    def display_image(self):
        img = resize_image(self.images[self.current_image_index], size=(300, 300))
        if img:
            self.image_label.config(image=img)
            self.image_label.image = img

        # Set name and role for the current contributor
        contributor = self.contributors[self.current_image_index]
        self.name_label.config(text=contributor["name"])
        self.role_label.config(text=contributor["role"])

    def show_previous_image(self):
        self.current_image_index = (self.current_image_index - 1) % len(self.images)
        self.display_image()

    def show_next_image(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.display_image()

    def auto_change_image(self):
        self.show_next_image()
        self.after(self.delay, self.auto_change_image)

    def open_details(self):
        play_click_sound()
        show_details(self.contributors[self.current_image_index])

# Create Image Slider frame with contributors' images
image_slider = ImageSlider(root, [contributor["image"] for contributor in contributors], contributors)

# Footer
footer_label = tk.Label(
    root,
    text="Thank you for contributing to the success of this project!",
    font=("Helvetica", 14, "italic"),
    bg="#f0f0f5",
    fg="#555555"
)
footer_label.pack(pady=30)

root.mainloop()
