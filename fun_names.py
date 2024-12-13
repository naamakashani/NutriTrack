import pymysql
from collections import defaultdict
import re
from tkinter import messagebox

import shared


def connect_to_db():
    # Database connection details
    host = 'localhost'
    user = 'root'
    password = 'Nn021099!'
    database = 'food_recommandation'

    try:
        # Connect to the database
        connection = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = connection.cursor()
        return connection, cursor
    except pymysql.MySQLError as e:
        messagebox.showerror("Error", "Connection to server failed.")
        print(f"Error connecting to database: {e}")
        raise  # Re-raise the exception after logging


def check_user_exists(user_id):
    # Check if a user with the given user_id exists in the user_profile table
    connection, cursor = connect_to_db()

    # Prepare the SQL query
    select_query = "SELECT COUNT(*) FROM user_profile WHERE user_id = %s"

    try:
        # Execute the query with the provided user_id
        cursor.execute(select_query, (user_id,))
        result = cursor.fetchone()
        return result[0]

    except pymysql.MySQLError as e:
        # Handle exceptions (log the error or re-raise as needed)
        print(f"Error checking user existence: {e}")
        return False

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


def insert_user(user_id, gender, age, subgroup, username, weight, height, activity_level):
    # Insert a new user into the user_profile table
    connection, cursor = connect_to_db()

    # SQL query to insert data into user_profile
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

    try:
        # Execute the query with the appropriate parameters
        cursor.execute(insert_query,
                       (
                           user_id, gender, age, subgroup, username, weight, height, activity_level, subgroup, gender,
                           age))

        # Commit the transaction to save changes
        connection.commit()

    except pymysql.MySQLError as e:
        # Handle exceptions (log the error or re-raise as needed)
        print(f"Error inserting into user_profile table: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


def insert_eaten(food, amount, user_id, date_of_eat):
    # Connect to the database
    connection, cursor = connect_to_db()
    try:
        # Normalize the input food string: trim spaces, convert to lowercase
        food = re.sub(r'\s+', ' ', food.strip().lower())

        # Find the exact food name in the food table (case-insensitive exact match)
        select_query = "SELECT food_name FROM food WHERE LOWER(food_name) = %s"
        cursor.execute(select_query, (food,))  # No need for '%' wildcards for exact match
        result = cursor.fetchone()

        if result:
            # Food exists; insert the eaten food into the `eat` table
            food_name = result[0]
            insert_query = """
                INSERT INTO eat (food_name, amount, user_id, date_of_eat)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (food_name, amount, user_id, date_of_eat))
            connection.commit()
            cursor.close()
            connection.close()
            return 1
        else:
            # Food does not exist
            cursor.close()
            connection.close()
            return 0
    except Exception as e:
        connection.rollback()
        return 0


def create_new_team(team_name):
    # Create a new team
    connection, cursor = connect_to_db()
    check_query = "SELECT COUNT(*) FROM team WHERE team_name = %s"
    insert_query = "INSERT INTO team (team_name) VALUES (%s)"
    flag = 1
    try:
        # Check if the team already exists
        cursor.execute(check_query, (team_name,))
        result = cursor.fetchone()
        if result[0] > 0:
            print("Team already exists.")
            flag = 0

        # Insert the new team if it doesn't exist
        cursor.execute(insert_query, (team_name,))  # Ensure that team_name is passed as a tuple

        # Commit the transaction to save changes
        connection.commit()
        print("Team created successfully.")

    except pymysql.MySQLError as e:
        # Handle exceptions (log the error or re-raise as needed)
        print(f"Error inserting into team table: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()
        return flag


def get_all_teams():
    # Show all teams
    connection, cursor = connect_to_db()
    select_query = "SELECT team_id, team_name FROM team"

    try:
        cursor.execute(select_query)
        results = cursor.fetchall()
        return results

    except pymysql.MySQLError as e:
        # Handle exceptions (log the error or re-raise as needed)
        print(f"Error fetching teams: {e}")

    finally:
        cursor.close()
        connection.close()


def user_join_team(user_id, team_id):
    connection, cursor = connect_to_db()
    check_query = "SELECT * FROM belong_team WHERE team_id = %s AND user_id = %s"
    insert_query = "INSERT INTO belong_team (team_id, user_id) VALUES (%s, %s)"
    already_in_group = False

    try:
        # Check if the user is already in the team
        cursor.execute(check_query, (team_id, user_id))
        if cursor.fetchone():
            already_in_group = True
        else:
            # Insert the user into the team
            cursor.execute(insert_query, (team_id, user_id))
            connection.commit()  # Commit after each insert
    except pymysql.MySQLError as e:
        # Handle exceptions
        messagebox.showerror("Database Error", f"Error joining team: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

    return not already_in_group  # Return False if the user is already in the group


def get_teams_for_user(user_id):
    # Get all teams that the user is a part of
    connection, cursor = connect_to_db()
    select_query = "SELECT team_id, team_name FROM team WHERE team_id IN (SELECT team_id FROM belong_team WHERE user_id = %s)"

    try:
        cursor.execute(select_query, (user_id,))
        results = cursor.fetchall()
        return results

    except pymysql.MySQLError as e:
        # Handle exceptions (log the error or re-raise as needed)
        print(f"Error fetching teams for user: {e}")

    finally:
        cursor.close()
        connection.close()


def join_team(groups):
    # Prepare the SQL query with placeholders
    insert_query = "INSERT INTO belong_team (team_id, user_id) VALUES (%s, %s)"

    connection, cursor = connect_to_db()

    try:
        # Iterate over the groups and execute the insert query
        for team_id, user_id in groups:
            cursor.execute(insert_query, (team_id, user_id))
            connection.commit()  # Commit after each insert (or you could commit after all)

    except pymysql.MySQLError as e:
        # Handle exceptions (log the error or re-raise as needed)
        print(f"Error inserting into belong_team table: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


def get_daily_gap(user_id, date):
    """
    Calculate the daily gap of the user on the given date.
    Returns a dictionary of nutrient deficiencies and excesses, along with caloric gap.
    """

    try:
        connection, cursor = connect_to_db()
        cursor.execute(""" SELECT
         ROUND(daily.daily_Vitamin_A_mg - recom_user.Vitamin_A_mg, 2),
            ROUND(daily.daily_Vitamin_C_mg - recom_user.Vitamin_C_mg, 2),
            ROUND(daily.daily_Vitamin_D_mg - recom_user.Vitamin_D_mg, 2),
            ROUND(daily.daily_Vitamin_E_mg - recom_user.Vitamin_E_mg, 2),
            ROUND(daily.daily_Vitamin_K_mg - recom_user.Vitamin_K_mg, 2),
            ROUND(daily.daily_Thiamin_mg - recom_user.Thiamin_mg, 2),
            ROUND(daily.daily_Riboflavin_mg - recom_user.Riboflavin_mg, 2),
            ROUND(daily.daily_Niacin_mg - recom_user.Niacin_mg, 2),
            ROUND(daily.daily_Vitamin_B6_mg - recom_user.Vitamin_B6_mg, 2),
            ROUND(daily.daily_Vitamin_B12_mg - recom_user.Vitamin_B12_mg, 2),
            ROUND(daily.daily_Pantothenic_acid_mg - recom_user.Pantothenic_acid_mg, 2),
            ROUND(daily.daily_Caloric_Value_kcal - recom_user.desired_calories, 2)
        FROM (
            SELECT Vitamin_A_mg, Vitamin_C_mg, Vitamin_D_mg, Vitamin_E_mg, Vitamin_K_mg,
                   Thiamin_mg, Riboflavin_mg, Niacin_mg, Vitamin_B6_mg, Vitamin_B12_mg,
                   Pantothenic_acid_mg,user_profile.desired_calories
            FROM life_stage_group_daily_recommand as ls,user_profile           
            WHERE user_profile.user_id = %s AND
            ls.gender=user_profile.gender AND ls.subgroup=user_profile.subgroup AND ls.min_age=user_profile.min_age AND 
            ls.max_age=user_profile.max_age) as recom_user,
        
            (SELECT SUM(eat.amount * food.Vitamin_A_mg / 100) AS daily_Vitamin_A_mg,
                   SUM(eat.amount * food.Vitamin_C_mg / 100) AS daily_Vitamin_C_mg,
                   SUM(eat.amount * food.Vitamin_D_mg / 100) AS daily_Vitamin_D_mg,
                   SUM(eat.amount * food.Vitamin_E_mg / 100) AS daily_Vitamin_E_mg,
                   SUM(eat.amount * food.Vitamin_K_mg / 100) AS daily_Vitamin_K_mg,
                   SUM(eat.amount * food.Thiamin_mg / 100) AS daily_Thiamin_mg,
                   SUM(eat.amount * food.Riboflavin_mg / 100) AS daily_Riboflavin_mg,
                   SUM(eat.amount * food.Niacin_mg / 100) AS daily_Niacin_mg,
                   SUM(eat.amount * food.Vitamin_B6_mg / 100) AS daily_Vitamin_B6_mg,
                   SUM(eat.amount * food.Vitamin_B12_mg / 100) AS daily_Vitamin_B12_mg,
                   SUM(eat.amount * food.Pantothenic_acid_mg / 100) AS daily_Pantothenic_acid_mg,
                   SUM(eat.amount * food.Caloric_Value_kcal / 100) AS daily_Caloric_Value_kcal
            FROM eat
            INNER JOIN food ON eat.food_name = food.food_name
            WHERE eat.user_id = %s AND DATE(eat.date_of_eat) = %s) as daily
                      
        """, (user_id, user_id, date))
        daily_gap = cursor.fetchone()

        # todo : check that it work gor negative gap
        # todo : check that this is good

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        connection.close()

    # if all daily gaps are nan return nan
    if all(v is None for v in daily_gap):
        return None
    return daily_gap


def recommand_food_for_nutrient(nutrient):
    connection, cursor = connect_to_db()
    try:
        # Query top 5 foods based on the nutrient
        query = f"""
                    SELECT food_name
                    FROM food
                    ORDER BY {nutrient} DESC
                    LIMIT 5;
                """
        cursor.execute(query)
        results = cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return results


def avg_consumption(user_id, period):
    connection, cursor = connect_to_db()
    query = """
    SELECT 
ROUND(AVG(e.amount * f.Caloric_Value_kcal / 100), 2) AS Avg_Calories,
ROUND(AVG(e.amount * f.Protein_g / 100), 2) AS Avg_Protein_g,
ROUND(AVG(e.amount * f.Dietary_Fiber_g / 100), 2) AS Avg_Fiber_g,
ROUND(AVG(e.amount * f.Cholesterol_mg / 100), 2) AS Avg_Cholesterol_mg,
ROUND(AVG(e.amount * f.Sodium_g / 100), 2) AS Avg_Sodium_g,
ROUND(AVG(e.amount * f.Water_g / 100), 2) AS Avg_Water_g,
ROUND(AVG(e.amount * f.Vitamin_A_mg / 100), 2) AS Avg_Vitamin_A_mg,
ROUND(AVG(e.amount * f.Thiamin_mg / 100), 2) AS Avg_Thiamin_mg,
ROUND(AVG(e.amount * f.Folic_Acid_mg / 100), 2) AS Avg_Folic_Acid_mg,
ROUND(AVG(e.amount * f.Vitamin_B12_mg / 100), 2) AS Avg_Vitamin_B12_mg,
ROUND(AVG(e.amount * f.Riboflavin_mg / 100), 2) AS Avg_Riboflavin_mg,
ROUND(AVG(e.amount * f.Niacin_mg / 100), 2) AS Avg_Niacin_mg,
ROUND(AVG(e.amount * f.Pantothenic_Acid_mg / 100), 2) AS Avg_Pantothenic_Acid_mg,
ROUND(AVG(e.amount * f.Vitamin_B6_mg / 100), 2) AS Avg_Vitamin_B6_mg,
ROUND(AVG(e.amount * f.Vitamin_C_mg / 100), 2) AS Avg_Vitamin_C_mg,
ROUND(AVG(e.amount * f.Vitamin_D_mg / 100), 2) AS Avg_Vitamin_D_mg,
ROUND(AVG(e.amount * f.Vitamin_E_mg / 100), 2) AS Avg_Vitamin_E_mg,
ROUND(AVG(e.amount * f.Vitamin_K_mg / 100), 2) AS Avg_Vitamin_K_mg,
ROUND(AVG(e.amount * f.Calcium_mg / 100), 2) AS Avg_Calcium_mg,
ROUND(AVG(e.amount * f.Copper_mg / 100), 2) AS Avg_Copper_mg,
ROUND(AVG(e.amount * f.Iron_mg / 100), 2) AS Avg_Iron_mg,
ROUND(AVG(e.amount * f.Magnesium_mg / 100), 2) AS Avg_Magnesium_mg,
ROUND(AVG(e.amount * f.Manganese_mg / 100), 2) AS Avg_Manganese_mg,
ROUND(AVG(e.amount * f.Phosphorus_mg / 100), 2) AS Avg_Phosphorus_mg,
ROUND(AVG(e.amount * f.Potassium_mg / 100), 2) AS Avg_Potassium_mg,
ROUND(AVG(e.amount * f.Selenium_mg / 100), 2) AS Avg_Selenium_mg,
ROUND(AVG(e.amount * f.Zinc_mg / 100), 2) AS Avg_Zinc_mg

        
    FROM 
        eat e
    JOIN 
        food f ON e.food_name = f.food_name
    WHERE 
        e.user_id = %s 
        AND e.date_of_eat >= DATE_SUB(NOW(), INTERVAL %s DAY);
    """
    cursor.execute(query, (user_id, period))
    consumption = cursor.fetchone()
    return consumption


def trends(user_id):
    # return the trends of the user
    return 0;


def comparison_team(team_id):
    # return the comparison of the team
    return 0;
