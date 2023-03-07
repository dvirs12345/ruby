import add_to_suspects_table
import readLicenecePlate
import psycopg2
import threading

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

def addSuspectThread(image, id):
    open("./2/{}.jpg".format(id), 'wb').write(image[-2])
    number_plate = readLicenecePlate.getLicensePlate(id)
    print(number_plate)
    report = {
        'number': number_plate,
        'sensor_id': image[0],
        'timestamp': image[-1],
        'sensor_location_x': image[1],
        'sensor_location_y': image[2]
    }

    add_to_suspects_table.addToSuspectTable(report)

threads = []
imageId = 0
for image in data:
    addSuspect = threading.Thread(target=addSuspectThread, args=(image, imageId))
    threads.append(addSuspect)
    addSuspect.start()
    imageId += 1

for currentThread in threads:
    print(currentThread)
    currentThread.join()





