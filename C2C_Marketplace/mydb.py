# import mysql.connector

# database = mysql.connector.connect(
#     'host':'localhost',
#     'name':'root',
#     'password':'admin123'
#     )

# curserobject= database.cursor()

# curserobject.execute("CREATE DATABASE test")

# print ("Database Created Successfully!")

import psycopg

# Define your database credentials
db_params = {
    "host": "localhost",
    "dbname": "C2CMarketplace",
    "user": "ahmed",
    "password": "aaaa0000",
    "port": 5432
}

try:
    # 1. Open the connection
    with psycopg.connect(**db_params) as conn:
        print("#1")
        # 2. Open a cursor to perform database operations
        with conn.cursor() as cur:
            print("#2")
            # 3. Execute a SQL statement
            cur.execute("UPDATE NAMEUsers_userprofile")
            print("#3")
            # 4. Fetch the result
            db_query = cur.fetchone()
            print(f"Successfully connected to db! \n {db_query}")
            
except Exception as error:
    print(f"Database connection failed: {error}")
