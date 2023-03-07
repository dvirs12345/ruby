import socket
from readLicensePlate import *
import json
import time
import datetime
import psycopg2

DATA_INDEX = 1

last_timestamp = ''


def get_changes():
    time.sleep(120)
    connection = psycopg2.connect(
        database="postgres",
        user='postgres',
        password='bagrut3',
        host='10.252.30.4',
        port='5432'
    )

    cursor = connection.cursor()

    cursor.execute(str("SELECT * FROM sensors.images img WHERE img.sensors_timestamp > '" + str(last_timestamp) + "'"));
    return cursor.fetchall()


server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 3000))
server_socket.listen()
print("Server is up and running")
(client_socket, client_address) = server_socket.accept()
print("Client connected")

while True:

    data = get_changes()
    for d in data:
        print(d[3])
        open("FromDB.jpg", 'wb').write(d[3])
        plate = getLicensePlate()
       
        x = { "plateId":plate}
        y = json.dumps(x)
        client_socket.send(y.encode())
        last_timestamp = datetime.datetime.now()

client_socket.close()
server_socket.close()
