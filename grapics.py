import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Dummy user ID for testing
current_user_id = 1

# Function to handle sign-in
def sign_in():
    messagebox.showinfo("Sign In", "Sign-In functionality is under development.")

# Function to handle log-in
def log_in():
    messagebox.showinfo("Log In", "Log-In functionality is under development.")

# Open the main menu
def open_main_menu():
    def daily_gap_window():
        messagebox.showinfo("Daily Gap", "Daily Gap feature is under development.")

    def insert_eaten_window():
        def submit_food():
            food_name = food_entry.get()
            amount = amount_entry.get()
            # Call insert_eaten (assumed implemented)
            insert_eaten(current_user_id, "2024-11-27", food_name, float(amount))
            messagebox.showinfo("Success", f"Food '{food_name}' added with amount {amount}!")
            food_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)

        food_window = tk.Toplevel(main_menu)
        food_window.title("Insert Eaten Food")
        food_window.geometry("400x300")

        tk.Label(food_window, text="Food Name:").pack(pady=5)
        food_entry = tk.Entry(food_window)
        food_entry.pack(pady=5)

        tk.Label(food_window, text="Amount (g/ml):").pack(pady=5)
        amount_entry = tk.Entry(food_window)
        amount_entry.pack(pady=5)

        tk.Button(food_window, text="Submit", command=submit_food).pack(pady=20)

    def recommendations_window():
        messagebox.showinfo("Recommendations", "Recommendations feature is under development.")

    def statistics_window():
        messagebox.showinfo("Statistics", "Statistics feature is under development.")

    def trends_window():
        messagebox.showinfo("Trends", "Trends feature is under development.")

    def comparison_window():
        messagebox.showinfo("Comparison", "Team Comparison feature is under development.")

    main_menu = tk.Tk()
    main_menu.title("Nutrition Tracker - Main Menu")
    main_menu.geometry("400x500")

    tk.Label(main_menu, text="Welcome to Nutrition Tracker!", font=("Arial", 16)).pack(pady=20)

    tk.Button(main_menu, text="View Daily Gap", command=daily_gap_window, width=20).pack(pady=10)
    tk.Button(main_menu, text="Insert Eaten Food", command=insert_eaten_window, width=20).pack(pady=10)
    tk.Button(main_menu, text="View Recommendations", command=recommendations_window, width=20).pack(pady=10)
    tk.Button(main_menu, text="View Statistics", command=statistics_window, width=20).pack(pady=10)
    tk.Button(main_menu, text="Track Trends", command=trends_window, width=20).pack(pady=10)
    tk.Button(main_menu, text="Team Comparison", command=comparison_window, width=20).pack(pady=10)

    main_menu.mainloop()

# Opening window
def open_app():
    root = tk.Tk()
    root.title("Nutrition Tracker")
    root.geometry("400x300")

    tk.Label(root, text="Nutrition Tracker", font=("Arial", 20)).pack(pady=30)

    tk.Button(root, text="Sign In", command=sign_in, width=15).pack(pady=10)
    tk.Button(root, text="Log In", command=log_in, width=15).pack(pady=10)
    tk.Button(root, text="Enter Main Menu", command=lambda: [root.destroy(), open_main_menu()], width=15).pack(pady=10)

    root.mainloop()

# Run the application
open_app()
