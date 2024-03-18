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

# Function to handle each client's connection
backend = default_backend()
many_users = 0
many_doors = 0


def databasecreate_user(db):
    db = sql.connect("mock_database.db")
    c = db.cursor()
    c.execute("""CREATE TABLE userdata(ID TEXT, PERMISSIONS TEXT)""")
    db.commit()
    db.close()
    
    return None

def permission(user):
    per = "normal"
    db3 = sql.connect("mock_database.db")
    c = db3.cursor()
    a = c.execute("SELECT * FROM userdata")
    for row in a:
        if row[0] == user:
            per = row[1]
            break
    db3.close()
    
    
    
    
    return per


def databasecreate_door(db):
    db = sql.connect("mock_database.db")
    c = db.cursor()
    c.execute("""CREATE TABLE doordata(ID TEXT, Sock TEXT, Should_Open TEXT, Permission_Type Text)""")
    db.commit()
    db.close()
    
    return None


def databasecreate_log(db):
    db = sql.connect("mock_database.db")
    c = db.cursor()
    c.execute("""CREATE TABLE Logue(ID TEXT, DOOR TEXT)""")
    db.commit()
    db.close()
    
    return None

def open_door(client_name, door):
    db3 = sql.connect("mock_database.db")
    c = db3.cursor()
    a = c.execute("SELECT * FROM doordata")
    for row in a:
        if row[3] == client_name:
            c.execute("UPDATE doordata SET Should_Open = ? WHERE ID = ?", ("Yes", str(door)))
            break
        
    db3.commit()
    db3.close() 
    

def check_if_remote_open(door):
    shoudl = 0
    db3 = sql.connect("mock_database.db")
    c = db3.cursor()
    a = c.execute("SELECT * FROM doordata")
    for row in a:
        if row[0] == str(door):
            if row[2] == "Yes":
                c.execute("UPDATE doordata SET Should_Open = ? WHERE ID = ?", ("No", row[0]))
                shoudl = 1
                break
    
    
    db3.commit()
    
    return shoudl

def read_log(user):
    
    strigue = ""
    db3 = sql.connect("mock_database.db")
    c = db3.cursor()
    a = c.execute("SELECT * FROM Logue when ID LIKE ?", (user))
    for row in a:
        stringue = stringue+row+"\n"
    db3.close()
    
    
    return stringue


def insertdatabase_door(id, sock):
    many_doors = 1
    db = sql.connect("mock_database.db")
    c = db.cursor()
    c.execute("INSERT INTO doordata VALUES (?, ?, ?, ?)", (str(id), str(sock), "No", "normal"))
    db.commit()
    
    db.close()
    


def check_nfc(nfc, door):
    
        shoudl = False
        print("Ola")
        user1 = 0
        user_permision = 0
        door_permissions = 0
    

        db = sql.connect("mock_database.db")
        c = db.cursor()
        a = c.execute("SELECT * FROM userdoor_codes")
        #a = c.execute("SELECT * FROM userdata")
        
        #b = c2.execute("SELECT * FROM doordata")
        
        #v = c3.execute("SELECT * FROM userdoor_codes")
        
        for row in a:
            if row[1] == nfc:
                user1 = row[0]     
        db.close()
        
        
        db2 = sql.connect("mock_database.db")
        c = db2.cursor()
        a = c.execute("SELECT * FROM userdata")
        for row in a:
            if row[0] == user1 :
                user_permision = row[1]  
        db2.close()
        #user_permision = "normal"
        
        
        db3 = sql.connect("mock_database.db")
        c = db3.cursor()
        a = c.execute("SELECT * FROM doordata")
        for row in a:
            if row[0] == door :
                door_permissions = row[3]     
        db3.close()
        
        print(user1)
        print(user_permision)
        print(door_permissions)
        if user1 != 0:
            if door_permissions == user_permision:
                shoudl = True
        
    

    
        return shoudl


    
    
    

def databasecreate_codes(db):
    db = sql.connect("mock_database.db")
    c = db.cursor()
    c.execute("""CREATE TABLE userdoor_codes(ID TEXT, NFC TEXT)""")
    db.commit()
    db.close()
    
    return None

def insertdatabase_NFC(user, NFC):
    db = sql.connect("mock_database.db")
    c = db.cursor()
    c.execute("INSERT INTO userdoor_codes VALUES (?, ?)", (user, str(NFC)))
    db.commit()
    
    db.close()

def handle_client(client_sock, addr):
    try:
        data = client_sock.recv(1024)
        if data.decode() == "Im client":
            
            message = "Send Name"
            client_sock.send(message.encode())
            print(f"Got connection from {addr}")
            
            client_name = client_sock.recv(1024).decode() #Turnar compativel com a autenticação
            
            
            permi = permission(client_name)
            
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
            ud = SHA256.new(bytearray(key))
            cipherR = PKCS1_OAEP.new(client_pub)
            cipher_rsa = cipherR.encrypt(key)

# Encode the encrypted key as base64
            client_sock.send(base64.b64encode(cipher_rsa) )
            print(type(cipher_rsa))
            signaturaRSA = PKCS1_v1_5.new(server_priv)
            st = {"You are client": str(1) ,  "iv":  str (base64.b64encode (iv), "utf8"), "sig": str(base64.b64encode(signaturaRSA.sign(ud)), "utf8"), "Your permisions": str(permi)}
            #verificar manual crypto sobre signature
            send_dict(client_sock, st)
            encryptor = cipher.encryptor()
            decryptor = cipher.decryptor()
            if response.decode() == "I'm a cliente":
                while True:
                    request = recv_dict(client_sock)
                    print(request)
                    
                    ud = SHA256.new(bytearray(request["I'm"].encode()))
                    u = PKCS1_v1_5.new(client_pub).verify(ud, base64.b64decode(request["Sig"]))
                    if u != True:
                        st = {"Compromise": "You where compromise\nQuiting..."}
                        send_dict(client_sock, st)
                        client_sock.close() 
                    elif request["command"] == "NFC":
                        print("here!!!")
                        data = ''.join(random.choices(string.ascii_letters + string.digits, k=15))

# Create an NDEF Text Record
                        data = data.zfill(16)
                #record = ndef.TextRecord(data)

# Encode the record
                #message = [record]

# Convert the message to bytes
                #encoded_message = bytes(ndef.message_encoder(message))

# Convert bytes to hexadecimal string
                #hex_string = binascii.hexlify(encoded_message).decode()
                        insertdatabase_NFC(str(data), str(request["I'm"]))
                        #insertdatabase_NFC(client_name, str("1b233a49"))
                        record = encryptor.update(str(data).encode("utf-8")) + encryptor.finalize()
                        st = {"NFC code": str( base64.b64encode (record), "utf-8")}
                        send_dict(client_sock, st)
                    elif request["command"] == "LOG":
                            to_sent = read_log(request["User"])
                            record = encryptor.update(str(to_sent).encode("utf-8")) + encryptor.finalize()
                            st = {"The Logs": str(base64.b64encode (record), "utf8")}
                            send_dict(to_sent)
                    
                    elif request["command"] == "Ademistrator_open":
                        #open_door(client_name)
                        open_door(permi, request["door"])

        else:
            message = "Whitch door?"
            client_sock.send(message.encode())
            num = client_sock.recv(1024)
            insertdatabase_door(num.decode(), client_sock)
            message = "You are set"
            client_sock.send(message.encode())
            while True:
                data = client_sock.recv(1024)
                message = "Hello door"
                should = check_if_remote_open(num.decode())
                if should == 1:
                    message = "Door, remote open"
                    client_sock.send(message.encode())
                else:
                    if check_nfc(data.decode(), num.decode()):
                        message = "You can open"
                        client_sock.send(message.encode())
                    else:
                        client_sock.send(message.encode())
                
            
 

                
                



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
    HOST = '192.168.118.147'  # Listen on all network interfaces 
                                                                
    PORT = 12345      # Port to listen on
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the local machine name and a port
    server_socket.bind((HOST, PORT))
    
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
    
    db3 = sql.connect("mock_database.db")
    c = db3.cursor()
    try:
            a = c.execute("SELECT * FROM Logue")
            print(9)
            for row in a:
                print(row)
            db3.close()
    except(sql.Error):
            databasecreate_log(db3)
            print(0)
            db3.close()
    
    db4 = sql.connect("mock_database.db")
    c = db4.cursor()
    try:
            a = c.execute("SELECT * FROM doordata")
            print(9)
            for row in a:
                print(row)
            db4.close()
    except(sql.Error):
            databasecreate_door(db4)
            print(0)
            db4.close()

# Bind to the port

# Listen for incoming connections
    server_socket.listen(5)


    while True:
    # Accept incoming connection
        client_sock, addr = server_socket.accept()

    # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_sock, addr))
        client_handler.start()
        
if __name__ == "__main__":
    main()
