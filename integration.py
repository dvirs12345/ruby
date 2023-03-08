import add_to_suspects_table
import readLicenecePlate
import psycopg2
import threading

#reportsThread = threading.Thread(target=add_to_suspects_table.listenForReports())
#reportsThread.start()

connection = psycopg2.connect(
    database="postgres",
    user='postgres',
    password='bagrut3',
    host='10.252.30.4',
    port='5432'
)

cursor = connection.cursor()

cursor.execute(str("SELECT * FROM sensors.images"))
data = cursor.fetchall()

threads = []

def addSuspect(image):
    open("FromDB.jpg", 'wb').write(image[-2])
    number_plate = readLicenecePlate.getLicensePlate()
    print(number_plate)
    report = {
        'number': number_plate,
        'sensor_id': image[1],
        'timestamp': image[-1],
        'sensor_location_x': image[2],
        'sensor_location_y': image[3]
    }

    addSuspect = threading.Thread(target=add_to_suspects_table.addToSuspectTable, args=(report, ))
    threads.append(addSuspect)
    addSuspect.start()

for image in data:
    addSuspect(image)

for currentThread in threads:
    print(currentThread)
    currentThread.join()
