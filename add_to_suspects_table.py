from socket import socket

import psycopg2
import psycopg2.extras
from psycopg2.extensions import AsIs
import datetime
import random
import requests


def addToSuspectTable(report):
	@@ -17,23 +18,22 @@ def addToSuspectTable(report):
    )

    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM sensors.person WHERE '" + report['number'] + "' = ANY (license_plates);")

    result = cursor.fetchone() # assuming every LP has one owner
    print(result)
    if (result):
        cursor.execute("SELECT * FROM sensors.suspects WHERE person_id = '" + str(result['person_id']) + "'")
        suspectResult = cursor.fetchone()

        if (suspectResult):
            update_statement = "UPDATE sensors.suspects SET sensor_id=%s, timestamp=%s, " \
                               "sensor_location_x=%s, sensor_location_y=%s WHERE person_id = '" + str(result['person_id'] + "'")
            cursor.execute(update_statement, (report['sensor_id'], report['timestamp'],
                                              report['sensor_location_x'], report['sensor_location_y']))
            conn.commit()
        else:
            wantedLevel = getWantedLevel(result['license_plates'][0])

            result['sensor_id'] = report['sensor_id']
            result['timestamp'] = report['timestamp']
	@@ -63,6 +63,7 @@ def addToSuspectTable(report):
                    "actions": result['actions'],
                    "license_plates": result['license_plates'],
                    # "car_model": "", # we dont have that field
                    "work_visa": result['work_visa'],
                }

                columns = wantedRecord.keys()
	@@ -87,39 +88,20 @@ def sendLicensePlate(lp):
    # res = requests.post(url, json=request)
    # return res.text

def getWantedLevel(licencePlate):
    KEY = 'duhcEFRU8BhZSZbwonbsVWwUOczcn4O=qFCpOoZDjj4X0bn4TEJyhak44jnxOuFFnTj1G1?d04LxsUmva8f-N-46b=Y4F5aCMeTq?OCfngG7DTwz/X-S-luxTO?yQNuX7/22lgo5JFTPX?0S2eWku?HEsD7RRxdrIFAc6!uAg?JE0DlmGL?/G5ZX?bC05ozSB0XtL1yGILCUihJc22EIYNYPB/DOg!0OrfIgseh58s6WdZg6KvK!xKo6n=!DyUFm'
    headers = {'authorize': KEY}

    req = requests.get("http://10.11.30.212:8000/citizens/lz/" + str(licencePlate), headers=headers)

    return req.text

def listenForReports():
    report = {}

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 8090))

    while True:
        message, address = server_socket.recvfrom(1024)
        addToSuspectTable(message.decode())
