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
    data = [
        [100000001, 'Male', 0.8, 'Infants', 'Alice_M', 7.2, 68, 'Sedentary'],
        [100000002, 'Female', 4, 'Children', 'Sophia_F', 18, 105, 'Lightly active'],
        [100000003, 'Male', 11, 'Adult', 'Liam_M', 55, 155, 'Moderately active'],
        [100000004, 'Female', 28, 'Pregnancy', 'Emma_F', 68, 162, 'Lightly active'],
        [100000005, 'Male', 21, 'Lactation', 'Noah_M', 58, 168, 'Very active'],
        [100000006, 'Female', 6, 'Children', 'Isabella_F', 23, 120, 'Moderately active'],
        [100000007, 'Male', 13, 'Adult', 'Elijah_M', 60, 160, 'Lightly active'],
        [100000008, 'Male', 9, 'Children', 'James_M', 32, 135, 'Moderately active'],
        [100000009, 'Female', 19, 'Pregnancy', 'Olivia_F', 75, 170, 'Extra active'],
        [100000010, 'Male', 5, 'Children', 'William_M', 22, 110, 'Sedentary'],
        [100000011, 'Male', 10, 'Adult', 'Benjamin_M', 45, 150, 'Moderately active'],
        [100000012, 'Female', 18, 'Lactation', 'Charlotte_F', 60, 165, 'Very active'],
        [100000013, 'Male', 4, 'Children', 'Henry_M', 18, 105, 'Sedentary'],
        [100000014, 'Female', 33, 'Pregnancy', 'Mia_F', 72, 160, 'Moderately active'],
        [100000015, 'Male', 7, 'Children', 'Alexander_M', 24, 115, 'Lightly active'],
        [100000016, 'Female', 15, 'Adult', 'Amelia_F', 55, 160, 'Very active'],
        [100000017, 'Male', 0.6, 'Infants', 'Lucas_M', 6.5, 66, 'Sedentary'],
        [100000018, 'Male', 30, 'Adult', 'Ethan_M', 70, 175, 'Very active'],
        [100000019, 'Female', 35, 'Adult', 'Ava_F', 72, 168, 'Lightly active'],
        [100000020, 'Male', 40, 'Adult', 'Jackson_M', 78, 180, 'Moderately active'],
        [100000021, 'Female', 45, 'Adult', 'Harper_F', 80, 170, 'Very active'],
        [100000022, 'Male', 50, 'Adult', 'Logan_M', 85, 185, 'Sedentary'],
        [100000023, 'Female', 25, 'Adult', 'Sophia_F', 65, 160, 'Extra active'],
        [100000024, 'Male', 38, 'Adult', 'Mason_M', 76, 177, 'Lightly active'],
        [100000025, 'Female', 22, 'Adult', 'Isabella_F', 62, 165, 'Moderately active'],
        [100000026, 'Male', 29, 'Adult', 'Sebastian_M', 68, 174, 'Very active'],
        [100000027, 'Male', 27, 'Adult', 'Lucas_M', 68, 173, 'Lightly active'],
        [100000028, 'Female', 32, 'Adult', 'Ella_F', 72, 165, 'Moderately active'],
        [100000029, 'Male', 41, 'Adult', 'Aiden_M', 80, 178, 'Very active'],
        [100000030, 'Female', 24, 'Adult', 'Emily_F', 63, 160, 'Lightly active'],
        [100000031, 'Male', 39, 'Adult', 'Nathan_M', 75, 177, 'Moderately active'],
        [100000032, 'Female', 29, 'Adult', 'Grace_F', 70, 167, 'Very active'],
        [100000033, 'Male', 36, 'Adult', 'Samuel_M', 78, 182, 'Sedentary'],
        [100000034, 'Female', 48, 'Adult', 'Hannah_F', 79, 170, 'Lightly active'],
        [100000035, 'Male', 33, 'Adult', 'Carter_M', 73, 175, 'Extra active'],
        [100000036, 'Female', 26, 'Adult', 'Victoria_F', 68, 163, 'Moderately active'],
        [100000037, 'Male', 50, 'Adult', 'Owen_M', 82, 180, 'Sedentary'],
        [100000038, 'Female', 44, 'Adult', 'Zoe_F', 77, 168, 'Moderately active'],
        [100000039, 'Male', 31, 'Adult', 'Leo_M', 69, 174, 'Lightly active'],
        [100000040, 'Female', 55, 'Adult', 'Lily_F', 74, 165, 'Very active'],
        [100000041, 'Male', 42, 'Adult', 'John_M', 76, 179, 'Moderately active'],
        [100000042, 'Female', 37, 'Adult', 'Scarlett_F', 71, 162, 'Very active'],
        [100000043, 'Male', 30, 'Adult', 'Isaac_M', 70, 172, 'Moderately active'],
        [100000044, 'Female', 23, 'Adult', 'Evelyn_F', 64, 160, 'Sedentary'],
        [100000045, 'Male', 47, 'Adult', 'Henry_M', 85, 185, 'Lightly active']
    ]
    # Creating a DataFrame
    df = pd.DataFrame(data, columns=['user_id', 'gender', 'age', 'subgroup', 'username', 'weight', 'height',
                                     'activity_level'])
    # Iterate over the DataFrame and execute the insert query for each row
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

    for index, row in df.iterrows():
        cursor.execute(insert_query, (
        row['user_id'], row['gender'], row['age'], row['subgroup'], row['username'], row['weight'], row['height'],
        row['activity_level'], row['subgroup'], row['gender'], row['age']))

    connection.commit()
    print("Users created successfully")


create_users()
