import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  # For handling the logo image
import shared
from fun_names import *
from tkinter import font
from tkinter import ttk
import tkinter as tk


def display_food_for_nutrient(nutrient_name):
    # Create a new window
    new_window = tk.Toplevel()
    new_window.title(f"Food Recommendations for {nutrient_name}")
    new_window.geometry("300x300")  # Adjust size as needed

    # Get recommendations
    recommendations = recommand_food_for_nutrient(nutrient_name)  # Assuming this function returns a list of foods or text

    # Add a label to display the nutrient name
    nutrient_label = tk.Label(
        new_window,
        text=f"Recommended Foods for {nutrient_name}",
        font=("Helvetica", 12, "bold")
    )
    nutrient_label.pack(pady=10)

    # Add a text widget or label to display the recommendations
    if recommendations:
        for food in recommendations:
            food_label = tk.Label(new_window, text=f"- {food}", font=("Helvetica", 10))
            food_label.pack(anchor="w", padx=20)
    else:
        no_recommendations_label = tk.Label(
            new_window,
            text="No recommendations available.",
            font=("Helvetica", 10),
            fg="red"
        )
        no_recommendations_label.pack(pady=20)

    # Add a close button
    close_button = tk.Button(
        new_window,
        text="Close",
        command=new_window.destroy,
        font=("Helvetica", 10)
    )
    close_button.pack(pady=10)


def display_daily_gap(daily_gap):
    """
    Displays the daily nutritional gaps in a new Tkinter window with color-coded values.

    Arguments:
    daily_gap -- a list of gap values corresponding to predefined nutrient names.
    """
    # Predefined list of nutrient names corresponding to the values in daily_gap
    nutrient_names = [
        "Vitamin_A_mg",
        "Vitamin_C_mg",
        "Vitamin_D_mg",
        "Vitamin_E_mg",
        "Vitamin_K_mg",
        "Thiamin_mg",
        "Riboflavin_mg",
        "Niacin_mg",
        "Vitamin_B6_mg",
        "Vitamin_B12_mg",
        "Pantothenic_acid_mg",
        "Caloric_Value_kcal"
    ]

    # Create a new window
    gap_display_window = tk.Toplevel()
    gap_display_window.title("Daily Gap")
    gap_display_window.geometry("400x600")
    gap_display_window.configure(bg="#f7f9fc")

    # Title label
    tk.Label(
        gap_display_window,
        text="Daily Nutritional Gap",
        font=("Helvetica", 16),
        bg="#f7f9fc"
    ).pack(pady=10)

    # Instructions label
    tk.Label(
        gap_display_window,
        text="Excess values are in green, deficiencies are in red.",
        font=("Helvetica", 10),
        bg="#f7f9fc",
        fg="gray"
    ).pack(pady=5)

    # Display each nutrient gap with color-coding
    for nutrient, gap in zip(nutrient_names, daily_gap):
        # Create a frame to hold the nutrient label and button
        frame = tk.Frame(gap_display_window, bg="#f7f9fc")
        frame.pack(fill=tk.X, pady=5)

        # Determine the color based on the gap value
        if gap > 0:
            color = "green"  # Excess
            value_text = f"+{gap}"  # Add "+" for excess values
        elif gap < 0:
            color = "red"  # Deficiency
            value_text = str(gap)
        else:
            color = "black"  # No gap
            value_text = str(gap)

        # Create the label for this nutrient
        tk.Label(
            frame,
            text=f"{nutrient}: {value_text}",
            font=("Helvetica", 10),
            bg="#f7f9fc",
            fg=color,
            width=25,
            anchor="w"
        ).pack(side=tk.LEFT, padx=10)

        custom_font = font.Font(family="Helvetica", size=8)  # Smaller size
        if nutrient != "Caloric_Value_kcal" and gap < 0:
            # Button to show recommendation
            button = tk.Button(
                frame,
                text="Food Recommendation",
                font=custom_font,  # Apply the custom font
                width=20,  # Adjust width to make the button smaller
                command=lambda n=nutrient: display_food_for_nutrient(n)
            )
            button.pack(side=tk.RIGHT, padx=10)

    # Close button
    ttk.Button(
        gap_display_window,
        text="Close",
        command=gap_display_window.destroy
    ).pack(pady=20)



def daily_gap_window():
    def submit_date():
        # Get the date from the entry field
        date = date_entry.get()

        if not date:
            messagebox.showerror("Error", "Please enter a date!")
        else:
            try:
                # list of all the gaps for the user on the given date
                daily_gap = get_daily_gap(shared.user_id, date)
                if not daily_gap:
                    messagebox.showinfo("Daily Gap", "No data available for the selected date.")
                    return

                # Display the daily gap
                display_daily_gap(daily_gap)

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
        flag = insert_eaten(food_name, amount, shared.user_id, date)
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


def blood_test():
    """
    Allows the user to select their deficiencies after a blood test and opens a window
    with buttons for each selected deficiency, calling display_food_for_nutrient.
    """
    # List of nutrients
    nutrient_deficiencies = [
        "Protein_g",
        "Dietary_Fiber_g",
        "Cholesterol_mg",
        "Sodium_g",
        "Water_g",
        "Vitamin_A_mg",
        "Thiamin_mg",
        "Folic_acid_mg",
        "Vitamin_B12_mg",
        "Riboflavin_mg",
        "Niacin_mg",
        "Pantothenic_acid_mg",
        "Vitamin_B6_mg",
        "Vitamin_C_mg",
        "Vitamin_D_mg",
        "Vitamin_E_mg",
        "Vitamin_K_mg",
        "Calcium_mg",
        "Copper_mg",
        "Iron_mg",
        "Magnesium_mg",
        "Manganese_mg",
        "Phosphorus_mg",
        "Potassium_mg",
        "Selenium_mg",
        "Zinc_mg"
    ]

    # Create a new Tkinter window
    test_window = tk.Toplevel()
    test_window.title("Select Deficiencies")
    test_window.geometry("400x600")  # Adjust the size as needed
    test_window.configure(bg="#f7f9fc")

    # Title label
    tk.Label(
        test_window,
        text="Select Nutritional Deficiencies",
        font=("Helvetica", 14, "bold"),
        bg="#f7f9fc"
    ).pack(pady=10)

    # Scrollable frame for nutrient checkboxes
    scroll_frame = tk.Frame(test_window, bg="#f7f9fc")
    scroll_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

    # Create a scrollbar
    scrollbar = tk.Scrollbar(scroll_frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a canvas for scrolling
    canvas = tk.Canvas(scroll_frame, bg="#f7f9fc", yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    scrollbar.config(command=canvas.yview)

    # Frame to hold checkboxes
    checkbox_frame = tk.Frame(canvas, bg="#f7f9fc")
    canvas.create_window((0, 0), window=checkbox_frame, anchor="nw")

    # List to hold the selected deficiencies
    selected_deficiencies = []

    # Function to toggle deficiencies in the list
    def toggle_deficiency(nutrient):
        if nutrient in selected_deficiencies:
            selected_deficiencies.remove(nutrient)
        else:
            selected_deficiencies.append(nutrient)

    # Create checkboxes for each nutrient
    for nutrient in nutrient_deficiencies:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(
            checkbox_frame,
            text=nutrient.replace("_", " ").title(),
            variable=var,
            onvalue=True,
            offvalue=False,
            bg="#f7f9fc",
            anchor="w",
            command=lambda n=nutrient: toggle_deficiency(n)
        )
        checkbox.pack(anchor="w", padx=10, pady=5)

    # Function to display buttons for selected deficiencies
    def show_deficiency_buttons():
        if not selected_deficiencies:
            messagebox.showwarning("Warning", "No deficiencies selected!")
            return

        # Create a new window for the buttons
        button_window = tk.Toplevel()
        button_window.title("Deficiency Recommendations")
        button_window.geometry("400x600")
        button_window.configure(bg="#f7f9fc")

        # Title label
        tk.Label(
            button_window,
            text="Recommendations for Selected Deficiencies",
            font=("Helvetica", 12, "bold"),
            bg="#f7f9fc"
        ).pack(pady=10)

        # Create a button for each selected deficiency
        for deficiency in selected_deficiencies:
            button = tk.Button(
                button_window,
                text=f"{deficiency.replace('_', ' ').title()}",
                font=("Helvetica", 10),
                command=lambda n=deficiency: display_food_for_nutrient(n),
                bg="#f7f9fc",
                fg="black",
                padx=10,
                pady=5
            )
            button.pack(pady=10)

        # Close button
        close_button = tk.Button(
            button_window,
            text="Close",
            command=button_window.destroy,
            font=("Helvetica", 10),
            bg="#f7f9fc",
            fg="black"
        )
        close_button.pack(pady=20)

    # Submit button
    submit_button = tk.Button(
        test_window,
        text="Submit",
        command=show_deficiency_buttons,
        font=("Helvetica", 10, "bold"),
        bg="#4caf50",
        fg="white"
    )
    submit_button.pack(pady=20)

    # Configure the canvas to update the scroll region
    def configure_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    checkbox_frame.bind("<Configure>", configure_canvas)



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
    ttk.Button(main_menu, text="Deficiencies From Blood Test", command=blood_test, width=25).pack(pady=10)
    ttk.Button(main_menu, text="Insert Eaten Food", command=insert_eaten_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="View Recommendations", command=recommendations_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="View Statistics", command=statistics_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="Track Trends", command=trends_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="Team Comparison", command=comparison_window, width=25).pack(pady=10)

    main_menu.mainloop()
