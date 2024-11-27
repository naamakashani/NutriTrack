import pandas as pd
import pymysql

def load_food_data_big():
    # Load data from CSV file - food data big and insert into the database,
    # delete rows with NULL food_name and duplicate rows

    # Database connection details
    host = 'localhost'
    user = 'root'
    password = 'shachar100'
    database = 'food_recommandation'

    # Paths to your CSV files
    food_data_big_csv = 'FoodDataBig.csv'
    food_data_small_csv = 'FoodDataSmall.csv'

    # Connect to the database
    connection = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = connection.cursor()

    try:
        # Step 1: Load and preprocess CSV 1
        df_big = pd.read_csv(food_data_big_csv)

        # Step 2: Load and preprocess CSV 2
        df_small = pd.read_csv(food_data_small_csv)

        # Step 3: Handle missing values - Replace 'NaN' with None
        df_big.loc[df_big['name'].isna(), 'name'] = None

        # Step 4: Insert data row by row
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
        # Step 5: Delete rows with NULL in the 'food_name' column
        delete_query = "DELETE FROM food WHERE food_name IS NULL;"
        cursor.execute(delete_query)
        connection.commit()
        print("Rows with NULL food_name deleted successfully.")
    except Exception as e:
        print("An error occurred:", e)
        connection.rollback()  # Rollback in case of error
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

def convert_scale():
    # convert the scale of the food data big from g to the appropriate measure according to the column name in the table
    # Database connection details
    host = 'localhost'
    user = 'root'
    password = 'shachar100'
    database = 'food_recommandation'

    # Paths to your CSV files
    food_data_big_csv = 'FoodDataBig.csv'
    food_data_small_csv = 'FoodDataSmall.csv'

    # Connect to the database
    connection = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = connection.cursor()


def convert_scale():
    # convert the scale of the food data from g to the appropriate measure according to the column name in the table
    # Database connection details
    host = 'localhost'
    user = 'root'
    password = 'shachar100'
    database = 'food_recommandation'


    # Connect to the database
    connection = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = connection.cursor()


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

    # Close the database connection
    cursor.close()
    connection.close()

    print("Data scale conversion completed successfully.")

# main
if __name__ == '__main__':
    load_food_data_big()
    convert_scale()
