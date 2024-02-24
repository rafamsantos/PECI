import machine
from machine import Pin, SPI, PWM, I2C
from nfc import NFC
import utime, time
import st7789
import vga1_bold_16x32 as font
import os
import socket
from cmath import sqrt
import os
import sys
import socket
import json
from ucryptolib import AES
from common_comm import send_dict, recv_dict, sendrecv_dict
from cryptography.fernet import Fernet, MultiFernet
from ucryptolib import PKCS1_OAEP
import math
import random
import rsa
from cryptography.hazmat.primitives import padding
import hashlib
import ndef
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

backend = default_backend()

def base64_encode(data):
    b64chars = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    encoded = bytearray()
    remainder = len(data) % 3

    # Pad the data to make its length a multiple of 3
    if remainder:
        data += b'\x00' * (3 - remainder)

    for i in range(0, len(data), 3):
        chunk = (data[i] << 16) | (data[i + 1] << 8) | data[i + 2]
        encoded.extend([b64chars[(chunk >> 18) & 63], b64chars[(chunk >> 12) & 63], b64chars[(chunk >> 6) & 63], b64chars[chunk & 63]])

    # Replace padding bytes
    if remainder:
        encoded[-remainder:] = b'=' * remainder

    return encoded

def base64_decode(encoded):
    b64chars = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    decoded = bytearray()

    for i in range(0, len(encoded), 4):
        chunk = (b64chars.index(encoded[i]) << 18) | (b64chars.index(encoded[i + 1]) << 12) | (b64chars.index(encoded[i + 2]) << 6) | b64chars.index(encoded[i + 3])
        decoded.extend([(chunk >> 16) & 255, (chunk >> 8) & 255, chunk & 255])

    # Remove padding bytes
    while decoded[-1] == 0:
        decoded.pop()

    return decoded


def set_asymetric(): 
	priv = RSA.generate(2048)
	pub = priv.publickey()

	return priv, pub

def main():
# Create a socket object
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the server's hostname and port
    server_host = socket.gethostname()
    server_port = 9999

# Connect to the server
    client_sock.connect((server_host, server_port))

# Receive data from the server
    response = client_sock.recv(1024)
    print(f"Server says: {response.decode()}")
    user = "1"
    client_priv, client_pub = set_asymetric()	
	# d = client_pub.verify(user, j)	
    client_sock.send(client_pub.exportKey(format='PEM', passphrase=None, pkcs=1))
    server_pub = RSA.importKey(client_sock.recv(2048), passphrase=None)
    #print(server_pub)
    message = "I'm a door"
    client_sock.send(message.encode())
    st = recv_dict(client_sock)
    key = base64.b64decode(st["cipher"])
    iv = base64.b64decode(st["iv"])
    ud = hashlib.sha256(str(key).encode("utf8")).digest()
    u = server_pub.verify(ud, st["sig"])
    print(u)
    if u == False:
        print("The conction was compromise. We are disconcting you for your safety\n")
        client_sock.close()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend)
    ud = hashlib.sha256(str(key).encode("utf8")).digest()
    encryptor = cipher.encryptor()
    decryptor = cipher.decryptor()
    i_m = st["You are client"]
    while True:
        print("wating...\n")
        
        
        
        
    
        
    

if __name__ == "__main__":
    main()
