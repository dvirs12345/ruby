import socket
import requests
import csv
import json

# HOST = "127.0.0.1"
# PORT = 8090
#
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_socket.bind((HOST, PORT))
#
# while True:
#     message, address = server_socket.recvfrom(1024)
#     server_socket.sendto(message, address)

def getWantedLevel(licencePlate):
    KEY = 'duhcEFRU8BhZSZbwonbsVWwUOczcn4O=qFCpOoZDjj4X0bn4TEJyhak44jnxOuFFnTj1G1?d04LxsUmva8f-N-46b=Y4F5aCMeTq?OCfngG7DTwz/X-S-luxTO?yQNuX7/22lgo5JFTPX?0S2eWku?HEsD7RRxdrIFAc6!uAg?JE0DlmGL?/G5ZX?bC05ozSB0XtL1yGILCUihJc22EIYNYPB/DOg!0OrfIgseh58s6WdZg6KvK!xKo6n=!DyUFm'
    headers = {'authorize': KEY}

    req = requests.get("http://10.11.30.212:8000/citizens/lz/" + str(licencePlate), headers=headers)

    return req.text

def csv_to_json(csv_file_path, json_file_path):
    data_dict = {}

    with open(csv_file_path, encoding='utf-8') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)

        index = 0
        for rows in csv_reader:
            index += 1
            data_dict[index] = rows

    with open(json_file_path, 'w', encoding='utf-8') as json_file_handler:
        # Step 4
        json_file_handler.write(json.dumps(data_dict, indent=4))

csv_file_path = "./addresses.csv"
json_file_path = "./test.json"

csv_to_json(csv_file_path, json_file_path)
