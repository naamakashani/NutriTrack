import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  # For handling the logo image
from login_windows import sign_in, log_in
import shared
from fun_names import connect_to_db

# Function to handle log-in
# def log_in():
#     messagebox.showinfo("Log In", "Log-In functionality is under development.")

# Opening window
def open_app():
    shared.root = tk.Tk()
    shared.root.title("Nutrition Tracker")
    shared.root.geometry("550x550")
    shared.root.configure(bg="#d6eefc")

    # Load and display the logo image
    logo_image = Image.open(r'C:\Users\kashann\PycharmProjects\NutriTrack\image.png')  # Replace with the uploaded logo file path
    # target size
    target_width = 200
    # Calculate proportional height based on original dimensions
    width, height = logo_image.size
    aspect_ratio = height / width
    new_height = int(target_width * aspect_ratio)

    # Resize the image while keeping proportions
    logo_image = logo_image.resize((target_width, new_height), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(shared.root, image=logo_photo, bg="#d6eefc")
    logo_label.image = logo_photo
    logo_label.pack(pady=5)

    # tk.Label(root, text="Nutrition Tracker", font=("Helvetica", 20), bg="#d6eefc").pack(pady=5)

    button_style = ttk.Style()
    button_style.configure("TButton", font=("Helvetica", 10), padding=10)

    ttk.Button(shared.root, text="Sign In", command=sign_in, width=15).pack(pady=5)

    # Add the button
    ttk.Button(shared.root, text="Log In", command=log_in, width=15).pack(pady=5)

    # ttk.Button(root, text="Enter Main Menu", command=lambda: [root.destroy(), open_main_menu()], width=15).pack(pady=5)
    shared.root.mainloop()

# Run the application
connect_to_db()
open_app()

