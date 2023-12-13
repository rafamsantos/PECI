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
import base64
from Crypto.PublicKey import RSA
from common_comm import send_dict, recv_dict, sendrecv_dict
from cryptography.fernet import Fernet, MultiFernet
from Crypto.Cipher import PKCS1_OAEP
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

# Function to handle each client's connection
backend = default_backend()
many_users = 0

def databasecreate_user(db):
    db = sql.connect("mock_database.db")
    c = db.cursor()
    c.execute("""CREATE TABLE userdata(ID TEXT, PUBLIC_KEY TEXT, SYMETRIC_KEY TEXT, IV TEXT)""")
    db.commit()
    db.close()
    
    return None

def insertdatabase_client(key, iv, client_pub):
    many_users = 1
    db = sql.connect("mock_database.db")
    c = db.cursor()
    c.execute("INSERT INTO userdata VALUES (?, ?, ?, ?)", (str(many_users), str(key), str(iv), str(client_pub)))
    db.commit()
    
    db.close()
    
    

def databasecreate_codes(db):
    db = sql.connect("mock_database.db")
    c = db.cursor()
    c.execute("""CREATE TABLE userdoor_codes(ID TEXT, NFC TEXT, PERMISSIONS TEXT)""")
    db.commit()
    db.close()
    
    return None

def insertdatabase_NFC(NFC, user):
    db = sql.connect("mock_database.db")
    c = db.cursor()
    c.execute("INSERT INTO userdoor_codes VALUES (?, ?, ?)", (user, str(NFC), str("all")))
    db.commit()
    
    db.close()

def handle_client(client_sock, addr):
    try:
        print(f"Got connection from {addr}")

        # Send data to the client
        message = "Hello, client. Thanks for connecting!"
        client_sock.send(message.encode())
        
        
        client_pub = RSA.importKey(client_sock.recv(2048), passphrase=None)
        user = "1"
        d = hashlib.sha256(user.encode("utf8")).digest()
        print(d)
        server_priv, server_pub = set_asymetric()	
        client_sock.send(server_pub.exportKey(format='PEM', passphrase=None, pkcs=1))
        #print(client_pub)
        response = client_sock.recv(1024)
        key = os.urandom(32)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend)
        ud = hashlib.sha256(str(key).encode("utf8")).digest()
        st = {"You are client": str(1) , "cipher":  str (base64.b64encode (key), "utf8"), "iv":  str (base64.b64encode (iv), "utf8"), "sig": server_priv.sign(ud, 32)}
        send_dict(client_sock, st)
        encryptor = cipher.encryptor()
        decryptor = cipher.decryptor()
        if response.decode() == "I'm a cliente":
            insertdatabase_client(key, iv, client_pub)
        while True:
            request = recv_dict(client_sock)
            if request["command"] == "NFC":
                data = ''.join(random.choices(string.ascii_letters + string.digits, k=50))

# Create an NDEF Text Record
                record = ndef.TextRecord(data)

# Encode the record
                #message = [record]

# Convert the message to bytes
                #encoded_message = bytes(ndef.message_encoder(message))

# Convert bytes to hexadecimal string
                #hex_string = binascii.hexlify(encoded_message).decode()
                insertdatabase_NFC(str(record), str(request["I'm"]))
                st = {"NFC code": str(record)}
                send_dict(client_sock, st)
                

                
                



    except Exception as e:
        print(f"Error in handling client: {e}")

    finally:
        # Close the connection
        client_sock.close()

def set_asymetric(): 
	priv = RSA.generate(2048)
	pub = priv.publickey()

	return priv, pub

# Create a socket object
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the local machine name and a port
    host = socket.gethostname()
    port = 9999  # You can use any available port
    
    db = sql.connect("mock_database.db")
    c = db.cursor()
    try:
            a = c.execute("SELECT * FROM userdata")
            print(9)
            for row in a:
                print(row)
            db.close()
    except(sql.Error):
            databasecreate_user(db)
            print(0)
            db.close()
    db2 = sql.connect("mock_database.db")
    c = db2.cursor()
    try:
            a = c.execute("SELECT * FROM userdoor_codes")
            print(9)
            for row in a:
                print(row)
            db2.close()
    except(sql.Error):
            databasecreate_codes(db2)
            print(0)
            db2.close()

# Bind to the port
    server_socket.bind((host, port))

# Listen for incoming connections
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:
    # Accept incoming connection
        client_sock, addr = server_socket.accept()

    # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_sock, addr))
        client_handler.start()
        
if __name__ == "__main__":
    main()
        
        
        
    
    
