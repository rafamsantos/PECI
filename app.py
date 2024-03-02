import socket
from cmath import sqrt
import os
import sys
import ast
from cryptography.hazmat.primitives import serialization
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
    SERVER_HOST = '192.168.185.147'  # IP address of the server
    SERVER_PORT = 12345                 # Port the server is listening on
    
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
    client_sock.connect((SERVER_HOST, SERVER_PORT))

# Connect to the server
# Receive data from the server
    message = "Im client"
    client_sock.send(message.encode())
    
    response = client_sock.recv(1024)
    print(f"Server says: {response.decode()}")
    user = "1"
    client_priv, client_pub = set_asymetric()	
	# d = client_pub.verify(user, j)	
    client_sock.send(client_pub.exportKey(format='PEM', passphrase=None, pkcs=1))
    server_pub = RSA.importKey(client_sock.recv(2048), passphrase=None)
    #print(server_pub)
    message = "I'm a cliente"
    client_sock.send(message.encode())
    key = client_sock.recv(1024)
    st = recv_dict(client_sock)
    key = base64.b64decode(key)
    cipherR = PKCS1_OAEP.new(client_priv)
    key = cipherR.decrypt(key)
    ud = hashlib.sha256(str(key).encode("utf8")).digest()
    u = server_pub.verify(ud, st["sig"])
    iv = base64.b64decode(st["iv"])
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
        print("what you want to do?\n")
        comand = input() #Var given via aplication
        if(int(comand) == 1):
            ud = hashlib.sha256(str(i_m).encode("utf8")).digest()
            st = {"command": "NFC", "door": comand, "I'm": i_m, "Sig": client_priv.sign(ud, 32)}
            send_dict(client_sock, st)
            st = recv_dict(client_sock)
            st_ex = {"Compromise": "You where compromise\nQuiting..."}
            if st == st_ex:
                print("You where compromise\nQuiting...\n")
                return 0
            NFC_code = st["NFC code"]
            NFC_code = base64.b64decode(NFC_code)
            NFC_code = decryptor.update(NFC_code) + decryptor.finalize()
            NFC_code = ndef.TextRecord(NFC_code)
        elif(int(comand) == 2):
            ud = hashlib.sha256(str(i_m).encode("utf8")).digest()
            st = {"command": "LOG", "ID": user, "I'm": i_m, "Sig": client_priv.sign(ud, 32)}
            send_dict(client_sock, st)
            st = recv_dict(client_sock)
            log = st["The Logs"]
            log = base64.b64decode(log)
            log = decryptor.update(log) + decryptor.finalize()
            print(log)
        
        
        
    
        
    

if __name__ == "__main__":
    main()
        

