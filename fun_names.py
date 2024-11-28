import pymysql
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
                       (user_id, gender, age, subgroup, username, weight, height, activity_level, subgroup, gender, age))

        # Commit the transaction to save changes
        connection.commit()

    except pymysql.MySQLError as e:
        # Handle exceptions (log the error or re-raise as needed)
        print(f"Error inserting into user_profile table: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


def insert_eaten(food_name, amount, user_id, date_of_eat):
    # Insert the eaten food to the eat table
    connection, cursor = connect_to_db()

    # SQL query to insert data into the eat table
    insert_query = """
        INSERT INTO eat (food_name, amount, user_id, date_of_eat)
        VALUES (%s, %s, %s, %s);
    """

    try:
        # Execute the query with the provided values
        cursor.execute(insert_query, (food_name, amount, user_id, date_of_eat))

        # Commit the transaction to save changes
        connection.commit()

    except pymysql.MySQLError as e:
        # Handle exceptions (log the error or re-raise as needed)
        print(f"Error inserting into eat table: {e}")

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


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
    print("daily gap of the user in the given date")
    print("user id: ", user_id)
    print("date: ", date)
    return 80;


def recommand_food(defic_list):
    # return the recommanded food by the list of deficencies
    # by top 10
    return 0;


def statistics(user_id):
    # return the statistics of the user
    return 0;


def trends(user_id):
    # return the trends of the user
    return 0;


def comparison_team(team_id):
    # return the comparison of the team
    return 0;

