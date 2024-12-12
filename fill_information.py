import pymysql
import pandas as pd

def connect_to_db():
    try:
        # Database connection details
        host = 'localhost'
        user = 'root'
        password = 'shachar100'
        database = 'food_recommandation'
        # Connect to the database
        connection = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        print("Error connecting to the database:", e)
        return None, None

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
        print("An error occurred in life_stage_group_load:", e)
        connection.rollback()

def insert_teams(connection, cursor):
    try:
        groups = ['Microsoft', 'Google', 'Amazon', 'Facebook', 'Apple', 'AngelmanFamily', 'BacharFamily', 'CohenFamily']
        insert_query = "INSERT INTO team (team_name) VALUES (%s)"
        cursor.executemany(insert_query, [(group,) for group in groups])
        connection.commit()
        print(f"{len(groups)} groups inserted successfully.")
    except Exception as e:
        print("An error occurred in insert_teams:", e)
        connection.rollback()

def create_users(connection, cursor):
    try:
        data = [
            [100000001, 'Male', 0.8, 'Infants', 'Alice_M', 7.2, 68, 'Sedentary'],
            # Other rows...
        ]
        df = pd.DataFrame(data, columns=['user_id', 'gender', 'age', 'subgroup', 'username', 'weight', 'height',
                                         'activity_level'])
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
    except Exception as e:
        print("An error occurred in create_users:", e)
        connection.rollback()

def insert_belong_teams(connection, cursor):
    try:
        groups = [
            (1, 100000001), (1, 100000002), (1, 100000003), (2, 100000004), (2, 100000006),
            (3, 100000007)
        ]
        insert_query = "INSERT INTO belong_team (team_id, user_id) VALUES (%s, %s)"
        for team_id, user_id in groups:
            cursor.execute(insert_query, (team_id, user_id))
        connection.commit()
        print("Users assigned to groups successfully")
    except Exception as e:
        print("An error occurred in insert_belong_teams:", e)
        connection.rollback()

def load_food_data_big(connection, cursor):
    try:
        food_data_big_csv = 'FoodDataBig.csv'
        df_big = pd.read_csv(food_data_big_csv)
        df_big.loc[df_big['name'].isna(), 'name'] = None
        insert_query = "INSERT IGNORE INTO food (food_name, Caloric_Value_kcal, Protein_g, Dietary_Fiber_g, Cholesterol_mg, Sodium_g, Water_g) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        for index, row in df_big.iterrows():
            cursor.execute(insert_query, (
                row['name'], row['Energy'], row['Protein'], row['Fiber, total dietary'], row['Cholesterol'], row['Sodium, Na'], row['Water']))
        connection.commit()
        print("Food data big inserted successfully.")
    except Exception as e:
        print("An error occurred in load_food_data_big:", e)
        connection.rollback()

def fill_information():
    try:
        connection, cursor = connect_to_db()
        if connection is None or cursor is None:
            print("Failed to connect to database.")
            return

        life_stage_group_load(connection, cursor)
        create_users(connection, cursor)
        insert_teams(connection, cursor)
        insert_belong_teams(connection, cursor)
        load_food_data_big(connection, cursor)

        cursor.close()
        connection.close()
    except Exception as e:
        print("An error occurred in fill_information:", e)

if __name__ == '__main__':
    try:
        import os
        os.chdir(r'C:\Users\kashann\PycharmProjects\NutriTrack')
        fill_information()
    except Exception as e:
        print("An error occurred in the main block:", e)
