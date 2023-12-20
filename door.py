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
import ast
import socket
import json
import sqlite3 as sql
from Crypto.Util import Counter
from Crypto.Util.number import bytes_to_long
import base64
from Crypto.PublicKey import RSA
from common_comm import send_dict, recv_dict, sendrecv_dict
from cryptography.fernet import Fernet, MultiFernet
from Crypto.Cipher import PKCS1_OAEP
import math
import random
import rsa
from Crypto.Cipher import AES
from cryptography.hazmat.primitives import padding
import hashlib
import ndef
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

backend = default_backend()

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
