import tkinter as tk
from tkinter import messagebox
import os

# File path where the user credentials are stored
USER_FILE = "users.txt"

# Function to read users from the file
def read_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as file:
        users = {}
        for line in file.readlines():
            username, password = line.strip().split(",")
            users[username] = password
        return users

# Function to save a new user to the file
def save_user(username, password):
    with open(USER_FILE, "a") as file:
        file.write(f"{username},{password}\n")

# Function to handle user registration (signup)
def signup_action(username_entry, password_entry, confirm_password_entry):
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    
    if password == confirm_password:
        # Check if username already exists
        users = read_users()
        if username in users:
            messagebox.showerror("Signup Failed", "Username already exists. Please choose another one.")
        else:
            # Save the new user and show confirmation message
            save_user(username, password)
            messagebox.showinfo("Signup Successful", f"Welcome {username}, your account has been created successfully!")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            confirm_password_entry.delete(0, tk.END)
    else:
        # Show error message if passwords don't match
        messagebox.showerror("Signup Failed", "Passwords do not match. Please try again.")
