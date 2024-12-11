import pymysql
from collections import defaultdict
import re


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
        print(f"Error connecting to database: {e}")
        raise  # Re-raise the exception after logging


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
        LIMIT 1;
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
        return f"An error occurred: {e}"


def create_new_team(team_name):
    # Create a new team
    connection, cursor = connect_to_db()
    insert_query = "INSERT INTO team (team_name) VALUES (%s)"

    try:
        # Execute the query with the provided values
        cursor.execute(insert_query, (team_name,))  # Ensure that team_name is passed as a tuple

        # Commit the transaction to save changes
        connection.commit()

    except pymysql.MySQLError as e:
        # Handle exceptions (log the error or re-raise as needed)
        print(f"Error inserting into team table: {e}")

    finally:
        # Close the cursor and connection
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
        # Connect to the database
        connection, cursor = connect_to_db()

        # Fetch user profile
        cursor.execute("""
            SELECT gender, subgroup, min_age, max_age, desired_calories
            FROM user_profile
            WHERE user_id = %s
        """, (user_id,))
        user_profile = cursor.fetchone()

        if not user_profile:
            return {"error": "User not found"}

        gender, subgroup, min_age, max_age, desired_calories = user_profile

        # Fetch recommended daily values
        cursor.execute("""
            SELECT Vitamin_A_mg, Vitamin_C_mg, Vitamin_D_mg, Vitamin_E_mg, Vitamin_K_mg,
                   Thiamin_mg, Riboflavin_mg, Niacin_mg, Vitamin_B6_mg, Vitamin_B12_mg,
                   Pantothenic_acid_mg
            FROM life_stage_group_daily_recommand
            WHERE gender = %s AND subgroup = %s AND min_age <= %s AND max_age >= %s
        """, (gender, subgroup, min_age, max_age))
        recommended_values = cursor.fetchone()

        if not recommended_values:
            return {"error": "No recommendations found for the user profile"}

        # Map recommended values to a dictionary
        recommended_nutrients = {
            "Vitamin_A_mg": recommended_values[0],
            "Vitamin_C_mg": recommended_values[1],
            "Vitamin_D_mg": recommended_values[2],
            "Vitamin_E_mg": recommended_values[3],
            "Vitamin_K_mg": recommended_values[4],
            "Thiamin_mg": recommended_values[5],
            "Riboflavin_mg": recommended_values[6],
            "Niacin_mg": recommended_values[7],
            "Vitamin_B6_mg": recommended_values[8],
            "Vitamin_B12_mg": recommended_values[9],
            "Pantothenic_acid_mg": recommended_values[10],
        }

        # Fetch total nutrient and calorie intake for the user on the given date
        cursor.execute("""
            SELECT SUM(eat.amount * food.Vitamin_A_mg / 100) AS daily_Vitamin_A_mg,
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
            WHERE eat.user_id = %s AND DATE(eat.date_of_eat) = %s
        """, (user_id, date))
        total_daily_consumption = cursor.fetchone()

        # Map fetched nutrient data to a dictionary
        nutrient_intakes = {
            "Vitamin_A_mg": total_daily_consumption[0] or 0,
            "Vitamin_C_mg": total_daily_consumption[1] or 0,
            "Vitamin_D_mg": total_daily_consumption[2] or 0,
            "Vitamin_E_mg": total_daily_consumption[3] or 0,
            "Vitamin_K_mg": total_daily_consumption[4] or 0,
            "Thiamin_mg": total_daily_consumption[5] or 0,
            "Riboflavin_mg": total_daily_consumption[6] or 0,
            "Niacin_mg": total_daily_consumption[7] or 0,
            "Vitamin_B6_mg": total_daily_consumption[8] or 0,
            "Vitamin_B12_mg": total_daily_consumption[9] or 0,
            "Pantothenic_acid_mg": total_daily_consumption[10] or 0,
        }
        total_calories_intake = total_daily_consumption[11] or 0

        # Calculate the daily gap
        daily_gap = {}
        for nutrient, recommended_value in recommended_nutrients.items():
            intake = nutrient_intakes.get(nutrient, 0)
            if intake < recommended_value:
                daily_gap[nutrient] = {"deficiency": recommended_value - intake, "excess": 0}
            elif intake > recommended_value:
                daily_gap[nutrient] = {"deficiency": 0, "excess": intake - recommended_value}
            else:
                daily_gap[nutrient] = {"deficiency": 0, "excess": 0}

        if total_calories_intake < desired_calories:
            daily_gap["Caloric_Value_kcal"] = {
                "deficiency": desired_calories - total_calories_intake,
                "excess": 0,
            }
        else:
            daily_gap["Caloric_Value_kcal"] = {
                "deficiency": 0,
                "excess": total_calories_intake - desired_calories,
            }


    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return daily_gap


def recommand_food(defic_list):
    """
    Recommend top 2 foods for each nutrient in the deficiency list.

    Parameters:
    - defic_list (list): list of  nutrients (e.g., 'Vitamin_A_mg')

    Returns:
    - recommendations (dict): Dictionary where keys are nutrients, and values
      are lists of top 2 food names that are richest in that nutrient.
    """

    connection, cursor = connect_to_db()
    recommendations = {}
    try:
        for nutrient in defic_list:
            # Query top 5 foods based on the nutrient
            query = f"""
                  SELECT food_name, {nutrient}
                  FROM food
                  ORDER BY {nutrient} DESC
                  LIMIT 2;
              """
            cursor.execute(query)
            results = cursor.fetchall()

            # Extract food names
            food_names = [row[0] for row in results]
            recommendations[nutrient] = food_names

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return recommendations


def avg_consumption(user_id,period):
    connection, cursor = connect_to_db()
    query = """
    SELECT 
        ROUND(AVG(e.amount * f.Caloric_Value_kcal / 100), 2) AS Avg_Calories,
        ROUND(AVG(e.amount * f.Protein_g / 100), 2) AS Avg_Protein_g,
        ROUND(AVG(e.amount * f.Dietary_Fiber_g / 100), 2) AS Avg_Fiber_g,
        ROUND(AVG(e.amount * f.Vitamin_A_mg / 100), 2) AS Avg_Vitamin_A_mg,
        ROUND(AVG(e.amount * f.Vitamin_C_mg / 100), 2) AS Avg_Vitamin_C_mg,
        ROUND(AVG(e.amount * f.Vitamin_D_mg / 100), 2) AS Avg_Vitamin_D_mg,
        ROUND(AVG(e.amount * f.Vitamin_E_mg / 100), 2) AS Avg_Vitamin_E_mg,
        ROUND(AVG(e.amount * f.Vitamin_K_mg / 100), 2) AS Avg_Vitamin_K_mg,
        ROUND(AVG(e.amount * f.Thiamin_mg / 100), 2) AS Avg_Thiamin_mg,
        ROUND(AVG(e.amount * f.Riboflavin_mg / 100), 2) AS Avg_Riboflavin_mg,
        ROUND(AVG(e.amount * f.Niacin_mg / 100), 2) AS Avg_Niacin_mg,
        ROUND(AVG(e.amount * f.Vitamin_B6_mg / 100), 2) AS Avg_Vitamin_B6_mg,
        ROUND(AVG(e.amount * f.Vitamin_B12_mg / 100), 2) AS Avg_Vitamin_B12_mg,
        ROUND(AVG(e.amount * f.Pantothenic_acid_mg / 100), 2) AS Avg_Pantothenic_Acid_mg
    FROM 
        eat e
    JOIN 
        food f ON e.food_name = f.food_name
    WHERE 
        e.user_id = %s 
        AND e.date_of_eat >= DATE_SUB(NOW(), INTERVAL %s DAY);
    """
    cursor.execute(query, (user_id,period))
    consumption = cursor.fetchone()
    if consumption:
        return {
            "Avg_Calories": consumption[0],
            "Avg_Protein_g": consumption[1],
            "Avg_Fiber_g": consumption[2],
            "Avg_Vitamin_A_mg": consumption[3],
            "Avg_Vitamin_C_mg": consumption[4],
            "Avg_Vitamin_D_mg": consumption[5],
            "Avg_Vitamin_E_mg": consumption[6],
            "Avg_Vitamin_K_mg": consumption[7],
            "Avg_Thiamin_mg": consumption[8],
            "Avg_Riboflavin_mg": consumption[9],
            "Avg_Niacin_mg": consumption[10],
            "Avg_Vitamin_B6_mg": consumption[11],
            "Avg_Vitamin_B12_mg": consumption[12],
            "Avg_Pantothenic_Acid_mg": consumption[13]
        }
    else:
        # If no data is found for the user in the last 7 days
        return None


def statistics(user_id):
    avg_week = avg_week_consumption(user_id,7)
    avg_month = avg_week_consumption(user_id,30)



def trends(user_id):
    # return the trends of the user
    return 0;


def comparison_team(team_id):
    # return the comparison of the team
    return 0;
