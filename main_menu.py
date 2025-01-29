from datetime import datetime
from sql_queries import *
from tkinter import font
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from AutocompleteEntry import AutocompleteEntry
import sys


def display_food_for_nutrient(nutrient_name):
    # Create a new window
    new_window = tk.Toplevel()
    new_window.title(f"Food Recommendations for {nutrient_name}")
    new_window.geometry("700x500")  # Adjust size as needed

    # Get recommendations
    recommendations = recommand_food_for_nutrient(
        nutrient_name)  # Assuming this function returns a list of foods or text

    # Add a label to display the nutrient name
    clear_name = nutrient_name.replace("_", " ")[:-3]
    nutrient_label = tk.Label(
        new_window,
        text=f"Recommended Foods for {clear_name}",
        font=("Helvetica", 12, "bold")
    )
    nutrient_label.pack(pady=10)

    # Add a text widget or label to display the recommendations
    if recommendations:
        for food in recommendations:
            # Remove unwanted characters like parentheses and single quotes
            clean_food = str(food).strip("()',")
            food_label = tk.Label(
                new_window,
                text=f"- {clean_food.capitalize()}",  # Capitalize for better readability
                font=("Helvetica", 10),
                bg="#f7f9fc"
            )
            food_label.pack(anchor="w", padx=20, pady=2)  # Add padding for cleaner look

            # food_label = tk.Label(new_window, text=f"- {food}", font=("Helvetica", 10))
            # food_label.pack(anchor="w", padx=20)

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
    daily_gap -- a list of gap percentages corresponding to predefined nutrient names.
                 Positive values indicate no gap (excess), and negative values indicate the percentage of the gap.
    """

    names = [
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

    nutrient_names = {
        "Vitamin A Gap": names[0],
        "Vitamin C Gap": names[1],
        "Vitamin D Gap": names[2],
        "Vitamin E Gap": names[3],
        "Vitamin K Gap": names[4],
        "Thiamin Gap": names[5],
        "Riboflavin Gap": names[6],
        "Niacin Gap": names[7],
        "Vitamin B6 Gap": names[8],
        "Vitamin B12 Gap": names[9],
        "Pantothenic Acid Gap": names[10],
        "Calories Gap": names[11]
    }

    # Create a new window
    gap_display_window = tk.Toplevel()
    gap_display_window.title("Daily Nutritional Gap")
    gap_display_window.geometry("600x600")
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
        text="Positive values indicate excess and negative values indicate deficiency.",
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
            color = "green"  # No gap (excess)
            value_text = f"{gap:.2f}%"  # Format percentage
        elif gap == 0:
            color = "black"
            value_text = "0%"  # No gap
        else:
            color = "red"  # Gap (deficiency)
            value_text = f"{gap:.2f}%"  # Format percentage

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
        if nutrient != "Calories Gap" and gap < 0:
            # Button to show recommendation
            button = tk.Button(
                frame,
                text="Food Recommendation",
                font=custom_font,  # Apply the custom font
                width=20,  # Adjust width to make the button smaller
                command=lambda n=nutrient_names[nutrient]: display_food_for_nutrient(n)
            )
            button.pack(side=tk.RIGHT, padx=10)

    # Close button
    ttk.Button(
        gap_display_window,
        text="Close",
        command=gap_display_window.destroy
    ).pack(pady=20)


def is_valid_date(date):
    """
    Check if the given date is in the correct format (YYYY-MM-DD).

    Arguments:
    date -- a string representing a date

    Returns:
    True if the date is valid, False otherwise.
    """
    try:
        # Attempt to parse the date
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def daily_gap_window():
    def submit_date():
        # Get the date from the entry field
        date = date_entry.get_date()

        if not date:
            messagebox.showerror("Error", "Please enter a date!")
        else:
            try:
                # check that the date is valid format
                if not is_valid_date(date):
                    messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
                    return

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
    gap_window.geometry("300x500")
    gap_window.configure(bg="#f7f9fc")

    # Title label
    tk.Label(gap_window, text="Enter Date", font=("Helvetica", 16), bg="#f7f9fc").pack(pady=10)

    # Date entry field
    ttk.Label(gap_window, text="Date:").pack(pady=5)
    # date_entry = ttk.Entry(gap_window, width=30)
    # date_entry.pack(pady=5)
    date_entry = Calendar(gap_window, selectmode='day', date_pattern='yyyy-mm-dd', background='green')  # Set the date format
    date_entry.pack(pady=10)

    # Submit button
    ttk.Button(gap_window, text="Submit", command=submit_date).pack(pady=20)


# def insert_eaten_window():
#     def submit_food():
#         food_name = food_entry.get()
#         amount = amount_entry.get()
#         date = date_entry.get_date()
#         # check that the date is valid format
#         if not is_valid_date(date):
#             messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
#             return
#         # check that the amount is valid number
#         if not amount.isdigit():
#             messagebox.showerror("Error", "Amount should be a number!")
#             return
#         flag = insert_eaten(food_name, amount, shared.user_id, date)
#         if flag:
#             messagebox.showinfo("Success", f"Food '{food_name}' added with amount {amount} g!")
#         else:
#             messagebox.showerror("Error", f"Food '{food_name}' not found in the database!")
#         food_entry.delete(0, tk.END)
#         amount_entry.delete(0, tk.END)
#         date_entry.delete(0, tk.END)
#         food_window.destroy()
#
#     food_window = tk.Toplevel()
#     food_window.title("Insert Eaten Food")
#     food_window.geometry("400x600")
#     food_window.configure(bg="#f7f9fc")
#
#     tk.Label(food_window, text="Insert Eaten Food", font=("Helvetica", 16), bg="#f7f9fc").pack(pady=20)
#     ttk.Label(food_window, text="Food Name:").pack(pady=5)
#     food_entry = ttk.Entry(food_window, width=30)
#     food_entry.pack(pady=5)
#
#     ttk.Label(food_window, text="Amount (in g):").pack(pady=5)
#     amount_entry = ttk.Entry(food_window, width=30)
#     amount_entry.pack(pady=5)
#
#     # Date entry field
#     ttk.Label(food_window, text="Date:").pack(pady=5)
#     # date_entry = ttk.Entry(food_window, width=30)
#     # date_entry.pack(pady=5)
#     date_entry = Calendar(food_window, selectmode='day', date_pattern='yyyy-mm-dd', background='green')  # Set the date format
#     date_entry.pack(pady=10)
#
#     ttk.Button(food_window, text="Submit", command=submit_food).pack(pady=20)
def insert_eaten_window():
    def submit_food():
        food_name = food_entry.var.get()
        amount = amount_entry.get()
        date = date_entry.get_date()

        if not is_valid_date(date):
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return
        if not amount.isdigit():
            messagebox.showerror("Error", "Amount should be a number!")
            return

        flag = insert_eaten(food_name, amount, shared.user_id, date)
        if flag:
            messagebox.showinfo("Success", f"Food '{food_name}' added with amount {amount} g!")
        else:
            messagebox.showerror("Error", f"Food '{food_name}' not found in the database!")
        food_entry.var.set("")
        amount_entry.delete(0, tk.END)
        #date_entry.delete(0, tk.END)
        food_window.destroy()

    food_window = tk.Toplevel()
    food_window.title("Insert Eaten Food")
    food_window.geometry("400x600")
    food_window.configure(bg="#f7f9fc")

    tk.Label(food_window, text="Insert Eaten Food", font=("Helvetica", 16), bg="#f7f9fc").pack(pady=20)
    ttk.Label(food_window, text="Food Name:").pack(pady=5)

    # Get food list for autocomplete
    food_list = get_all_food_names()
    food_entry = AutocompleteEntry(food_window, food_list, width=30)
    food_entry.pack(pady=5)

    ttk.Label(food_window, text="Amount (in g):").pack(pady=5)
    amount_entry = ttk.Entry(food_window, width=30)
    amount_entry.pack(pady=5)

    ttk.Label(food_window, text="Date:").pack(pady=5)
    date_entry = Calendar(food_window, selectmode='day', date_pattern='yyyy-mm-dd', background='green')
    date_entry.pack(pady=10)

    ttk.Button(food_window, text="Submit", command=submit_food).pack(pady=20)


def blood_test():
    """
    Allows the user to select their deficiencies after a blood test and opens a window
    with buttons for each selected deficiency, calling display_food_for_nutrient.
    """
    import tkinter as tk
    from tkinter import messagebox

    # List of nutrients (clean display names)
    nutrient_deficiencies = [
        "Protein",
        "Dietary Fiber",
        "Cholesterol",
        "Sodium",
        "Water",
        "Vitamin A",
        "Thiamin",
        "Folic Acid",
        "Vitamin B12",
        "Riboflavin",
        "Niacin",
        "Pantothenic Acid",
        "Vitamin B6",
        "Vitamin C",
        "Vitamin D",
        "Vitamin E",
        "Vitamin K",
        "Calcium",
        "Copper",
        "Iron",
        "Magnesium",
        "Manganese",
        "Phosphorus",
        "Potassium",
        "Selenium",
        "Zinc"
    ]

    # Mapping of deficiencies to their corresponding database field names
    deficiency_mapping = {
        "Protein": "Protein_g",
        "Dietary Fiber": "Dietary_Fiber_g",
        "Cholesterol": "Cholesterol_mg",
        "Sodium": "Sodium_g",
        "Water": "Water_g",
        "Vitamin A": "Vitamin_A_mg",
        "Thiamin": "Thiamin_mg",
        "Folic Acid": "Folic_acid_mg",
        "Vitamin B12": "Vitamin_B12_mg",
        "Riboflavin": "Riboflavin_mg",
        "Niacin": "Niacin_mg",
        "Pantothenic Acid": "Pantothenic_acid_mg",
        "Vitamin B6": "Vitamin_B6_mg",
        "Vitamin C": "Vitamin_C_mg",
        "Vitamin D": "Vitamin_D_mg",
        "Vitamin E": "Vitamin_E_mg",
        "Vitamin K": "Vitamin_K_mg",
        "Calcium": "Calcium_mg",
        "Copper": "Copper_mg",
        "Iron": "Iron_mg",
        "Magnesium": "Magnesium_mg",
        "Manganese": "Manganese_mg",
        "Phosphorus": "Phosphorus_mg",
        "Potassium": "Potassium_mg",
        "Selenium": "Selenium_mg",
        "Zinc": "Zinc_mg"
    }

    # Create a new Tkinter window
    test_window = tk.Toplevel()
    test_window.title("Select Deficiencies")
    test_window.geometry("400x600")
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
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
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
            text=nutrient,
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
        button_window.title("Food Recommendations Based On Blood Test")
        button_window.geometry("400x600")
        button_window.configure(bg="#f7f9fc")

        # Title label for the button window
        tk.Label(
            button_window,
            text="Food Recommendations Based On Blood Test",
            font=("Helvetica", 12, "bold"),
            bg="#f7f9fc"
        ).pack(pady=10)

        # Add a scrollbar to the button window
        scroll_frame = tk.Frame(button_window, bg="#f7f9fc")
        scroll_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(scroll_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas = tk.Canvas(scroll_frame, bg="#f7f9fc", yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=canvas.yview)

        button_frame = tk.Frame(canvas, bg="#f7f9fc")
        canvas.create_window((0, 0), window=button_frame, anchor="nw")

        # Create a button for each selected deficiency
        for deficiency in selected_deficiencies:
            nutrient_field = deficiency_mapping.get(deficiency, deficiency)  # Map to database field
            button = tk.Button(
                button_frame,
                text=deficiency,  # Display the clean name
                font=("Helvetica", 10),
                command=lambda n=nutrient_field: display_food_for_nutrient(n),  # Pass the correct field name
                bg="gray",
                fg="black",  # Black text
                padx=10,
                pady=5
            )
            button.pack(pady=10, side=tk.TOP, anchor="center")  # Ensure buttons are centered

        # Close button
        close_button = tk.Button(
            button_frame,
            text="Close",
            command=button_window.destroy,
            font=("Helvetica", 10),
            bg="#d32f2f",  # Red background for the close button
            fg="white"  # White text for contrast
        )
        close_button.pack(pady=20, side=tk.TOP, anchor="center")  # Center the close button

        # Configure the canvas to update the scroll region
        def configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        button_frame.bind("<Configure>", configure_canvas)

    # Submit button
    submit_button = tk.Button(
        test_window,
        text="Submit",
        command=show_deficiency_buttons,
        font=("Helvetica", 10, "bold"),
        bg="#4caf50",  # Green for the submit button
        fg="white"  # White text
    )
    submit_button.pack(pady=20)

    # Configure the canvas to update the scroll region
    def configure_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    checkbox_frame.bind("<Configure>", configure_canvas)


def recommendations_window():
    messagebox.showinfo("Recommendations", "Recommendations feature is under development.")


def statistics_window():
    """
    Displays a statistics window showing all average nutrient values.
    """
    try:
        user_id = shared.user_id  # Assuming shared.user_id is available

        # Nutrient names corresponding to the returned values from avg_consumption
        nutrient_names = [
            "Avg Calories",
            "Avg Protein (g)",
            "Avg Fiber (g)",
            "Avg Cholesterol (mg)",
            "Avg Sodium (g)",
            "Avg Water (g)",
            "Avg Vitamin A (mg)",
            "Avg Thiamin (mg)",
            "Avg Folic Acid (mg)",
            "Avg Vitamin B12 (mg)",
            "Avg Riboflavin (mg)",
            "Avg Niacin (mg)",
            "Avg Pantothenic Acid (mg)",
            "Avg Vitamin B6 (mg)",
            "Avg Vitamin C (mg)",
            "Avg Vitamin D (mg)",
            "Avg Vitamin E (mg)",
            "Avg Vitamin K (mg)",
            "Avg Calcium (mg)",
            "Avg Copper (mg)",
            "Avg Iron (mg)",
            "Avg Magnesium (mg)",
            "Avg Manganese (mg)",
            "Avg Phosphorus (mg)",
            "Avg Potassium (mg)",
            "Avg Selenium (mg)",
            "Avg Zinc (mg)"
        ]

        def show_avg(period):
            """
            Displays average consumption data for the selected period.
            """
            try:
                stats = avg_consumption(user_id, period)  # Replace with your actual function
                if not stats or len(stats) != len(nutrient_names):
                    raise ValueError("Invalid or missing data for the selected period.")

                # Clear previous data
                for widget in data_frame.winfo_children():
                    widget.destroy()

                # Display the stats dynamically
                for i, (name, value) in enumerate(zip(nutrient_names, stats)):
                    tk.Label(
                        data_frame,
                        text=f"{name}:",
                        font=("Helvetica", 12, "bold"),
                        bg="#f0f8ff",
                        anchor="w"
                    ).grid(row=i, column=0, sticky="w", padx=10, pady=5)

                    tk.Label(
                        data_frame,
                        text=f"{value}",
                        font=("Helvetica", 12),
                        bg="#f0f8ff",
                        anchor="e"
                    ).grid(row=i, column=1, sticky="e", padx=10, pady=5)
            except Exception as e:
                messagebox.showerror("Error", f"Could not retrieve data: {str(e)}")

        # Create the statistics window
        stats_window = tk.Toplevel()
        stats_window.title("User Statistics")
        stats_window.geometry("500x600")
        stats_window.configure(bg="#f0f8ff")

        # Title label
        tk.Label(
            stats_window,
            text="User Statistics",
            font=("Helvetica", 16, "bold"),
            bg="#4682b4",
            fg="white",
            pady=10
        ).pack(fill=tk.X)

        # Sub-title
        tk.Label(
            stats_window,
            text="Select a time period to view averages",
            font=("Helvetica", 12),
            bg="#f0f8ff"
        ).pack(pady=10)

        # Frame for buttons
        button_frame = tk.Frame(stats_window, bg="#f0f8ff")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Last Week Average",
            command=lambda: show_avg(7),
            font=("Helvetica", 10),
            bg="#4caf50",
            fg="white",
            padx=10,
            pady=5
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="Last Month Average",
            command=lambda: show_avg(30),
            font=("Helvetica", 10),
            bg="#4caf50",
            fg="white",
            padx=10,
            pady=5
        ).grid(row=0, column=1, padx=10)

        # Scrollable frame for data
        scroll_frame = tk.Frame(stats_window, bg="#f0f8ff")
        scroll_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        scrollbar = tk.Scrollbar(scroll_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas = tk.Canvas(scroll_frame, bg="#f0f8ff", yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=canvas.yview)

        data_frame = tk.Frame(canvas, bg="#f0f8ff")
        canvas.create_window((0, 0), window=data_frame, anchor="nw")

        def configure_canvas(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        data_frame.bind("<Configure>", configure_canvas)

        # Close button
        tk.Button(
            stats_window,
            text="Close",
            command=stats_window.destroy,
            font=("Helvetica", 10, "bold"),
            bg="#d32f2f",
            fg="white",
            padx=10,
            pady=5
        ).pack(pady=20)

    except Exception as e:
        messagebox.showerror("Error", f"Could not open statistics window: {str(e)}")


def submit_selected_teams(selected_teams):
    # Simulate a user ID (replace with actual user ID logic)
    user_id = shared.user_id
    already_in_groups = []

    for team_name, team_id in selected_teams:
        if not user_join_team(user_id, team_id):
            already_in_groups.append(team_name)

    if already_in_groups:
        messagebox.showerror("Join Team", f"You are already in these groups: {', '.join(already_in_groups)}")

    successfully_joined = [team_name for team_name, team_id in selected_teams if team_name not in already_in_groups]
    if successfully_joined:
        messagebox.showinfo("Join Team", f"Successfully joined the selected teams: {', '.join(successfully_joined)}")


def join_team_window():
    teams = get_all_teams()
    if not teams:
        messagebox.showinfo("Join Team", "No teams available.")
        return

    # Create the main window
    root = tk.Toplevel()
    root.title("Choose Groups to Join")

    # Create a title label
    title_label = tk.Label(root, text="Choose Groups to Join", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    # Create a frame for the canvas and scrollbar
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create a canvas
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create an inner frame in the canvas
    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # Store selected teams
    selected_teams = []

    def toggle_team(team_name, team_id):
        team_tuple = (team_name, team_id)
        if team_tuple in selected_teams:
            selected_teams.remove(team_tuple)
        else:
            selected_teams.append(team_tuple)

    # Create checkboxes for each team
    for team_id, team_name in teams:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(inner_frame, text=team_name, variable=var,
                                  command=lambda t=team_name, i=team_id: toggle_team(t, i))
        checkbox.pack(anchor="w", padx=5, pady=2)

    # Update the scroll region
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    inner_frame.bind("<Configure>", on_frame_configure)

    # Submit button
    submit_button = tk.Button(root, text="Submit", command=lambda: submit_selected_teams(selected_teams), bg="green",
                              fg="white", font=("Helvetica", 12, "bold"))
    submit_button.pack(pady=10)

    # Run the main loop
    #root.mainloop()


def show_teams():
    # Simulate a user ID (replace with actual user ID logic)
    user_id = shared.user_id
    teams = get_teams_for_user(user_id)

    if not teams:
        messagebox.showinfo("My Teams", "You are not part of any team.")
        return

    # Create the main window
    root = tk.Toplevel()
    root.title("My Teams")

    # Create a title label
    title_label = tk.Label(root, text="Teams You Are Part Of", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    # Create a frame for the canvas and scrollbar
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create a canvas
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create an inner frame in the canvas
    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # Populate the inner frame with team names
    for team_id, team_name in teams:
        label = tk.Label(inner_frame, text=team_name, font=("Helvetica", 12))
        label.pack(anchor="w", padx=5, pady=2)

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    inner_frame.bind("<Configure>", on_frame_configure)

    # Run the main loop
    #root.mainloop()


def leave_team_window():
    # Simulate a user ID (replace with actual user ID logic)
    user_id = shared.user_id  # Assuming `shared.user_id` stores the current user ID
    teams = get_teams_for_user(user_id)

    if not teams:
        messagebox.showinfo("Leave Team", "You are not part of any team.")
        return

    # Create the window
    root = tk.Toplevel()
    root.title("Leave Team")
    root.geometry("400x400")

    # Create a title label
    title_label = tk.Label(root, text="Select a Team to Leave", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    # Add a dropdown menu for team selection
    team_dropdown = ttk.Combobox(root, state="readonly", width=30)
    team_dropdown['values'] = [team_name for _, team_name in teams]  # Populate dropdown with team names
    team_dropdown.pack(pady=10)

    # Add a label to display the currently selected team (for debugging purposes)
    selected_team_label = tk.Label(root, text="", font=("Helvetica", 12))
    selected_team_label.pack(pady=5)

    def on_team_selected(event):
        # Display the currently selected team
        selected_team_label.config(text=f"Selected Team: {team_dropdown.get()}")
        # print(f"Team selected: {team_dropdown.get()}")  # Debugging: Check selected value

    team_dropdown.bind("<<ComboboxSelected>>", on_team_selected)

    def submit_leave_team():
        # Get the selected team name directly from the Combobox
        team_name = team_dropdown.get()
        if not team_name:
            messagebox.showerror("Error", "Please select a team to leave.")
            return

        # Find the corresponding team ID
        team_id = next((team[0] for team in teams if team[1] == team_name), None)

        if team_id:
            leave_team(user_id, team_id)  # Call the leave_team function
            messagebox.showinfo("Success", f"You have successfully left the team '{team_name}'.")
            root.destroy()
        else:
            messagebox.showerror("Error", "Unable to find the selected team.")

    # Add a submit button
    submit_button = ttk.Button(root, text="Leave Team", command=submit_leave_team)
    submit_button.pack(pady=20)

    # Run the main loop
    #root.mainloop()


def create_team_window():
    # Function to handle the creation of a team
    def handle_create_team():
        team_name = team_entry.get().strip()
        if not team_name:
            messagebox.showerror("Error", "Team name cannot be empty.")
            return

        result = create_new_team(team_name)
        if result == 0:
            messagebox.showerror("Error", f"The team '{team_name}' already exists.")
        else:
            messagebox.showinfo("Success", f"Team '{team_name}' created successfully.")
            new_team_window.destroy()

    # Create the new team window
    new_team_window = tk.Toplevel()
    new_team_window.title("Create New Team")
    new_team_window.geometry("400x400")
    new_team_window.configure(bg="#f7f9fc")

    # Add labels and entry widget for team name
    tk.Label(new_team_window, text="Insert Team Name", font=("Helvetica", 16), bg="#f7f9fc").pack(pady=20)
    ttk.Label(new_team_window, text="Team Name:", background="#f7f9fc").pack(pady=5)
    team_entry = ttk.Entry(new_team_window, width=30)
    team_entry.pack(pady=5)

    # Add a button to create the team
    create_button = ttk.Button(new_team_window, text="Create Team", command=handle_create_team)
    create_button.pack(pady=20)


def trends_window():
    def plot_nutrient_trends_ui(results, nutrient):
        """
        Displays the nutrient gap trends in a histogram format within the UI.

        Parameters:
            results (list of tuples): Each tuple contains the nutrient gap for a week.
            nutrient (str): The name of the nutrient.
            parent_window (tk.Toplevel): The parent window where the results will be displayed.
        """
        # Clear existing content in parent window
        # for widget in parent_window.winfo_children():
        #     widget.destroy()
        #parent_window.destroy()
        plot_window = tk.Toplevel()

        # Set larger window size
        plot_window.geometry("800x600")

        # Add a title
        # tk.Label(
        #     plot_window,
        #     text=f"Weekly Nutrient Gap Trends for {nutrient}, Lower is Better!",
        #     font=("Helvetica", 10),
        #     bg="#f7f9fc"
        # ).pack(pady=10)
        tk.Label(
            plot_window,
            text=f"Weekly {nutrient} Consumption Rate, Higher is Better!",
            font=("Helvetica", 10),
            bg="#f7f9fc"
        ).pack(pady=10)

        # Prepare the data for plotting
        weeks = list(range(1, len(results) + 1))
        #gaps = [result[0] for result in results]
        gaps = [100 - result[0] for result in results]

        # Create a matplotlib figure
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(weeks, gaps, color="skyblue", edgecolor="black")
        #ax.set_title(f"Nutrient Gap Trends for {nutrient}, Lower is Better!", fontsize=10)
        ax.set_ylabel("Consumption Rate (%)", fontsize=10)  # Keep the y-axis label
        ax.set_xlabel("Week", fontsize=10)  # X-axis label
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        # plt.tight_layout()  # Adjust layout to ensure everything fits
        #
        # Embed the matplotlib figure into the Tkinter UI
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        canvas.draw()

        def on_close():
            #print("Closing window...")
            plt.close(fig)
            plot_window.destroy()
        # Add a "Close" button
        ttk.Button(
            plot_window,
            text="Close",
            command=on_close
        ).pack(pady=20)
        plot_window.protocol("WM_DELETE_WINDOW", on_close)
        #plot_window.mainloop()

    def show_trends():
        start = start_date.get_date()
        end = end_date.get_date()
        if not is_valid_date(start) or not is_valid_date(end):
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        # Create a new window for nutrient buttons
        #trends_date_window.destroy()
        nutrient_window = tk.Toplevel()
        nutrient_window.title("Nutrient Trends")
        nutrient_window.geometry("400x600")
        nutrient_window.configure(bg="#f7f9fc")

        # Create a button for each nutrient
        for nutrient in nutrient_names:
            custom_font = font.Font(family="Helvetica", size=12)  # Button font
            frame = tk.Frame(nutrient_window, bg="#f7f9fc")
            frame.pack(fill=tk.X, pady=5)

            # Label for the nutrient
            tk.Label(
                frame,
                text=f"{nutrient}",
                font=("Helvetica", 10),
                bg="#f7f9fc",
                fg="gray",
                width=25,
                anchor="w"
            ).pack(side=tk.LEFT, padx=10)

            # Button to show trends
            button = tk.Button(
                frame,
                text="Show Trends",
                font=("Helvetica", 8),  # Smaller font
                width=12,  # Set a smaller width
                padx=5,  # Reduce horizontal padding
                pady=2,  # Reduce vertical padding
                command=lambda n=nutrient: open_trends_window(nutrient_window, n, start, end)
            )
            button.pack(side=tk.RIGHT, padx=5)  # Reduce side padding

        # Close button
        ttk.Button(
            nutrient_window,
            text="Close",
            command=nutrient_window.destroy
        ).pack(pady=20)

    def open_trends_window(nutrient_window, nutrient, start, end):
        results = trends(shared.user_id, start, end, nutrient)
        #nutrient_window.destroy()
        if not results:
            messagebox.showinfo("Trends", f"No data available for {nutrient} in the selected date range.")
        else:
            # show_trends_window = tk.Toplevel()
            # show_trends_window.title(f"Trends for {nutrient}")
            # show_trends_window.geometry("400x400")
            # show_trends_window.configure(bg="#f7f9fc")
            plot_nutrient_trends_ui(results, nutrient)

    # Nutrient names
    nutrient_names = [
        "Vitamin_A_mg", "Vitamin_C_mg", "Vitamin_D_mg", "Vitamin_E_mg",
        "Vitamin_K_mg", "Thiamin_mg", "Riboflavin_mg", "Niacin_mg",
        "Vitamin_B6_mg", "Vitamin_B12_mg", "Pantothenic_acid_mg"
    ]

    # Main window setup
    trends_date_window = tk.Toplevel()
    trends_date_window.title("Trends")
    trends_date_window.geometry("500x700")
    trends_date_window.configure(bg="#f7f9fc")

    # tk.Label(trends_date_window, text="Insert Start Date (YYYY-MM-DD)", font=("Helvetica", 16), bg="#f7f9fc").pack(pady=20)
    # ttk.Label(trends_date_window, text="Start Date:").pack(pady=5)
    # start_date = ttk.Entry(trends_date_window, width=30)
    # start_date.pack(pady=5)
    #
    # tk.Label(trends_date_window, text="Insert End Date (YYYY-MM-DD)", font=("Helvetica", 16), bg="#f7f9fc").pack(pady=20)
    # ttk.Label(trends_date_window, text="End Date:").pack(pady=5)
    # end_date = ttk.Entry(trends_date_window, width=30)
    # end_date.pack(pady=5)

    # Add calendar for start date selection
    tk.Label(trends_date_window, text="Select Start Date", font=("Helvetica", 16), bg="#f7f9fc").pack(pady=20)
    start_date = Calendar(trends_date_window, selectmode='day', date_pattern='yyyy-mm-dd', background='green')  # Set the date format
    start_date.pack(pady=10)

    # Add calendar for end date selection
    tk.Label(trends_date_window, text="Select End Date", font=("Helvetica", 16), bg="#f7f9fc").pack(pady=20)
    end_date = Calendar(trends_date_window, selectmode='day', date_pattern='yyyy-mm-dd', background='green')  # Set the date format
    end_date.pack(pady=10)

    submit_button = ttk.Button(trends_date_window, text="Show Trends", command=show_trends)
    submit_button.pack(pady=20)

    #trends_date_window.mainloop()


def check_violate_users(team_id, start_date, end_date):
    """
    Check for users with incomplete data and ask the user for the next action.
    :param team_id:
    :param start_date:
    :param end_date:
    :return: True if the user wants to remove the violating users, False if the user wants to enter another date range,
    """
    violating_users = violate_users_of_team(team_id, start_date, end_date)
    violating_user_ids = [user[0] for user in violating_users]  # Extract user IDs

    if violating_user_ids:
        user_list = "\n".join([f"- {user[1]}" for user in violating_users])  # Create a list of usernames
        # Ask the user for the next action
        response = messagebox.askyesnocancel(
            "Users with Incomplete Data Detected",
            f"The following users have days without recorded meal data between {start_date} and {end_date}:\n\n"
            f"{user_list}\n\n"
            "Would you like to remove these users from the team?\n\n"
            "Yes: Remove users\n"
            "No: Exit\n"
        )
        if response is True:  # User clicked 'Yes'
            leave_team_list_of_users(violating_user_ids, team_id)
            return True
        else:
            return False
    return True


def comparison_window():
    def show_competition_results():
        start = start_date.get_date()
        end = end_date.get_date()
        team_name = team_dropdown.get()
        # Find the corresponding team ID
        team_id = next((team[0] for team in teams if team[1] == team_name), None)
        if not check_violate_users(team_id, start, end):
            date_window.destroy()
            return
        results = comparison_team(team_id, start,
                                  end)  # return for every user the average daily gap for each nutrient
        winners_data = winner_in_team_comparison(team_id, start, end)  # return the winner user - the user that
        # has the lowest average daily gap for the highest number of nutrients. if there is a tie, return list of users
        date_window.destroy()  # Close the current window

        if not results:
            messagebox.showinfo("Team Competition", f"No data available in the selected date range.")
        else:
            # Create a new window for trends
            #date_window.destroy() # Close the current window
            perf_window = tk.Toplevel()
            perf_window.title("Team Performance")
            perf_window.geometry("1000x4000")  # Adjust the size of the window
            perf_window.configure(bg="#f7f9fc")
            plot_competitive_nutrient_comparison(results, winners_data, perf_window)

    # Main window setup
    date_window = tk.Toplevel()
    date_window.title("Team Competition")
    date_window.geometry("600x1000")
    date_window.configure(bg="#f7f9fc")

    user_id = shared.user_id  # Assuming `shared.user_id` stores the current user ID
    teams = get_teams_for_user(user_id)

    if not teams:
        messagebox.showinfo("Team Competition", "You are not part of any team.")
        return

    # Add a dropdown menu for team selection
    tk.Label(date_window, text="Select a Team", font=("Helvetica", 16), bg="#f7f9fc").pack(
        pady=20)
    team_dropdown = ttk.Combobox(date_window, state="readonly", width=30)
    team_dropdown['values'] = [team_name for _, team_name in teams]  # Populate dropdown with team names
    team_dropdown.pack(pady=10)

    # tk.Label(date_window, text="Insert Competition Start Date (YYYY-MM-DD)", font=("Helvetica", 16), bg="#f7f9fc").pack(pady=20)
    # ttk.Label(date_window, text="Start Date:").pack(pady=5)
    # start_date = ttk.Entry(date_window, width=30)
    # start_date.pack(pady=5)
    #
    # tk.Label(date_window, text="Insert Competition End Date (YYYY-MM-DD)", font=("Helvetica", 16), bg="#f7f9fc").pack(pady=20)
    # ttk.Label(date_window, text="End Date:").pack(pady=5)
    # end_date = ttk.Entry(date_window, width=30)
    # end_date.pack(pady=5)

    # Add calendar for start date selection
    tk.Label(date_window, text="Select Competition Start Date", font=("Helvetica", 16), bg="#f7f9fc").pack(pady=20)
    start_date = Calendar(date_window, selectmode='day', date_pattern='yyyy-mm-dd', background='green')  # Set the date format
    start_date.pack(pady=10)

    # Add calendar for end date selection
    tk.Label(date_window, text="Select Competition End Date", font=("Helvetica", 16), bg="#f7f9fc").pack(pady=20)
    end_date = Calendar(date_window, selectmode='day', date_pattern='yyyy-mm-dd', background='green')  # Set the date format
    end_date.pack(pady=10)

    # Create a style for the button
    style = ttk.Style()
    style.configure(
        "Big.TButton",  # Custom style name
        font=("Helvetica", 20),  # Larger font size
        padding=10  # Extra padding to make the button bigger
    )
    submit_button = ttk.Button(date_window, text="Show Team Performance!", style="Big.TButton",
                               command=show_competition_results)
    submit_button.pack(pady=20)

    #date_window.mainloop()


def plot_competitive_nutrient_comparison(results, winners_results, parent_window):
    # Clear existing content in parent window
    for widget in parent_window.winfo_children():
        widget.destroy()

    # Add a title
    tk.Label(
        parent_window,
        text=f"Team Performance",
        font=("Helvetica", 10),
        bg="#f7f9fc"
    ).pack(pady=10)

    # Display winners' information
    winner_text = "Winners!!! " + ", ".join([f"{row[1]} ({row[0]})" for row in winners_results])
    tk.Label(
        parent_window,
        text=winner_text,
        font=("Helvetica", 20),
        bg="#f7f9fc",
        fg="#ed0070"  # Use a distinct color for the winners
    ).pack(pady=10)
    #parent_window.geometry("3000x8000")  # Adjust the size of the window
    parent_window.attributes('-fullscreen', True)

    # Unpack data
    user_ids = [row[0] for row in results]  # Extract user IDs
    avg_gaps = np.array([row[1:] for row in results])  # Extract nutrient gaps

    nutrients = ['Vitamin A', 'Vitamin C', 'Vitamin D', 'Vitamin E', 'Vitamin K', 'Thiamin', 'Riboflavin', 'Niacin', 'Vitamin B6', 'Vitamin B12', 'Pantothenic acid']
    x = np.arange(len(nutrients))  # X-axis positions for nutrients
    width = 0.2  # Width of each bar
    offsets = np.arange(-len(user_ids) // 2 * width, len(user_ids) // 2 * width, width)

    # Plot
    fig, ax = plt.subplots(figsize=(40, 6))
    for i, user_id in enumerate(user_ids):
        ax.bar(x + offsets[i], avg_gaps[i], width, label=f'{user_id}')

    # Add labels, title, and legend
    ax.set_xlabel('Nutrients', fontsize=12)
    #ax.set_ylabel('Average Daily Gap (%)', fontsize=12)
    ax.set_ylabel('Average Daily Intake (%)', fontsize=12)
    #ax.set_title('Nutrient Gap Comparison by User: Lower is Better!', fontsize=14, pad=20)
    ax.set_title('Nutrient Intake Comparison by User: Higher is Better!', fontsize=14, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(nutrients)
    ax.legend(title="Users")

    # Annotate values above bars
    for i, user_gap in enumerate(avg_gaps):
        for j, gap in enumerate(user_gap):
            gap = 100 - gap  # Convert gap to intake
            ax.text(j + offsets[i], gap + 1, f'{gap:.1f}%', ha='center', fontsize=8, rotation=45)

    plt.tight_layout()

    # Embed the matplotlib figure into the Tkinter UI
    canvas = FigureCanvasTkAgg(fig, master=parent_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
    canvas.draw()

    def on_close():
        plt.close(fig)
        parent_window.destroy()
    # Add a "Close" button
    ttk.Button(
        parent_window,
        text="Close",
        command=on_close
    ).pack(pady=3)
    parent_window.protocol("WM_DELETE_WINDOW", on_close)


# Open the main menu
def open_main_menu():
    shared.root.destroy()
    main_menu = tk.Tk()
    main_menu.title("Nutrition Tracker - Main Menu")
    main_menu.geometry("600x800")
    main_menu.configure(bg="#eaf4fc")

    tk.Label(main_menu, text="Welcome to Nutrition Tracker!", font=("Helvetica", 18), bg="#eaf4fc").pack(pady=30)

    button_style = ttk.Style()
    button_style.configure("TButton", font=("Helvetica", 12), padding=5)

    ttk.Button(main_menu, text="View Daily Gap", command=daily_gap_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="Deficiencies From Blood Test", command=blood_test, width=25).pack(pady=10)
    ttk.Button(main_menu, text="Insert Eaten Food", command=insert_eaten_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="View Statistics", command=statistics_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="Track Trends", command=trends_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="Team Comparison", command=comparison_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="Join Team", command=join_team_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="Leave Team", command=leave_team_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="Show My Teams", command=show_teams, width=25).pack(pady=10)
    ttk.Button(main_menu, text="Create New Team", command=create_team_window, width=25).pack(pady=10)

    # Close window event handler to terminate the program
    # def on_closing():
    #     try:
    #         shared.root.quit()  # Exit the Tkinter main loop
    #         shared.root.quit()
    #         shared.root.quit()
    #         shared.root.quit()
    #         shared.root.quit()
    #         shared.root.quit()
    #         shared.root.quit()
    #         shared.root.quit()
    #     except Exception as e:
    #         print(f"Error during closing: {e}")
    #     # finally:
    #     #     sys.exit(0)  # Ensure the program fully terminates
    #
    # main_menu.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window close (X) event
    #main_menu.mainloop()

