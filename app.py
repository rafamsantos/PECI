import socket
import threading
from cmath import sqrt
import os
import sys
import ast
import socket
import json
import sqlite3 as sql
from Crypto.Util import Counter
from Crypto.Util.number import bytes_to_long
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64
from Crypto.PublicKey import RSA
from common_comm import send_dict, recv_dict, sendrecv_dict
from cryptography.fernet import Fernet, MultiFernet
import math
import random
import rsa
import ndef
import binascii
from Crypto.Cipher import AES
from cryptography.hazmat.primitives import padding
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import random
import string
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import base64
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/door', methods = ['GET'])
def door_called():
   
    return jsonify({"User":["Hello","My","World"]})

    #response = {'message': 'Data received successfully'}
    #return jsonify(response)
    



backend = default_backend()

def set_asymetric(): 
	priv = RSA.generate(2048)
	pub = priv.publickey()

	return priv, pub

def main():
# Create a socket object
    SERVER_HOST = '192.168.118.147'  # IP address of the server
    SERVER_PORT = 12345                 # Port the server is listening on
    
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
    client_sock.connect((SERVER_HOST, SERVER_PORT))

# Connect to the server
# Receive data from the server
    message = "Im client"
    client_sock.send(message.encode())
    
    response = client_sock.recv(1024)
    name = "rmlameiras@ua.pt"
    message = "rmlameiras@ua.pt"
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
    ud = SHA256.new(bytearray(key))
    u = PKCS1_v1_5.new(server_pub).verify(ud, base64.b64decode(st["sig"]))
    #u = signaturaRSA.verify(ud, st["sig"])
    iv = base64.b64decode(st["iv"])
    print(u)
    if u == False:
        print("The conction was compromise. We are disconcting you for your safety\n")
        client_sock.close()
    
    my_permissions = st["Your permisions"] #Var with the permissions
    print(my_permissions)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend)
    ud = SHA256.new(bytearray(key))
    encryptor = cipher.encryptor()
    decryptor = cipher.decryptor()
    i_m = st["You are client"]
    while True:
        print("what you want to do?\n")
        comand = input() #Var given via aplication
        if(int(comand) == 1):
            ud = SHA256.new(bytearray(name.encode()))
            signaturaRSA = PKCS1_v1_5.new(client_priv)
            st = {"command": "NFC", "door": comand, "I'm": name, "Sig": str(base64.b64encode(signaturaRSA.sign(ud)), "utf8")}
            send_dict(client_sock, st)
            
            NFC_code = recv_dict(client_sock)
            print(NFC_code)
            NFC_code = decryptor.update(base64.b64decode(NFC_code["NFC code"])) + decryptor.finalize()
            record = ndef.TextRecord(NFC_code)
        elif(int(comand) == 2):
            ud = SHA256.new(bytearray(name.encode()))
            signaturaRSA = PKCS1_v1_5.new(client_priv)
            st = {"command": "Ademistrator_open", "door": comand, "I'm": name, "Sig": str(base64.b64encode(signaturaRSA.sign(ud)), "utf8")}
            send_dict(client_sock, st)
            st = recv_dict(client_sock)
            log = st["The Logs"]
            log = base64.b64decode(log)
            log = decryptor.update(log) + decryptor.finalize()
            print(log)
        
        elif(int(comand) == 3): #addmistrator open door
            ud = SHA256.new(bytearray(name.encode()))
            signaturaRSA = PKCS1_v1_5.new(client_priv)
            print("which door?\n")
            do = input() #Var given via aplication about door to opne Note: Only door is 4
            st = {"command": "Ademistrator_open", "door": comand, "I'm": name, "Sig": str(base64.b64encode(signaturaRSA.sign(ud)), "utf8"), "door": do}
            send_dict(client_sock, st)
        
        
        
    
        
    

if __name__ == "__main__":
    app.run(host='192.168.56.1',port=12345,debug=True)
   # main()
        

