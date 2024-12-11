import pymysql
import pandas as pd
def connect_to_db():
    # Database connection details
    host = 'localhost'
    user = 'root'
    password = 'Nn021099!'
    database = 'food_recommandation'
    # Connect to the database
    connection = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = connection.cursor()
    return connection, cursor

def life_stage_group_load(connection, cursor):
    try:
        csv_file_path = 'life_stage_group.csv'
        df_life_stage = pd.read_csv(csv_file_path)
        df_life_stage['min_age'] = df_life_stage['min_age'].astype(int)
        df_life_stage['max_age'] = df_life_stage['max_age'].astype(int)

        # Convert vitamin columns to DECIMAL(4,4), i.e., round to 4 decimal places
        vitamin_columns = [
            'Vitamin_A_mg', 'Vitamin_C_mg', 'Vitamin_D_mg', 'Vitamin_E_mg', 'Vitamin_K_mg',
            'Thiamin_mg', 'Riboflavin_mg', 'Niacin_mg', 'Vitamin_B6_mg', 'Vitamin_B12_mg', 'Pantothenic_acid_mg'
        ]

        for column in vitamin_columns:
            df_life_stage[column] = df_life_stage[column].apply(lambda x: round(x, 4))

        insert_query = """
            INSERT INTO life_stage_group_daily_recommand 
            (gender, subgroup, min_age, max_age, Vitamin_A_mg, Vitamin_C_mg, Vitamin_D_mg, Vitamin_E_mg, Vitamin_K_mg, 
            Thiamin_mg, Riboflavin_mg, Niacin_mg, Vitamin_B6_mg, Vitamin_B12_mg, Pantothenic_acid_mg) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        for index, row in df_life_stage.iterrows():
            cursor.execute(insert_query, (row['gender'],
                                          row['subgroup'], row['min_age'], row['max_age'], row['Vitamin_A_mg'],
                                          row['Vitamin_C_mg'], row['Vitamin_D_mg'],
                                          row['Vitamin_E_mg'], row['Vitamin_K_mg'], row['Thiamin_mg'],
                                          row['Riboflavin_mg'], row['Niacin_mg'],
                                          row['Vitamin_B6_mg'], row['Vitamin_B12_mg'], row['Pantothenic_acid_mg']
                                          ))
        # Commit the changes
        connection.commit()
        print("life_stage_group_load inserted successfully.")
    except Exception as e:
        print("An error occurred:", e)
        connection.rollback()  # Rollback in case of error

def insert_teams(connection, cursor):
    groups = ['Microsoft', 'Google', 'Amazon', 'Facebook', 'Apple', 'AngelmanFamily', 'BacharFamily', 'CohenFamily']
    # Prepare the SQL query with placeholders
    insert_query = "INSERT INTO team (team_name) VALUES (%s)"
    try:
        # Use executemany to insert multiple rows efficiently
        cursor.executemany(insert_query, [(group,) for group in groups])
        connection.commit()
        print(f"{len(groups)} groups inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_users(connection, cursor):
    data = [
        [100000001, 'Male', 0.8, 'Infants', 'Alice_M', 7.2, 68, 'Sedentary'],
        [100000002, 'Female', 4, 'Children', 'Sophia_F', 18, 105, 'Lightly active'],
        [100000003, 'Male', 11, 'Adult', 'Liam_M', 55, 155, 'Moderately active'],
        [100000004, 'Female', 28, 'Pregnancy', 'Emma_F', 68, 162, 'Lightly active'],
        [100000006, 'Female', 6, 'Children', 'Isabella_F', 23, 120, 'Moderately active'],
        [100000007, 'Male', 13, 'Adult', 'Elijah_M', 60, 160, 'Lightly active'],
        [100000009, 'Female', 19, 'Pregnancy', 'Olivia_F', 75, 170, 'Extra active'],
        [100000010, 'Male', 5, 'Children', 'William_M', 22, 110, 'Sedentary'],
        [100000011, 'Male', 10, 'Adult', 'Benjamin_M', 45, 150, 'Moderately active'],
        [100000012, 'Female', 18, 'Lactation', 'Charlotte_F', 60, 165, 'Very active'],
        [100000013, 'Male', 4, 'Children', 'Henry_M', 18, 105, 'Sedentary'],
        [100000014, 'Female', 33, 'Pregnancy', 'Mia_F', 72, 160, 'Moderately active'],
        [100000015, 'Male', 7, 'Children', 'Alexander_M', 24, 115, 'Lightly active'],
        [100000016, 'Female', 15, 'Adult', 'Amelia_F', 55, 160, 'Very active'],
        [100000017, 'Male', 0.6, 'Infants', 'Lucas_M', 6.5, 66, 'Sedentary'],
        [100000018, 'Male', 30, 'Adult', 'Ethan_M', 70, 175, 'Very active'],
        [100000019, 'Female', 35, 'Adult', 'Ava_F', 72, 168, 'Lightly active'],
        [100000020, 'Male', 40, 'Adult', 'Jackson_M', 78, 180, 'Moderately active'],
        [100000021, 'Female', 45, 'Adult', 'Harper_F', 80, 170, 'Very active'],
        [100000022, 'Male', 50, 'Adult', 'Logan_M', 85, 185, 'Sedentary'],
        [100000023, 'Female', 25, 'Adult', 'Sophia_F', 65, 160, 'Extra active'],
        [100000024, 'Male', 38, 'Adult', 'Mason_M', 76, 177, 'Lightly active'],
        [100000025, 'Female', 22, 'Adult', 'Isabella_F', 62, 165, 'Moderately active'],
        [100000026, 'Male', 29, 'Adult', 'Sebastian_M', 68, 174, 'Very active'],
        [100000027, 'Male', 27, 'Adult', 'Lucas_M', 68, 173, 'Lightly active'],
        [100000028, 'Female', 32, 'Adult', 'Ella_F', 72, 165, 'Moderately active'],
        [100000029, 'Male', 41, 'Adult', 'Aiden_M', 80, 178, 'Very active'],
        [100000030, 'Female', 24, 'Adult', 'Emily_F', 63, 160, 'Lightly active'],
        [100000031, 'Male', 39, 'Adult', 'Nathan_M', 75, 177, 'Moderately active'],
        [100000032, 'Female', 29, 'Adult', 'Grace_F', 70, 167, 'Very active'],
        [100000033, 'Male', 36, 'Adult', 'Samuel_M', 78, 182, 'Sedentary'],
        [100000034, 'Female', 48, 'Adult', 'Hannah_F', 79, 170, 'Lightly active'],
        [100000035, 'Male', 33, 'Adult', 'Carter_M', 73, 175, 'Extra active'],
        [100000036, 'Female', 26, 'Adult', 'Victoria_F', 68, 163, 'Moderately active'],
        [100000037, 'Male', 50, 'Adult', 'Owen_M', 82, 180, 'Sedentary'],
        [100000038, 'Female', 44, 'Adult', 'Zoe_F', 77, 168, 'Moderately active'],
        [100000039, 'Male', 31, 'Adult', 'Leo_M', 69, 174, 'Lightly active'],
        [100000040, 'Female', 55, 'Adult', 'Lily_F', 74, 165, 'Very active'],
        [100000041, 'Male', 42, 'Adult', 'John_M', 76, 179, 'Moderately active'],
        [100000042, 'Female', 37, 'Adult', 'Scarlett_F', 71, 162, 'Very active'],
        [100000043, 'Male', 30, 'Adult', 'Isaac_M', 70, 172, 'Moderately active'],
        [100000044, 'Female', 23, 'Adult', 'Evelyn_F', 64, 160, 'Sedentary'],
        [100000045, 'Male', 47, 'Adult', 'Henry_M', 85, 185, 'Lightly active']
    ]
    # Creating a DataFrame
    df = pd.DataFrame(data, columns=['user_id', 'gender', 'age', 'subgroup', 'username', 'weight', 'height',
                                     'activity_level'])
    # Iterate over the DataFrame and execute the insert query for each row
    insert_query = """
    INSERT INTO user_profile (user_id, gender, age, subgroup, username, min_age, max_age, weight, height, activity_level)
    SELECT
        %s AS user_id,
        %s AS gender,
        %s AS age,
        %s AS subgroup,
        %s AS username,
        lsgr.min_age,
        lsgr.max_age,
        %s AS weight,
        %s AS height,
        %s AS activity_level
    FROM
        life_stage_group_daily_recommand lsgr
    WHERE
        lsgr.subgroup = %s AND lsgr.gender = %s
        AND %s BETWEEN lsgr.min_age AND lsgr.max_age
    """

    for index, row in df.iterrows():
        cursor.execute(insert_query, (
        row['user_id'], row['gender'], row['age'], row['subgroup'], row['username'], row['weight'], row['height'],
        row['activity_level'], row['subgroup'], row['gender'], row['age']))

    connection.commit()
    print("Users created successfully")




def insert_belong_teams(connection, cursor):
    groups = [
        (1, 100000001), (1, 100000002), (1, 100000003), (2, 100000004), (2, 100000006),
        (3, 100000007)
    ]
    # Prepare the SQL query with placeholders
    insert_query = "INSERT INTO belong_team (team_id, user_id) VALUES (%s, %s)"
    # Iterate over the groups and execute the insert query
    for team_id, user_id in groups:
        cursor.execute(insert_query, (team_id, user_id))
        connection.commit()

    print("Users assigned to groups successfully")




def load_food_data_big(connection, cursor):
    food_data_big_csv = 'FoodDataBig.csv'
    try:
        # Step 1: Load and preprocess CSV 1
        df_big = pd.read_csv(food_data_big_csv)

        # Step 2: Handle missing values - Replace 'NaN' with None
        df_big.loc[df_big['name'].isna(), 'name'] = None

        # Step 3: Insert data row by row
        insert_query = "INSERT IGNORE INTO food (food_name, Caloric_Value_kcal, Protein_g, Dietary_Fiber_g, Cholesterol_mg, Sodium_g" \
                    ", Water_g, Vitamin_A_mg, Thiamin_mg, Folic_acid_mg, Vitamin_B12_mg, Riboflavin_mg, Niacin_mg, Pantothenic_acid_mg" \
                    ", Vitamin_B6_mg, Vitamin_C_mg, Vitamin_D_mg, Vitamin_E_mg, Vitamin_K_mg, Calcium_mg, Copper_mg, Iron_mg" \
                    ", Magnesium_mg, Manganese_mg, Phosphorus_mg, Potassium_mg, Selenium_mg, Zinc_mg) VALUES (%s, %s," \
                    " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for index, row in df_big.iterrows():
            cursor.execute(insert_query, (
                row['name'], row['Energy'], row['Protein'], row['Fiber, total dietary'], row['Cholesterol'], row['Sodium, Na'], row['Water'],
                row['Vitamin A, RAE'], row['Thiamin'], row['Folic acid'], row['Vitamin B-12'], row['Riboflavin'], row['Niacin'],
                row['Pantothenic acid'], row['Vitamin B-12'], row['Vitamin C, total ascorbic acid'], row['Vitamin D (D2 + D3)'], row['Vitamin E'],
                row['Vitamin K (phylloquinone)'], row['Calcium, Ca'], row['Copper, Cu'], row['Iron, Fe'], row['Magnesium, Mg'], row['Manganese, Mn'],
                row['Phosphorus, P'], row['Potassium, K'], row['Selenium, Se'], row['Zinc, Zn']
            ))

        # Commit the changes
        connection.commit()
        print("Data inserted successfully.")
        # Step 4: Delete rows with NULL in the 'food_name' column
        delete_query = "DELETE FROM food WHERE food_name IS NULL;"
        cursor.execute(delete_query)
        connection.commit()
        print("Rows with NULL food_name deleted successfully.")
    except Exception as e:
        print("An error occurred:", e)
        connection.rollback()  # Rollback in case of error




def convert_scale(connection, cursor):
    # convert the scale of the food data from g to the appropriate measure according to the column name in the table
    # Database connection details
    # Define a dictionary for the conversion scale based on column names
    conversion_factors = {
        'Caloric_Value_kcal' : 0.239006, # KJ to kcal
        'Cholesterol_mg': 1000,  # g to mg
        'Calcium_mg': 1000,       # g to mg
        'Magnesium_mg': 1000,     # g to mg
        'Potassium_mg': 1000,     # g to mg
        'Vitamin_A_mg': 1000,     # µg to mg
        'Thiamin_mg': 1000,       # µg to mg
        'Folic_acid_mg': 1000,    # µg to mg
        'Vitamin_B12_mg': 1000,   # µg to mg
        'Riboflavin_mg': 1000,    # µg to mg
        'Niacin_mg': 1000,        # µg to mg
        'Pantothenic_acid_mg': 1000,  # µg to mg
        'Vitamin_B6_mg': 1000,    # µg to mg
        'Vitamin_C_mg': 1000,     # µg to mg
        'Vitamin_D_mg': 1000,     # µg to mg
        'Vitamin_E_mg': 1000,     # µg to mg
        'Vitamin_K_mg': 1000,     # µg to mg
        'Copper_mg': 1000,        # µg to mg
        'Iron_mg': 1000,          # µg to mg
        'Manganese_mg': 1000,     # µg to mg
        'Phosphorus_mg': 1000,    # µg to mg
        'Selenium_mg': 1000,      # µg to mg
        'Zinc_mg': 1000           # µg to mg
    }

    # Loop over the columns and apply the conversion factor where applicable
    for column, factor in conversion_factors.items():
        # Update the table with converted values (multiply by the conversion factor)
        update_query = f"""
        UPDATE food
        SET {column} = {column} * {factor}
        """
        cursor.execute(update_query)

    # Commit the changes to the database
    connection.commit()
    print("Data scale conversion completed successfully.")

def load_food_data_small(connection, cursor):
    food_data_small_csv = 'FoodDataSmall.csv'
    try:
        # Load and preprocess CSV 2
        df_small = pd.read_csv(food_data_small_csv)

        # Convert all numeric columns to numeric type, invalid parsing will be set as NaN
        numeric_columns = [
            'Caloric Value', 'Protein', 'Dietary Fiber', 'Cholesterol', 'Sodium', 'Water', 'Vitamin A',
            'Vitamin B1', 'Vitamin B11', 'Vitamin B12', 'Vitamin B2', 'Vitamin B3', 'Vitamin B5', 'Vitamin B6',
            'Vitamin C', 'Vitamin D', 'Vitamin E', 'Vitamin K', 'Calcium', 'Copper', 'Iron', 'Magnesium',
            'Manganese', 'Phosphorus', 'Potassium', 'Selenium', 'Zinc'
        ]

        # # Ensure that these columns are converted to float, coercing errors to NaN
        # df_small[numeric_columns] = df_small[numeric_columns].apply(pd.to_numeric, errors='coerce')

        # Round all float values to 6 decimal places to avoid scientific notation
        #df_small[numeric_columns] = df_small[numeric_columns].round(6)

        # # Step 3: Handle missing values - Replace 'NaN' with None
        # df_big.loc[df_big['name'].isna(), 'name'] = None

        # Step 4: Insert data row by row
        insert_query = """
            INSERT IGNORE INTO food (
                food_name, Caloric_Value_kcal, Protein_g, Dietary_Fiber_g, Cholesterol_mg, Sodium_g, Water_g, Vitamin_A_mg,
                Thiamin_mg, Folic_acid_mg, Vitamin_B12_mg, Riboflavin_mg, Niacin_mg, Pantothenic_acid_mg, Vitamin_B6_mg,
                Vitamin_C_mg, Vitamin_D_mg, Vitamin_E_mg, Vitamin_K_mg, Calcium_mg, Copper_mg, Iron_mg, Magnesium_mg,
                Manganese_mg, Phosphorus_mg, Potassium_mg, Selenium_mg, Zinc_mg
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Iterate over each row in the dataframe and insert into the table
        for index, row in df_small.iterrows():
            cursor.execute(insert_query, (
                row['food'], row['Caloric Value'], row['Protein'], row['Dietary Fiber'],
                row['Cholesterol'],
                row['Sodium'], row['Water'], row['Vitamin A'], row['Vitamin B1'], row['Vitamin B11'],
                row['Vitamin B12'],
                row['Vitamin B2'], row['Vitamin B3'], row['Vitamin B5'], row['Vitamin B6'],
                row['Vitamin C'],
                row['Vitamin D'], row['Vitamin E'], row['Vitamin K'], row['Calcium'], row['Copper'],
                row['Iron'],
                row['Magnesium'], row['Manganese'], row['Phosphorus'], row['Potassium'], row['Selenium'],
                row['Zinc']
            ))

        # Commit the changes
        connection.commit()
        print("Data small inserted successfully.")
    except Exception as e:
        print("An error occurred:", e)
        connection.rollback()  # Rollback in case of error

def fill_information():
    connection, cursor = connect_to_db()
    life_stage_group_load(connection, cursor)
    create_users(connection, cursor)
    insert_teams(connection, cursor)
    insert_belong_teams(connection, cursor)
    load_food_data_big(connection, cursor)
    convert_scale(connection, cursor)
    load_food_data_small(connection, cursor)
    cursor.close()
    connection.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import os
    os.chdir(r'C:\Users\kashann\PycharmProjects\NutriTrack')
    fill_information()


