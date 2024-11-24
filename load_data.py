import pandas as pd
import pymysql

# Database connection details
host = 'localhost'
user = 'root'
password = 'Nn021099!'
database = 'food_recommandation'



# Connect to the database
connection = pymysql.connect(host=host, user=user, password=password, database=database)

# CSV file path
small_ = r'C:\Users\kashann\PycharmProjects\NutriTrack\FoodDataSmall.csv'

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
