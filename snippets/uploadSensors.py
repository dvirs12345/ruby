import psycopg2
import datetime
import random
import os
import threading

conn = psycopg2.connect(
    database="postgres",
    user='postgres',
    password='bagrut3',
    host='10.252.30.4',
    port='5432'
)

sensorsArr = [["Nazlat Zayd", 32.453982, 35.177957],
              ["Elkosh", 33.044436, 35.319963],
              ["Sderot", 31.525924, 34.594307],
              ["Hebron", 31.532129, 35.102015],
              ["Rehavia", 31.767855, 35.206349],
              ["Beit Guvrin", 31.612125, 34.896332],
              ["Shivta", 30.881710, 34.630321],
              ["Zohar", 31.236357, 34.426551],
              ["Bethlehem", 31.705054, 35.202593],
              ["Eilat", 29.554385, 34.941726]]

cursor = conn.cursor()

def main():
    directory = './3'
    threads = []

    for filename in os.listdir(directory):
        fileThread = threading.Thread(target=insertToDb, args=(filename,))
        threads.append(fileThread)
        fileThread.start()

    for currentThread in threads:
        print(currentThread)
        currentThread.join()

    print("finished")
    cursor.execute("SELECT * FROM sensors.images")
    data = cursor.fetchall()
    open("FromDB.jpg", 'wb').write(data[4][-2])
    print(data[0][-2])

def insertToDb(filename):
    randNum = random.randint(0, 9)
    camid = sensorsArr[randNum][0]
    long = sensorsArr[randNum][1]
    lat = sensorsArr[randNum][2]
    imageSrc = open("./3/" + filename, 'rb').read()
    timestamp = datetime.datetime.now()
    print(filename)
    query = "INSERT INTO sensors.images (camera_id, longitude, latitude, image_src, sensors_timestamp) "
    cursor.execute(query + "VALUES(%s,%s,%s,%s,%s)",
                   (camid, long, lat, psycopg2.Binary(imageSrc), timestamp))
    conn.commit()

if __name__ == "__main__":
    main()
