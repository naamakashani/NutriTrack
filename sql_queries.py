import pymysql
from collections import defaultdict
import re
import shared
from tkinter import messagebox


def connect_to_db():
    # Database connection details
    host = 'localhost'
    user = 'root'
    password = 'shachar100'
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


def get_username_from_id(user_id):
    connection, cursor = connect_to_db()
    select_query = "SELECT username FROM user_profile WHERE user_id = %s"

    try:
        cursor.execute(select_query, (user_id,))
        result = cursor.fetchone()
        return result[0]

    except pymysql.MySQLError as e:
        # Handle exceptions (log the error or re-raise as needed)
        print(f"Error fetching username: {e}")

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
    """

    try:
        connection, cursor = connect_to_db()
        cursor.execute(""" SELECT
    (daily.daily_Vitamin_A_mg - recom_user.Vitamin_A_mg) / NULLIF(recom_user.Vitamin_A_mg, 0) * 100 AS Vitamin_A_gap,
    (daily.daily_Vitamin_C_mg - recom_user.Vitamin_C_mg) / NULLIF(recom_user.Vitamin_C_mg, 0) * 100 AS Vitamin_C_gap,
    (daily.daily_Vitamin_D_mg - recom_user.Vitamin_D_mg) / NULLIF(recom_user.Vitamin_D_mg, 0) * 100 AS Vitamin_D_gap,
    (daily.daily_Vitamin_E_mg - recom_user.Vitamin_E_mg) / NULLIF(recom_user.Vitamin_E_mg, 0) * 100 AS Vitamin_E_gap,
    (daily.daily_Vitamin_K_mg - recom_user.Vitamin_K_mg) / NULLIF(recom_user.Vitamin_K_mg, 0) * 100 AS Vitamin_K_gap,
    (daily.daily_Thiamin_mg - recom_user.Thiamin_mg) / NULLIF(recom_user.Thiamin_mg, 0) * 100 AS Thiamin_gap,
    (daily.daily_Riboflavin_mg - recom_user.Riboflavin_mg) / NULLIF(recom_user.Riboflavin_mg, 0) * 100 AS Riboflavin_gap,
    (daily.daily_Niacin_mg - recom_user.Niacin_mg) / NULLIF(recom_user.Niacin_mg, 0) * 100 AS Niacin_gap,
    (daily.daily_Vitamin_B6_mg - recom_user.Vitamin_B6_mg) / NULLIF(recom_user.Vitamin_B6_mg, 0) * 100 AS Vitamin_B6_gap,
    (daily.daily_Vitamin_B12_mg - recom_user.Vitamin_B12_mg) / NULLIF(recom_user.Vitamin_B12_mg, 0) * 100 AS Vitamin_B12_gap,
    (daily.daily_Pantothenic_acid_mg - recom_user.Pantothenic_acid_mg) / NULLIF(recom_user.Pantothenic_acid_mg, 0) * 100 AS Pantothenic_acid_gap,
    (daily.daily_Caloric_Value_kcal - recom_user.desired_calories) / NULLIF(recom_user.desired_calories, 0) * 100 AS Caloric_gap
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
        # Query top 10 foods based on the nutrient
        query = f"""
                    SELECT food_name
                    FROM food
                    ORDER BY {nutrient} DESC
                    LIMIT 10;
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
        ROUND(AVG(daily_calories), 5) AS Avg_Calories,
        ROUND(AVG(daily_protein), 5) AS Avg_Protein_g,
        ROUND(AVG(daily_fiber), 5) AS Avg_Fiber_g,
        ROUND(AVG(daily_cholesterol), 5) AS Avg_Cholesterol_mg,
        ROUND(AVG(daily_sodium), 5) AS Avg_Sodium_g,
        ROUND(AVG(daily_water), 5) AS Avg_Water_g,
        ROUND(AVG(daily_vitamin_a), 5) AS Avg_Vitamin_A_mg,
        ROUND(AVG(daily_thiamin), 5) AS Avg_Thiamin_mg,
        ROUND(AVG(daily_folic_acid), 5) AS Avg_Folic_Acid_mg,
        ROUND(AVG(daily_vitamin_b12), 5) AS Avg_Vitamin_B12_mg,
        ROUND(AVG(daily_riboflavin), 5) AS Avg_Riboflavin_mg,
        ROUND(AVG(daily_niacin), 5) AS Avg_Niacin_mg,
        ROUND(AVG(daily_pantothenic_acid), 5) AS Avg_Pantothenic_Acid_mg,
        ROUND(AVG(daily_vitamin_b6), 5) AS Avg_Vitamin_B6_mg,
        ROUND(AVG(daily_vitamin_c), 5) AS Avg_Vitamin_C_mg,
        ROUND(AVG(daily_vitamin_d), 5) AS Avg_Vitamin_D_mg,
        ROUND(AVG(daily_vitamin_e), 5) AS Avg_Vitamin_E_mg,
        ROUND(AVG(daily_vitamin_k), 5) AS Avg_Vitamin_K_mg,
        ROUND(AVG(daily_calcium), 5) AS Avg_Calcium_mg,
        ROUND(AVG(daily_copper), 5) AS Avg_Copper_mg,
        ROUND(AVG(daily_iron), 5) AS Avg_Iron_mg,
        ROUND(AVG(daily_magnesium), 5) AS Avg_Magnesium_mg,
        ROUND(AVG(daily_manganese), 5) AS Avg_Manganese_mg,
        ROUND(AVG(daily_phosphorus), 5) AS Avg_Phosphorus_mg,
        ROUND(AVG(daily_potassium), 5) AS Avg_Potassium_mg,
        ROUND(AVG(daily_selenium), 5) AS Avg_Selenium_mg,
        ROUND(AVG(daily_zinc), 5) AS Avg_Zinc_mg

    FROM (
        SELECT 
            SUM(e.amount * f.Caloric_Value_kcal / 100) AS daily_calories,
            SUM(e.amount * f.Protein_g / 100) AS daily_protein,
            SUM(e.amount * f.Dietary_Fiber_g / 100) AS daily_fiber,
            SUM(e.amount * f.Cholesterol_mg / 100) AS daily_cholesterol,
            SUM(e.amount * f.Sodium_g / 100) AS daily_sodium,
            SUM(e.amount * f.Water_g / 100) AS daily_water,
            SUM(e.amount * f.Vitamin_A_mg / 100) AS daily_vitamin_a,
            SUM(e.amount * f.Thiamin_mg / 100) AS daily_thiamin,
            SUM(e.amount * f.Folic_Acid_mg / 100) AS daily_folic_acid,
            SUM(e.amount * f.Vitamin_B12_mg / 100) AS daily_vitamin_b12,
            SUM(e.amount * f.Riboflavin_mg / 100) AS daily_riboflavin,
            SUM(e.amount * f.Niacin_mg / 100) AS daily_niacin,
            SUM(e.amount * f.Pantothenic_Acid_mg / 100) AS daily_pantothenic_acid,
            SUM(e.amount * f.Vitamin_B6_mg / 100) AS daily_vitamin_b6,
            SUM(e.amount * f.Vitamin_C_mg / 100) AS daily_vitamin_c,
            SUM(e.amount * f.Vitamin_D_mg / 100) AS daily_vitamin_d,
            SUM(e.amount * f.Vitamin_E_mg / 100) AS daily_vitamin_e,
            SUM(e.amount * f.Vitamin_K_mg / 100) AS daily_vitamin_k,
            SUM(e.amount * f.Calcium_mg / 100) AS daily_calcium,
            SUM(e.amount * f.Copper_mg / 100) AS daily_copper,
            SUM(e.amount * f.Iron_mg / 100) AS daily_iron,
            SUM(e.amount * f.Magnesium_mg / 100) AS daily_magnesium,
            SUM(e.amount * f.Manganese_mg / 100) AS daily_manganese,
            SUM(e.amount * f.Phosphorus_mg / 100) AS daily_phosphorus,
            SUM(e.amount * f.Potassium_mg / 100) AS daily_potassium,
            SUM(e.amount * f.Selenium_mg / 100) AS daily_selenium,
            SUM(e.amount * f.Zinc_mg / 100) AS daily_zinc
        FROM 
            eat e
        JOIN 
            food f ON e.food_name = f.food_name
        WHERE 
            e.user_id = %s
            AND e.date_of_eat >= DATE_SUB(NOW(), INTERVAL %s DAY)
        GROUP BY 
            DATE(e.date_of_eat)
    ) AS daily_consumption;
    """

    cursor.execute(query, (user_id, period))
    consumption = cursor.fetchone()
    return consumption


def leave_team(user_id, team_id):
    connection, cursor = connect_to_db()
    flag = 1
    try:
        # Query to check if the user is part of the team
        check_query = """
            SELECT COUNT(*) 
            FROM belong_team 
            WHERE user_id = %s AND team_id = %s;
        """
        cursor.execute(check_query, (user_id, team_id))
        result = cursor.fetchone()

        if result[0] == 0:
            print("User is not part of the team.")
            flag = 0

        # If the user is part of the team, proceed to remove them
        delete_query = """
            DELETE FROM belong_team
            WHERE user_id = %s AND team_id = %s;
        """
        cursor.execute(delete_query, (user_id, team_id))
        connection.commit()
        print("User has successfully left the team.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()
        return flag


def leave_team_list_of_users(user_id_list, team_id):
    conn, cursor = connect_to_db()
    remove_query = """
               DELETE FROM belong_team
               WHERE user_id IN %s AND team_id = %s;
           """
    try:
        # cursor.execute(remove_query, (','.join(map(str, user_id_list)), team_id))
        cursor.execute(remove_query, (tuple(f"{user_id}" for user_id in user_id_list), team_id))
        conn.commit()  # Commit the transaction to remove the users
    except Exception as e:
        print(f"Error: {e}")
        flag = 0
    finally:
        cursor.close()
        conn.close()


def trends(user_id, start_date, end_date, nutrient):
    # Construct the query safely
    query = f"""
    SELECT
        AVG(
    CASE
        WHEN (recom_user.{nutrient} - daily.daily_nutrient) / recom_user.{nutrient} * 100 < 0 THEN 0
        ELSE (recom_user.{nutrient} - daily.daily_nutrient) / recom_user.{nutrient} * 100
    END
) AS Avg_Percentage
    FROM 
        (
            SELECT 
                ls.{nutrient}
            FROM 
                life_stage_group_daily_recommand AS ls, user_profile
            WHERE 
                user_profile.user_id = %s 
                AND ls.gender = user_profile.gender 
                AND ls.subgroup = user_profile.subgroup 
                AND ls.min_age = user_profile.min_age 
                AND ls.max_age = user_profile.max_age
        ) AS recom_user,
        (
            SELECT 
                eat.user_id,
                eat.date_of_eat,
                SUM(eat.amount * food.{nutrient} / 100) AS daily_nutrient
            FROM 
                eat
            INNER JOIN 
                food 
            ON 
                eat.food_name = food.food_name
            WHERE 
                eat.user_id = %s
                AND eat.date_of_eat BETWEEN %s AND %s
            GROUP BY 
                eat.date_of_eat
        ) AS daily
    GROUP BY
        WEEK(daily.date_of_eat)
    ORDER BY
        WEEK(daily.date_of_eat);
    """

    # Establish database connection
    try:
        connection, cursor = connect_to_db()
        # Execute the query
        cursor.execute(query, (user_id, user_id, start_date, end_date))
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error occurred: {e}")
        raise
    finally:
        # Ensure resources are cleaned up
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def comparison_team(team_id, start_date, end_date):
    # return for every user the average daily gap for each nutrient
    query = f"""
SELECT
user_profile.username,
AVG(
    CASE
        WHEN (recom_user.Vitamin_A_mg - daily.daily_nutrient_A) / recom_user.Vitamin_A_mg * 100 < 0 THEN 0
        ELSE (recom_user.Vitamin_A_mg - daily.daily_nutrient_A) / recom_user.Vitamin_A_mg * 100
    END
) AS Avg_Percentage_Vitamin_A,
        AVG(
    CASE
        WHEN (recom_user.Vitamin_C_mg - daily.daily_nutrient_C) / recom_user.Vitamin_C_mg * 100 < 0 THEN 0
        ELSE (recom_user.Vitamin_C_mg - daily.daily_nutrient_C) / recom_user.Vitamin_C_mg * 100
    END
) AS Avg_Percentage_Vitamin_C,
AVG(
    CASE
        WHEN (recom_user.Vitamin_D_mg - daily.daily_nutrient_D) / recom_user.Vitamin_D_mg * 100 < 0 THEN 0
        ELSE (recom_user.Vitamin_D_mg - daily.daily_nutrient_D) / recom_user.Vitamin_D_mg * 100
    END
) AS Avg_Percentage_Vitamin_D,
AVG(
    CASE
        WHEN (recom_user.Vitamin_E_mg - daily.daily_nutrient_E) / recom_user.Vitamin_E_mg * 100 < 0 THEN 0
        ELSE (recom_user.Vitamin_E_mg - daily.daily_nutrient_E) / recom_user.Vitamin_E_mg * 100
    END
) AS Avg_Percentage_Vitamin_E,
AVG(
    CASE
        WHEN (recom_user.Vitamin_K_mg - daily.daily_nutrient_K) / recom_user.Vitamin_K_mg * 100 < 0 THEN 0
        ELSE (recom_user.Vitamin_K_mg - daily.daily_nutrient_K) / recom_user.Vitamin_K_mg * 100
    END
) AS Avg_Percentage_Vitamin_K,
AVG(
    CASE
        WHEN (recom_user.Thiamin_mg - daily.daily_nutrient_Thiamin) / recom_user.Thiamin_mg * 100 < 0 THEN 0
        ELSE (recom_user.Thiamin_mg - daily.daily_nutrient_Thiamin) / recom_user.Thiamin_mg * 100
    END
) AS Avg_Percentage_Thiamin,
AVG(
    CASE
        WHEN (recom_user.Riboflavin_mg - daily.daily_nutrient_Riboflavin) / recom_user.Riboflavin_mg * 100 < 0 THEN 0
        ELSE (recom_user.Riboflavin_mg - daily.daily_nutrient_Riboflavin) / recom_user.Riboflavin_mg * 100
    END
) AS Avg_Percentage_Riboflavin,
AVG(
    CASE
        WHEN (recom_user.Niacin_mg - daily.daily_nutrient_Niacin) / recom_user.Niacin_mg * 100 < 0 THEN 0
        ELSE (recom_user.Niacin_mg - daily.daily_nutrient_Niacin) / recom_user.Niacin_mg * 100
    END
) AS Avg_Percentage_Niacin_mg,
AVG(
    CASE
        WHEN (recom_user.Vitamin_B6_mg - daily.daily_nutrient_B6) / recom_user.Vitamin_B6_mg * 100 < 0 THEN 0
        ELSE (recom_user.Vitamin_B6_mg - daily.daily_nutrient_B6) / recom_user.Vitamin_B6_mg * 100
    END
) AS Avg_Percentage_Vitamin_B6,
AVG(
    CASE
        WHEN (recom_user.Vitamin_B12_mg - daily.daily_nutrient_B12) / recom_user.Vitamin_B12_mg * 100 < 0 THEN 0
        ELSE (recom_user.Vitamin_B12_mg - daily.daily_nutrient_B12) / recom_user.Vitamin_B12_mg * 100
    END
) AS Avg_Percentage_Vitamin_B12,
AVG(
    CASE
        WHEN (recom_user.Pantothenic_acid_mg - daily.daily_nutrient_Pantothenic_acid) / recom_user.Pantothenic_acid_mg * 100 < 0 THEN 0
        ELSE (recom_user.Pantothenic_acid_mg - daily.daily_nutrient_Pantothenic_acid) / recom_user.Pantothenic_acid_mg * 100
    END
) AS Avg_Percentage_Pantothenic_acid
    FROM 
        (
            SELECT 
                user_profile.user_id, ls.Vitamin_A_mg, ls.Vitamin_C_mg, ls.Vitamin_D_mg, ls.Vitamin_K_mg, ls.Vitamin_E_mg, ls.Thiamin_mg, ls.Riboflavin_mg, ls.Niacin_mg, ls.Vitamin_B6_mg, ls.Vitamin_B12_mg, ls.Pantothenic_acid_mg
            FROM 
                life_stage_group_daily_recommand AS ls, user_profile, belong_team
            WHERE 
				belong_team.team_id = %s
                AND user_profile.user_id = belong_team.user_id
                AND ls.gender = user_profile.gender 
                AND ls.subgroup = user_profile.subgroup 
                AND ls.min_age = user_profile.min_age 
                AND ls.max_age = user_profile.max_age
        ) AS recom_user,
        (
            SELECT 
                eat.user_id,
                eat.date_of_eat,
                SUM(eat.amount * food.Vitamin_A_mg / 100) AS daily_nutrient_A,
                SUM(eat.amount * food.Vitamin_C_mg / 100) AS daily_nutrient_C,
                SUM(eat.amount * food.Vitamin_D_mg / 100) AS daily_nutrient_D,
                SUM(eat.amount * food.Vitamin_K_mg / 100) AS daily_nutrient_K,
                SUM(eat.amount * food.Vitamin_E_mg / 100) AS daily_nutrient_E,
                SUM(eat.amount * food.Thiamin_mg / 100) AS daily_nutrient_Thiamin,
                SUM(eat.amount * food.Riboflavin_mg / 100) AS daily_nutrient_Riboflavin,
                SUM(eat.amount * food.Niacin_mg / 100) AS daily_nutrient_Niacin,
                SUM(eat.amount * food.Vitamin_B6_mg / 100) AS daily_nutrient_B6,
                SUM(eat.amount * food.Vitamin_B12_mg / 100) AS daily_nutrient_B12,
                SUM(eat.amount * food.Pantothenic_acid_mg / 100) AS daily_nutrient_Pantothenic_acid
            FROM 
                eat, food, belong_team
            WHERE 
				eat.food_name = food.food_name
                AND belong_team.team_id = %s
                AND eat.user_id = belong_team.user_id
                AND eat.date_of_eat BETWEEN %s AND %s
            GROUP BY 
                eat.user_id, eat.date_of_eat
        ) AS daily, user_profile
	 WHERE 
		recom_user.user_id = daily.user_id
		AND recom_user.user_id = user_profile.user_id
    GROUP BY
		recom_user.user_id
        """
    try:
        connection, cursor = connect_to_db()
        # Execute the query
        cursor.execute(query, (team_id, team_id, start_date, end_date))
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error occurred: {e}")
        raise
    finally:
        # Ensure resources are cleaned up
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def winner_in_team_comparison(team_id, start_date, end_date):
    # return the winner user - the user that has the lowest average daily gap for the highest number of nutrients. if there is a tie, return list of users
    # return the user id, username and the number of nutrients that the user has the lowest average daily gap
    query = f"""
WITH AvgGapPerUser AS (
    SELECT
        recom_user.user_id,
        AVG(
            CASE
                WHEN (recom_user.Vitamin_A_mg - daily.daily_nutrient_A) / recom_user.Vitamin_A_mg * 100 < 0 THEN 0
                ELSE (recom_user.Vitamin_A_mg - daily.daily_nutrient_A) / recom_user.Vitamin_A_mg * 100
            END
        ) AS Avg_Percentage_Vitamin_A,
        AVG(
            CASE
                WHEN (recom_user.Vitamin_C_mg - daily.daily_nutrient_C) / recom_user.Vitamin_C_mg * 100 < 0 THEN 0
                ELSE (recom_user.Vitamin_C_mg - daily.daily_nutrient_C) / recom_user.Vitamin_C_mg * 100
            END
        ) AS Avg_Percentage_Vitamin_C,
        AVG(
            CASE
                WHEN (recom_user.Vitamin_D_mg - daily.daily_nutrient_D) / recom_user.Vitamin_D_mg * 100 < 0 THEN 0
                ELSE (recom_user.Vitamin_D_mg - daily.daily_nutrient_D) / recom_user.Vitamin_D_mg * 100
            END
        ) AS Avg_Percentage_Vitamin_D,
        AVG(
    CASE
        WHEN (recom_user.Vitamin_E_mg - daily.daily_nutrient_E) / recom_user.Vitamin_E_mg * 100 < 0 THEN 0
        ELSE (recom_user.Vitamin_E_mg - daily.daily_nutrient_E) / recom_user.Vitamin_E_mg * 100
    END
) AS Avg_Percentage_Vitamin_E,
AVG(
    CASE
        WHEN (recom_user.Vitamin_K_mg - daily.daily_nutrient_K) / recom_user.Vitamin_K_mg * 100 < 0 THEN 0
        ELSE (recom_user.Vitamin_K_mg - daily.daily_nutrient_K) / recom_user.Vitamin_K_mg * 100
    END
) AS Avg_Percentage_Vitamin_K,
AVG(
    CASE
        WHEN (recom_user.Thiamin_mg - daily.daily_nutrient_Thiamin) / recom_user.Thiamin_mg * 100 < 0 THEN 0
        ELSE (recom_user.Thiamin_mg - daily.daily_nutrient_Thiamin) / recom_user.Thiamin_mg * 100
    END
) AS Avg_Percentage_Thiamin,
AVG(
    CASE
        WHEN (recom_user.Riboflavin_mg - daily.daily_nutrient_Riboflavin) / recom_user.Riboflavin_mg * 100 < 0 THEN 0
        ELSE (recom_user.Riboflavin_mg - daily.daily_nutrient_Riboflavin) / recom_user.Riboflavin_mg * 100
    END
) AS Avg_Percentage_Riboflavin,
AVG(
    CASE
        WHEN (recom_user.Niacin_mg - daily.daily_nutrient_Niacin) / recom_user.Niacin_mg * 100 < 0 THEN 0
        ELSE (recom_user.Niacin_mg - daily.daily_nutrient_Niacin) / recom_user.Niacin_mg * 100
    END
) AS Avg_Percentage_Niacin_mg,
AVG(
    CASE
        WHEN (recom_user.Vitamin_B6_mg - daily.daily_nutrient_B6) / recom_user.Vitamin_B6_mg * 100 < 0 THEN 0
        ELSE (recom_user.Vitamin_B6_mg - daily.daily_nutrient_B6) / recom_user.Vitamin_B6_mg * 100
    END
) AS Avg_Percentage_Vitamin_B6,
AVG(
    CASE
        WHEN (recom_user.Vitamin_B12_mg - daily.daily_nutrient_B12) / recom_user.Vitamin_B12_mg * 100 < 0 THEN 0
        ELSE (recom_user.Vitamin_B12_mg - daily.daily_nutrient_B12) / recom_user.Vitamin_B12_mg * 100
    END
) AS Avg_Percentage_Vitamin_B12,
AVG(
    CASE
        WHEN (recom_user.Pantothenic_acid_mg - daily.daily_nutrient_Pantothenic_acid) / recom_user.Pantothenic_acid_mg * 100 < 0 THEN 0
        ELSE (recom_user.Pantothenic_acid_mg - daily.daily_nutrient_Pantothenic_acid) / recom_user.Pantothenic_acid_mg * 100
    END
) AS Avg_Percentage_Pantothenic_acid
    FROM 
        (
            SELECT 
                user_profile.user_id, ls.Vitamin_A_mg, ls.Vitamin_C_mg, ls.Vitamin_D_mg, ls.Vitamin_K_mg, ls.Vitamin_E_mg, ls.Thiamin_mg, ls.Riboflavin_mg, ls.Niacin_mg, ls.Vitamin_B6_mg, ls.Vitamin_B12_mg, ls.Pantothenic_acid_mg
            FROM 
                life_stage_group_daily_recommand AS ls, user_profile, belong_team
            WHERE 
                belong_team.team_id = %s
                AND user_profile.user_id = belong_team.user_id
                AND ls.gender = user_profile.gender 
                AND ls.subgroup = user_profile.subgroup 
                AND ls.min_age = user_profile.min_age 
                AND ls.max_age = user_profile.max_age
        ) AS recom_user,
        (
            SELECT 
                eat.user_id,
                eat.date_of_eat,
                SUM(eat.amount * food.Vitamin_A_mg / 100) AS daily_nutrient_A,
                SUM(eat.amount * food.Vitamin_C_mg / 100) AS daily_nutrient_C,
                SUM(eat.amount * food.Vitamin_D_mg / 100) AS daily_nutrient_D,
                SUM(eat.amount * food.Vitamin_K_mg / 100) AS daily_nutrient_K,
                SUM(eat.amount * food.Vitamin_E_mg / 100) AS daily_nutrient_E,
                SUM(eat.amount * food.Thiamin_mg / 100) AS daily_nutrient_Thiamin,
                SUM(eat.amount * food.Riboflavin_mg / 100) AS daily_nutrient_Riboflavin,
                SUM(eat.amount * food.Niacin_mg / 100) AS daily_nutrient_Niacin,
                SUM(eat.amount * food.Vitamin_B6_mg / 100) AS daily_nutrient_B6,
                SUM(eat.amount * food.Vitamin_B12_mg / 100) AS daily_nutrient_B12,
                SUM(eat.amount * food.Pantothenic_acid_mg / 100) AS daily_nutrient_Pantothenic_acid
            FROM 
                eat, food, belong_team
            WHERE 
                eat.food_name = food.food_name
                AND belong_team.team_id = %s
                AND eat.user_id = belong_team.user_id
                AND eat.date_of_eat BETWEEN %s AND %s
            GROUP BY 
                eat.user_id, eat.date_of_eat
        ) AS daily
    WHERE 
        recom_user.user_id = daily.user_id
    GROUP BY
        recom_user.user_id
),
MinGaps AS (
    SELECT
        MIN(Avg_Percentage_Vitamin_A) AS Min_Vitamin_A,
        MIN(Avg_Percentage_Vitamin_C) AS Min_Vitamin_C,
        MIN(Avg_Percentage_Vitamin_D) AS Min_Vitamin_D,
        MIN(Avg_Percentage_Vitamin_K) AS Min_Vitamin_K,
        MIN(Avg_Percentage_Vitamin_E) AS Min_Vitamin_E,
        MIN(Avg_Percentage_Thiamin) AS Min_Thiamin,
        MIN(Avg_Percentage_Riboflavin) AS Min_Riboflavin,
        MIN(Avg_Percentage_Niacin_mg) AS Min_Niacin_mg,
        MIN(Avg_Percentage_Vitamin_B6) AS Min_Vitamin_B6,
        MIN(Avg_Percentage_Vitamin_B12) AS Min_Vitamin_B12,
        MIN(Avg_Percentage_Pantothenic_acid) AS Min_Pantothenic_acid
    FROM AvgGapPerUser
),
UserCounts AS (
    SELECT
        user_id,
        (CASE WHEN Avg_Percentage_Vitamin_A = (SELECT Min_Vitamin_A FROM MinGaps) THEN 1 ELSE 0 END +
         CASE WHEN Avg_Percentage_Vitamin_C = (SELECT Min_Vitamin_C FROM MinGaps) THEN 1 ELSE 0 END +
         CASE WHEN Avg_Percentage_Vitamin_D = (SELECT Min_Vitamin_D FROM MinGaps) THEN 1 ELSE 0 END +
         CASE WHEN Avg_Percentage_Vitamin_K = (SELECT Min_Vitamin_K FROM MinGaps) THEN 1 ELSE 0 END +
            CASE WHEN Avg_Percentage_Vitamin_E = (SELECT Min_Vitamin_E FROM MinGaps) THEN 1 ELSE 0 END +
            CASE WHEN Avg_Percentage_Thiamin = (SELECT Min_Thiamin FROM MinGaps) THEN 1 ELSE 0 END +
            CASE WHEN Avg_Percentage_Riboflavin = (SELECT Min_Riboflavin FROM MinGaps) THEN 1 ELSE 0 END +
            CASE WHEN Avg_Percentage_Niacin_mg = (SELECT Min_Niacin_mg FROM MinGaps) THEN 1 ELSE 0 END +
            CASE WHEN Avg_Percentage_Vitamin_B6 = (SELECT Min_Vitamin_B6 FROM MinGaps) THEN 1 ELSE 0 END +
            CASE WHEN Avg_Percentage_Vitamin_B12 = (SELECT Min_Vitamin_B12 FROM MinGaps) THEN 1 ELSE 0 END +
            CASE WHEN Avg_Percentage_Pantothenic_acid = (SELECT Min_Pantothenic_acid FROM MinGaps) THEN 1 ELSE 0 END
        ) AS Total_Min_Count
    FROM AvgGapPerUser
)
SELECT UserCounts.user_id, user_profile.username, Total_Min_Count
FROM UserCounts, user_profile
WHERE Total_Min_Count = (SELECT MAX(Total_Min_Count) FROM UserCounts)
AND UserCounts.user_id = user_profile.user_id;
"""
    try:
        connection, cursor = connect_to_db()
        # Execute the query
        cursor.execute(query, (team_id, team_id, start_date, end_date))
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error occurred: {e}")
        raise
    finally:
        # Ensure resources are cleaned up
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def violate_users_of_team(team_id, start_date, end_date):
    # return users that have day with no eat data in the given period
    query = f"""SELECT DISTINCT eat.user_id, user_profile.username
        FROM eat, belong_team, user_profile
        WHERE 
        eat.user_id = belong_team.user_id
        AND belong_team.team_id = %s
        AND eat.date_of_eat BETWEEN %s AND %s
        AND user_profile.user_id = belong_team.user_id
        GROUP BY eat.user_id
        HAVING COUNT(DISTINCT eat.date_of_eat) < DATEDIFF(%s, %s) + 1"""

    try:
        connection, cursor = connect_to_db()
        # Execute the query
        cursor.execute(query, (team_id, start_date, end_date, end_date, start_date))
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error occurred: {e}")
        raise
    finally:
        # Ensure resources are cleaned up
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_all_food_names():
    connection, cursor = connect_to_db()
    try:
        cursor.execute("SELECT food_name FROM food")
        foods = [row[0] for row in cursor.fetchall()]
        cursor.close()
        connection.close()
        return foods
    except Exception as e:
        connection.rollback()
        return []
