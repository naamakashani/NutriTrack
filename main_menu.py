import tkinter as tk
from datetime import datetime
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
    new_window.geometry("500x500")  # Adjust size as needed

    # Get recommendations
    recommendations = recommand_food_for_nutrient(
        nutrient_name)  # Assuming this function returns a list of foods or text

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
        text="Excess values are in black, deficiencies are in red.",
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
        date = date_entry.get()

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
        # check that the date is valid format
        if not is_valid_date(date):
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return
        # check that the amount is valid number
        if not amount.isdigit():
            messagebox.showerror("Error", "Amount should be a number!")
            return
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
                bg="gray",  # Green for deficiency buttons
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
            text="Weekly Averages",
            command=lambda: show_avg(7),
            font=("Helvetica", 10),
            bg="#4caf50",
            fg="white",
            padx=10,
            pady=5
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="Monthly Averages",
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
    root = tk.Tk()
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
        checkbox = tk.Checkbutton(inner_frame, text=team_name, variable=var, command=lambda t=team_name, i=team_id: toggle_team(t, i))
        checkbox.pack(anchor="w", padx=5, pady=2)

    # Update the scroll region
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    inner_frame.bind("<Configure>", on_frame_configure)

    # Submit button
    submit_button = tk.Button(root, text="Submit", command=lambda: submit_selected_teams(selected_teams), bg="green", fg="white", font=("Helvetica", 12, "bold"))
    submit_button.pack(pady=10)

    # Run the main loop
    root.mainloop()



def show_teams():
    # Simulate a user ID (replace with actual user ID logic)
    user_id = shared.user_id
    teams = get_teams_for_user(user_id)

    if not teams:
        messagebox.showinfo("My Teams", "You are not part of any team.")
        return

    # Create the main window
    root = tk.Tk()
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
    root.mainloop()


def trends_window():
    messagebox.showinfo("Trends", "Trends feature is under development.")


def comparison_window():
    messagebox.showinfo("Comparison", "Team Comparison feature is under development.")


# Open the main menu
def open_main_menu():
    main_menu = tk.Tk()
    main_menu.title("Nutrition Tracker - Main Menu")
    main_menu.geometry("800x600")
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
    ttk.Button(main_menu, text="Join Team", command=join_team_window, width=25).pack(pady=10)
    ttk.Button(main_menu, text="Show my teams", command=show_teams, width=25).pack(pady=10)

    main_menu.mainloop()
