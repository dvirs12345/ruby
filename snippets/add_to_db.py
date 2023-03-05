import json
import  psycopg2

if __name__ == '__main__':
    DATA_INDEX = 1

    conn = psycopg2.connect(
        database="postgres",
        user='postgres',
        password='vn3fxpugx',
        host='localhost',
        port='5432'
    )

    #TO DO: Change value according to table
    sql_query = "INSERT INTO persons (photo_url) VALUES (%s);"
    cursor = conn.cursor()

    with open("population_registry.json", encoding="utf8") as json_file:
        data = json.load(json_file)
        for item in data.items():
            cursor.execute(sql_query, (item[DATA_INDEX]['photo_url']))
