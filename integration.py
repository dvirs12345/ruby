import add_to_suspects_table
import readLicensePlate
import psycopg2

connection = psycopg2.connect(
    database="postgres",
    user='postgres',
    password='bagrut3',
    host='20.229.148.43',
    port='5432'
)

cursor = connection.cursor()

cursor.execute(str("SELECT * FROM sensors.images LIMIT 1"))
data = cursor.fetchall()
open("FromDB.jpg", 'wb').write(data[0][-2])

number_plate = readLicensePlate.getLicensePlate()

exampleReport = {
        'number': number_plate,
        'sensor_id': 'sensor',
        'timestamp': datetime.datetime.now(),
        'sensor_location_x': 1,
        'sensor_location_y': 100
    }

