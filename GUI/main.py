import tkinter as tk
from Login_Page import login_page

# Main function to start the app
def main():
    window = tk.Tk()
    window.geometry("1200x800")
    login_page(window)  # Start with login page
    window.mainloop()

# Run the app
if __name__ == "__main__":
    main()
