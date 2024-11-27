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

groups = ['Microsoft', 'Google', 'Amazon', 'Facebook', 'Apple', 'AngelmanFamily', 'BacharFamily', 'CohenFamily' ]
def insert_teams(groups):
    # Prepare the SQL query with placeholders
    insert_query = "INSERT INTO team (team_name) VALUES (%s)"

    try:
        # Use executemany to insert multiple rows efficiently
        cursor.executemany(insert_query, [(group,) for group in groups])
        connection.commit()
        print(f"{len(groups)} groups inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Call the function
insert_teams(groups)
