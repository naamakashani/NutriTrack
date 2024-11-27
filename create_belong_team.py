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

groups = [
    (1, 100000001), (1, 100000002), (1, 100000003), (2, 100000004), (2, 100000006),
    (3, 100000007)
]

def insert_belong_teams(groups):
    # Prepare the SQL query with placeholders
    insert_query = "INSERT INTO belong_team (team_id, user_id) VALUES (%s, %s)"
    # Iterate over the groups and execute the insert query
    for team_id, user_id in groups:
        cursor.execute(insert_query, (team_id, user_id))
        connection.commit()



# Call the function
insert_belong_teams(groups)

