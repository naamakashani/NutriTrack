import pandas as pd
import pymysql

# Database connection details
host = 'localhost'
user = 'root'
password = 'shachar100'
database = 'food_recommandation'

# Paths to your CSV files
food_data_big_csv = 'path_to_first_file.csv'
food_data_small_csv = 'path_to_second_file.csv'

# Connect to the database
connection = pymysql.connect(host=host, user=user, password=password, database=database)
cursor = connection.cursor()

try:
    # Step 1: Load and preprocess CSV 1
    df_big = pd.read_csv(food_data_big_csv)

    # Step 2: Load and preprocess CSV 2
    df_small = pd.read_csv(food_data_small_csv)

    # Step 4: Insert data row by row
    insert_query = "INSERT INTO food (food_name, Caloric_Value_kcal, Protein_g, Dietary_Fiber_g, Cholesterol_mg, Sodium_g" \
                   ", Water_g, Vitamin_A, Thiamin_mg, Folic_acid_mg, Vitamin_B12_mg, Riboflavin_mg, Niacin_mg, Pantothenic_acid_mg" \
                   ", Vitamin_B6_mg, Vitamin_C_mg, Vitamin_D_mg, Vitamin_E_mg, Vitamin_K_mg, Calcium_mg, Copper_mg, Iron_mg" \
                   ", Magnesium_mg, Manganese_mg, Phosphorus_mg, , Potassium_mg, Selenium_mg, Zinc_mg) VALUES (%s, %s)"
    for index, row in df_big.iterrows():
        cursor.execute(insert_query, (
            row['name'], row['Energy'], row['Protein'], row['Fiber, total dietary'], row['Cholesterol'], row['Sodium, Na'], row['Water'],
            row['Vitamin A, RAE'], row['Thiamin'], row['Folic acid'], row['Vitamin B-12'], row['Riboflavin'], row['Niacin'],
            row['Pantothenic acid'], row['Vitamin B-12'], row['Vitamin C, total ascorbic acid'], row['Vitamin D (D2 + D3)'], row['Vitamin E'],
            row['Vitamin K'], row['Calcium'], row['Copper'], row['Iron'], row['Magnesium'], row['Manganese'],
            row['Phosphorus, P'], row['Potassium, K'], row['Selenium, Se'], row['Zinc, Zn']
        ))

    # Commit the changes
    connection.commit()
    print("Data inserted successfully.")
except Exception as e:
    print("An error occurred:", e)
    connection.rollback()  # Rollback in case of error
finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()
