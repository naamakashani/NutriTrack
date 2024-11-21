import pandas as pd
import pymysql

# Database connection details
host = 'localhost'
user = 'your_username'
password = 'your_password'
database = 'your_database'

# CSV file path
csv_file_path = 'path_to_your_file.csv'

# Connect to the database
connection = pymysql.connect(host=host, user=user, password=password, database=database)

try:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Insert data into the SQL table
    df.to_sql('your_table_name', con=connection, if_exists='append', index=False)
    print("Data loaded successfully.")
except Exception as e:
    print("An error occurred:", e)
finally:
    # Close the database connection
    connection.close()
