import tkinter as tk
from tkinter import ttk, messagebox
from fun_names import insert_user
from main_menu import open_main_menu
import shared


def sign_in():
    def submit_user_details():
        user_id = user_id_entry.get()
        user_name = user_name_entry.get()
        age = age_entry.get()
        gender = gender_var.get()
        subgroup = subgroup_var.get()
        weight = weight_entry.get()
        height = height_entry.get()
        activity_level = activity_level_var.get()

        if not (user_id and user_name and age and gender and subgroup and weight and height and activity_level):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            # Call the insert_user function
            insert_user(user_id, gender, age, subgroup, user_name, weight, height, activity_level)
            messagebox.showinfo("Success", "User details have been successfully saved!")

            # Clear all input fields
            for entry in [user_id_entry, user_name_entry, age_entry, weight_entry, height_entry]:
                entry.delete(0, tk.END)
            gender_var.set("")
            subgroup_var.set("")
            activity_level_var.set("")
            sign_in_window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please check your input and try again.")

    # Create the sign-in window
    sign_in_window = tk.Toplevel()
    sign_in_window.title("Sign In")
    sign_in_window.geometry("400x620")
    sign_in_window.configure(bg="#f7f9fc")

    # Title label
    tk.Label(sign_in_window, text="Sign In", font=("Helvetica", 16), bg="#f7f9fc").pack(pady=10)

    # User ID
    ttk.Label(sign_in_window, text="User ID:").pack(pady=5)
    user_id_entry = ttk.Entry(sign_in_window, width=30)
    user_id_entry.pack(pady=5)

    # User Name
    ttk.Label(sign_in_window, text="User Name:").pack(pady=5)
    user_name_entry = ttk.Entry(sign_in_window, width=30)
    user_name_entry.pack(pady=5)

    # Age
    ttk.Label(sign_in_window, text="Age:").pack(pady=5)
    age_entry = ttk.Entry(sign_in_window, width=30)
    age_entry.pack(pady=5)

    # Gender
    ttk.Label(sign_in_window, text="Gender:").pack(pady=5)
    gender_var = tk.StringVar()
    gender_menu = ttk.OptionMenu(sign_in_window, gender_var, "Select", "Male", "Female")
    gender_menu.pack(pady=5)

    # Subgroup
    ttk.Label(sign_in_window, text="Subgroup:").pack(pady=5)
    subgroup_var = tk.StringVar()
    subgroup_menu = ttk.OptionMenu(sign_in_window, subgroup_var, "Select", "Infants", "Children", "Adult", "Pregnancy", "Lactation")
    subgroup_menu.pack(pady=5)

    # Weight
    ttk.Label(sign_in_window, text="Weight (kg):").pack(pady=5)
    weight_entry = ttk.Entry(sign_in_window, width=30)
    weight_entry.pack(pady=5)

    # Height
    ttk.Label(sign_in_window, text="Height (cm):").pack(pady=5)
    height_entry = ttk.Entry(sign_in_window, width=30)
    height_entry.pack(pady=5)

    # Activity Level
    ttk.Label(sign_in_window, text="Activity Level:").pack(pady=5)
    activity_level_var = tk.StringVar()
    activity_level_menu = ttk.OptionMenu(sign_in_window, activity_level_var, "Select", "Sedentary", "Lightly active", "Moderately active", "Very active",
                                   "Extra active")
    activity_level_menu.pack(pady=5)

    # Submit button
    ttk.Button(sign_in_window, text="Submit", command=submit_user_details).pack(pady=10)

def log_in():
    def submit_user_id():
        user_id = user_id_entry.get()
        if not user_id:
            messagebox.showerror("Error", "User ID is required!")
        else:
            messagebox.showinfo("Success", f"Welcome back! User ID: {user_id}")
            log_in_window.destroy()  # Close the login window
            shared.root.destroy()
            shared.user_id = user_id
            open_main_menu()  # Open the main menu


    # Create the login window
    log_in_window = tk.Toplevel()
    log_in_window.title("Log In")
    log_in_window.geometry("300x200")
    log_in_window.configure(bg="#f7f9fc")

    # Title label
    tk.Label(log_in_window, text="Log In", font=("Helvetica", 16), bg="#f7f9fc").pack(pady=10)

    # User ID field
    ttk.Label(log_in_window, text="User ID:").pack(pady=5)
    user_id_entry = ttk.Entry(log_in_window, width=30)
    user_id_entry.pack(pady=5)

    # Submit button
    ttk.Button(log_in_window, text="Submit", command=submit_user_id).pack(pady=20)

    # Wait for the user to close the window
    #log_in_window.wait_window()


