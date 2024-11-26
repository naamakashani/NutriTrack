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


def create_users():
    # Creating additional data with more Adults
    data = [
        ['Male', 0.8, 'Infants', 7.2, 68, 'Sedentary'],
        ['Female', 4, 'Children', 18, 105, 'Lightly active'],
        ['Male', 11, 'Adult', 55, 155, 'Moderately active'],
        ['Female', 28, 'Pregnancy', 68, 162, 'Lightly active'],
        ['Male', 21, 'Lactation', 58, 168, 'Very active'],
        ['Female', 6, 'Children', 23, 120, 'Moderately active'],
        ['Male', 13, 'Adult', 60, 160, 'Lightly active'],
        ['Male', 9, 'Children', 32, 135, 'Moderately active'],
        ['Female', 19, 'Pregnancy', 75, 170, 'Extra active'],
        ['Male', 5, 'Children', 22, 110, 'Sedentary'],
        ['Male', 10, 'Adult', 45, 150, 'Moderately active'],
        ['Female', 18, 'Lactation', 60, 165, 'Very active'],
        ['Male', 4, 'Children', 18, 105, 'Sedentary'],
        ['Female', 33, 'Pregnancy', 72, 160, 'Moderately active'],
        ['Male', 7, 'Children', 24, 115, 'Lightly active'],
        ['Female', 15, 'Adult', 55, 160, 'Very active'],
        ['Male', 0.6, 'Infants', 6.5, 66, 'Sedentary'],
        ['Male', 30, 'Adult', 70, 175, 'Very active'],
        ['Female', 35, 'Adult', 72, 168, 'Lightly active'],
        ['Male', 40, 'Adult', 78, 180, 'Moderately active'],
        ['Female', 45, 'Adult', 80, 170, 'Very active'],
        ['Male', 50, 'Adult', 85, 185, 'Sedentary'],
        ['Female', 25, 'Adult', 65, 160, 'Extra active'],
        ['Male', 38, 'Adult', 76, 177, 'Lightly active'],
        ['Female', 22, 'Adult', 62, 165, 'Moderately active'],
        ['Male', 29, 'Adult', 68, 174, 'Very active'],
        ['Male', 27, 'Adult', 68, 173, 'Lightly active'],
        ['Female', 32, 'Adult', 72, 165, 'Moderately active'],
        ['Male', 41, 'Adult', 80, 178, 'Very active'],
        ['Female', 24, 'Adult', 63, 160, 'Lightly active'],
        ['Male', 39, 'Adult', 75, 177, 'Moderately active'],
        ['Female', 29, 'Adult', 70, 167, 'Very active'],
        ['Male', 36, 'Adult', 78, 182, 'Sedentary'],
        ['Female', 48, 'Adult', 79, 170, 'Lightly active'],
        ['Male', 33, 'Adult', 73, 175, 'Extra active'],
        ['Female', 26, 'Adult', 68, 163, 'Moderately active'],
        ['Male', 50, 'Adult', 82, 180, 'Sedentary'],
        ['Female', 44, 'Adult', 77, 168, 'Moderately active'],
        ['Male', 31, 'Adult', 69, 174, 'Lightly active'],
        ['Female', 55, 'Adult', 74, 165, 'Very active'],
        ['Male', 42, 'Adult', 76, 179, 'Moderately active'],
        ['Female', 37, 'Adult', 71, 162, 'Very active'],
        ['Male', 30, 'Adult', 70, 172, 'Moderately active'],
        ['Female', 23, 'Adult', 64, 160, 'Sedentary'],
        ['Male', 47, 'Adult', 85, 185, 'Lightly active']

    ]

    # Creating a DataFrame
    df = pd.DataFrame(data, columns=['gender', 'age', 'subgroup', 'weight', 'height', 'activity_level'])
    # Iterate over the DataFrame and execute the insert query for each row
    insert_query = """
    INSERT INTO user_profile (gender, age, subgroup, min_age, max_age, weight, height, activity_level)
    SELECT
        %s AS gender,
        %s AS age,
        %s AS subgroup,
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

    for index, row in df.iterrows():
        cursor.execute(insert_query, (row['gender'], row['age'], row['subgroup'], row['weight'], row['height'],
                                      row['activity_level'], row['subgroup'], row['gender'], row['age']))

    connection.commit()
    print("Users created successfully")


create_users()
