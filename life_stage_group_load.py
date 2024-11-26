import pandas as pd
import pymysql

# Database connection details
host = 'localhost'
user = 'root'
password = 'Nn021099!'
database = 'food_recommandation'

# Connect to the database
connection = pymysql.connect(host=host, user=user, password=password, database=database)
cursor = connection.cursor()

try:
    csv_file_path = r'C:\Users\kashann\PycharmProjects\NutriTrack\life_stage_group.csv'
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
        row['subgroup'], row['min_age'], row['max_age'], row['Vitamin_A_mg'], row['Vitamin_C_mg'], row['Vitamin_D_mg'],
        row['Vitamin_E_mg'], row['Vitamin_K_mg'], row['Thiamin_mg'], row['Riboflavin_mg'], row['Niacin_mg'],
        row['Vitamin_B6_mg'], row['Vitamin_B12_mg'], row['Pantothenic_acid_mg']
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


