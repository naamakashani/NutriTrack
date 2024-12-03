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
                       user_id, gender, age, subgroup, username, weight, height, activity_level, subgroup, gender, age))

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
    # return the daily gap of the user in the given date
    # the gap is dict of the deficencies and the excesses , the amount of the deficencies and the excesses
    connection, cursor = connect_to_db()
    # Fetch user profile to get gender, subgroup, age, and activity level
    cursor.execute("""
            SELECT gender, subgroup, min_age, max_age,desired_calories
            FROM user_profile
            WHERE user_id = %s
        """, (user_id,))
    user_profile = cursor.fetchone()

    if user_profile is None:
        return {"error": "User not found"}

    gender, subgroup, min_age, max_age, desired_calories = user_profile

    # Fetch recommended daily values from life_stage_group_daily_recommand
    cursor.execute("""
            SELECT Vitamin_A_mg, Vitamin_C_mg, Vitamin_D_mg, Vitamin_E_mg, Vitamin_K_mg, 
                   Thiamin_mg, Riboflavin_mg, Niacin_mg, Vitamin_B6_mg, Vitamin_B12_mg, 
                   Pantothenic_acid_mg
            FROM life_stage_group_daily_recommand
            WHERE gender = %s AND subgroup = %s AND min_age <= %s AND max_age >= %s
        """, (gender, subgroup, min_age, max_age))
    recommended_values = cursor.fetchone()

    if recommended_values is None:
        return {"error": "No recommendations found for the user profile"}

    # Map the recommended values to a dictionary for easy access
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
        "Pantothenic_acid_mg": recommended_values[10]
    }

    # Fetch the foods consumed by the user on the given date
    cursor.execute("""
            SELECT food_name, amount
            FROM eat
            WHERE user_id = %s AND DATE(date_of_eat) = %s
        """, (user_id, date))
    eaten_foods = cursor.fetchall()

    #create dictionary to store the daily intake of each nutrient
    nutrient_intakes = {
        "Vitamin_A_mg": 0,
        "Vitamin_C_mg": 0,
        "Vitamin_D_mg": 0,
        "Vitamin_E_mg": 0,
        "Vitamin_K_mg": 0,
        "Thiamin_mg": 0,
        "Riboflavin_mg": 0,
        "Niacin_mg": 0,
        "Vitamin_B6_mg": 0,
        "Vitamin_B12_mg": 0,
        "Pantothenic_acid_mg": 0
    }
    total_calories_intake = 0
    # Fetch nutritional info for each food consumed
    for food_name, amount in eaten_foods:
        cursor.execute("""
                SELECT Vitamin_A_mg, Vitamin_C_mg, Vitamin_D_mg, Vitamin_E_mg, Vitamin_K_mg, 
                       Thiamin_mg, Riboflavin_mg, Niacin_mg, Vitamin_B6_mg, Vitamin_B12_mg, 
                       Pantothenic_acid_mg, Caloric_Value_kcal
                FROM food
                WHERE food_name = %s
            """, (food_name,))
        food_nutrients = cursor.fetchone()

        if food_nutrients:
            # Calculate the intake of each nutrient for the given amount of the food
            for i, nutrient in enumerate(nutrient_intakes):
                nutrient_intakes[nutrient] += food_nutrients[i] * amount / 100  # Assuming amount is in grams
            total_calories_intake += food_nutrients[11] * amount / 100

    # Calculate the daily gap (deficiencies and excesses)
    daily_gap = {}
    for nutrient, recommended_value in recommended_nutrients.items():
        intake = nutrient_intakes.get(nutrient, 0)
        if intake < recommended_value:
            daily_gap[nutrient] = {"deficiency": recommended_value - intake, "excess": 0}
        elif intake > recommended_value:
            daily_gap[nutrient] = {"deficiency": 0, "excess": intake - recommended_value}
        else:
            daily_gap[nutrient] = {"deficiency": 0, "excess": 0}

    if desired_calories < total_calories_intake:
        daily_gap["Caloric_Value_kcal"] = {"deficiency": 0, "excess": total_calories_intake-desired_calories}
    else:
        daily_gap["Caloric_Value_kcal"] = {"deficiency": desired_calories-total_calories_intake, "excess": 0}


    # Close the database connection
    cursor.close()
    db.close()

    print("daily gap of the user in the given date")
    print("user id: ", user_id)
    print("date: ", date)
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


def statistics(user_id):
    # return the statistics of the user
    return 0;


def trends(user_id):
    # return the trends of the user
    return 0;


def comparison_team(team_id):
    # return the comparison of the team
    return 0;
