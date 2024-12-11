import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  # For handling the logo image
import shared
from fun_names import *

def daily_gap_window():
    def submit_date():
        # Get the date from the entry field
        date = date_entry.get()

        if not date:
            messagebox.showerror("Error", "Please enter a date!")
        else:
            try:
                # Fetch the daily gap using the provided date
                daily_gap = get_daily_gap(shared.user_id, date)

                # Display the daily gap in a message box
                messagebox.showinfo("Daily Gap", f"Daily Gap: {daily_gap}")
            except Exception as e:
                # Handle any potential errors gracefully
                messagebox.showerror("Error", f"An error occurred: {e}")

    # Create the daily gap window
    gap_window = tk.Toplevel()
    gap_window.title("Daily Gap")
    gap_window.geometry("300x200")
    gap_window.configure(bg="#f7f9fc")

    # Title label
    tk.Label(gap_window, text="Enter Date", font=("Helvetica", 16), bg="#f7f9fc").pack(pady=10)

    # Date entry field
    ttk.Label(gap_window, text="Date (YYYY-MM-DD):").pack(pady=5)
    date_entry = ttk.Entry(gap_window, width=30)
    date_entry.pack(pady=5)

    # Submit button
    ttk.Button(gap_window, text="Submit", command=submit_date).pack(pady=20)


def insert_eaten_window():
    def submit_food():
        food_name = food_entry.get()
        amount = amount_entry.get()
        date = date_entry.get()
        flag= insert_eaten(food_name, amount, shared.user_id, date)
        if flag:
            messagebox.showinfo("Success", f"Food '{food_name}' added with amount {amount} g!")
        else:
            messagebox.showerror("Error", f"Food '{food_name}' not found in the database!")
        food_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        food_window.destroy()

    food_window = tk.Toplevel()
    food_window.title("Insert Eaten Food")
    food_window.geometry("400x400")
    food_window.configure(bg="#f7f9fc")

    tk.Label(food_window, text="Insert Eaten Food", font=("Helvetica", 16), bg="#f7f9fc").pack(pady=20)
    ttk.Label(food_window, text="Food Name:").pack(pady=5)
    food_entry = ttk.Entry(food_window, width=30)
    food_entry.pack(pady=5)

    ttk.Label(food_window, text="Amount (in g):").pack(pady=5)
    amount_entry = ttk.Entry(food_window, width=30)
    amount_entry.pack(pady=5)

    # Date entry field
    ttk.Label(food_window, text="Date (YYYY-MM-DD):").pack(pady=5)
    date_entry = ttk.Entry(food_window, width=30)
    date_entry.pack(pady=5)

    ttk.Button(food_window, text="Submit", command=submit_food).pack(pady=20)


def recommendations_window():
    messagebox.showinfo("Recommendations", "Recommendations feature is under development.")



def statistics_window():
    messagebox.showinfo("Statistics", "Statistics feature is under development.")


def trends_window():
    messagebox.showinfo("Trends", "Trends feature is under development.")


def comparison_window():
    messagebox.showinfo("Comparison", "Team Comparison feature is under development.")
# Open the main menu
def open_main_menu():

    main_menu = tk.Tk()
    main_menu.title("Nutrition Tracker - Main Menu")
    main_menu.geometry("500x600")
    main_menu.configure(bg="#eaf4fc")

    tk.Label(main_menu, text="Welcome to Nutrition Tracker!", font=("Helvetica", 18), bg="#eaf4fc").pack(pady=30)

    button_style = ttk.Style()
    button_style.configure("TButton", font=("Helvetica", 12), padding=5)

    ttk.Button(main_menu, text="View Daily Gap", command=daily_gap_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="Insert Eaten Food", command=insert_eaten_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="View Recommendations", command=recommendations_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="View Statistics", command=statistics_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="Track Trends", command=trends_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="Team Comparison", command=comparison_window, width=25).pack(pady=10)

    main_menu.mainloop()