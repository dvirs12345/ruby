import socket
import rsa
import time


if __name__ == '__main__':
    KEY_SIZE = 2048
    UDP_IP = ""
    UDP_PORT = "8090"

    print("UDP target IP:", UDP_IP)
    print("UDP target port:", UDP_PORT)

    (public_key, private_key) = rsa.newkeys(KEY_SIZE)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send key that will be used to verify signatures
    sock.sendto(bytes(public_key), (UDP_IP, UDP_PORT))

    while True:
        message = ""
        bytes_message = bytes(message, "utf-8")
        signature = rsa.sign(bytes_message, private_key, 'SHA-512')

        sock.sendto(signature, (UDP_IP, UDP_PORT))
        sock.sendto(bytes_message, (UDP_IP, UDP_PORT))
        time.sleep(1)
