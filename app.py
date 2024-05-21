import signal
import socket
import threading
import logging
from cmath import sqrt
import os
import sys
import ast
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
#import nfcpy
#from ndef import NdefMessage
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
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import requests
from zxcvbn import zxcvbn
from URL import IP_AD

app = Flask(__name__)

# Sendgrid configuration    Tirem os espaços e descomentem na parte de baixo
#SENDGRID_API_KEY = 'SG.2dHir0cV     RiqMQwAtxBbSSw.WHxl6ETM5    Kk_GgjovMFsoMn4BzuuHRPXoh-cjcg-0Ks'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['JWT_SECRET_KEY'] = 'voU1coL2ocA1raL3goS1opA4raT1esT5e'
jwt = JWTManager(app)
exit_event = threading.Event()
#dbFlask = SQLAlchemy(app)

#class appCommand(dbFlask.model):
#     id = dbFlask.Column(dbFlask.Integer, primary_key=True)
#     commandFlask = dbFlask.Column(dbFlask.Integer)
     


#@app.route('/door', methods = ['GET'])
#def door_called():
   
#    return jsonify({"User":["Hello","My","World"]})

def is_password_pwned(password):
    hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    hash_prefix = hashed_password[:5]
    hash_suffix = hashed_password[5:]

    url = f'https://api.pwnedpasswords.com/range/{hash_prefix}'
    response = requests.get(url)

    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == hash_suffix:
            return int(count)
        
    return 0



def send_email(recipient_email, subject, body):
    message = Mail(
        from_email='gonalolo12@gmail.com',
        to_emails=recipient_email,
        subject=subject,
        plain_text_content=body
    ) 
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent successfully! Status Code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

def is_email_in_database(email):
    conn = sql.connect('register_users.db')
    cursor = conn.cursor()
    check_email_query = '''SELECT COUNT(*) FROM users WHERE email = ?;'''
    cursor.execute(check_email_query, (email,))
    result = cursor.fetchone()[0]
    conn.close()

    return result > 0

def get_password_by_email(email):
    conn = sql.connect('register_users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE email = ?;', (email,))
    password = cursor.fetchone()
    conn.close()

    return password

def add_user(email, password):
    conn = sql.connect('register_users.db')
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    insert_user_query = '''INSERT INTO users (email, password) VALUES (?, ?);'''
    cursor.execute(insert_user_query, (email, hashed_password))
    conn.commit()
    conn.close()

    return True

# Store token
def store_token(token):
    expires_at = datetime.now() + timedelta(hours=24)
    conn = sql.connect('register_users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM session')  # Clear previous sessions
    cursor.execute('INSERT INTO session (token, expires_at) VALUES (?, ?)', (token, expires_at))
    conn.commit()
    conn.close()

# Retrieve token
def get_token():
    conn = sql.connect('register_users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT token, expires_at FROM session')
    result = cursor.fetchone()
    conn.close()
    
    if result:
        token, expires_at = result
        if datetime.now() < datetime.fromisoformat(expires_at):
            return token
    return None

# Store code
def store_code(code):
    expires_at = datetime.now() + timedelta(minutes=5)
    conn = sql.connect('register_users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO code (code, expires_at) VALUES (?, ?)', (code, expires_at))
    conn.commit()
    conn.close()

def delete_code():
    conn = sql.connect('register_users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM code')  # Clear previous code
    conn.commit()
    conn.close()

# Retrieve code
def get_code():
    conn = sql.connect('register_users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT code, expires_at FROM code')
    result = cursor.fetchone()
    conn.close()
    
    if result:
        code, expires_at = result
        if datetime.now() < datetime.fromisoformat(expires_at):
            return code
    return None



def database_createsome(db):
    db = sql.connect("app.db")
    c = db.cursor()
    c.execute("""CREATE TABLE data(MAC TEXT, RSA_Priv TEXT, RSA_Pub TEXT, SymmetricKey Text, MAC2 TEXT, Command TEXT, DoorNum TEXT)""")
    db.commit()
    db.close()
    
    return None

def database_dataRepo(db):
    db = sql.connect("app.db")
    c = db.cursor()
    c.execute("""CREATE TABLE dataRepository(NFC TEXT, LOG TEXT)""")
    db.commit()
    db.close()
    
    return None

def insert_database_NFC(NFC_code):
    
    db = sql.connect("app.db")
    c = db.cursor()
    c.execute("INSERT INTO dataRepository VALUES (?, ?)", (NFC_code, "None"))
    db.commit()
    
    db.close()

    return None


def get_database_NFC(NFC_code):
    
    db = sql.connect("app.db")
    print("access granted")
    c = db.cursor()
    a = c.execute("SELECT * FROM data")
    print("granting more")
    nfc = None
    for row in a:
            if row[0] == "None":
                nfc = row[0]
                c.execute("UPDATE dataRepository SET NFC = ? WHERE NFC = ?", ("None", row[0]))

                break
            
    db.commit()               
    db.close()
    return nfc
    

backend = default_backend()

def delete_dataRepository(db):
    db = sql.connect("app.db")
    c = db.cursor()
    c.execute("""DROP TABLE dataRepository""")
    db.commit()
    db.close()


    return None

def database_insertrc(db):
     
    db = sql.connect("app.db")
    c = db.cursor()
    c.execute("INSERT INTO data VALUES (?, ?, ?, ?, ?, ?, ?)", ("User", "None","None","None","None","None","None"))
    db.commit()
    
    db.close()

    return None


def set_asymetric(): 
	priv = RSA.generate(2048)
	pub = priv.publickey()

	return priv, pub


def set_input(command): 
    db = sql.connect("app.db")
    print("input set")
    c = db.cursor()
    a = c.execute("SELECT * FROM data")
    for row in a:
            c.execute("UPDATE data SET Command = ? WHERE MAC = ?", (command, row[0]))
            print(row)
            break
            
    db.commit()               
    db.close()
    
    
    
    
    return None

def set_MAC(mac): 
    db = sql.connect("app.db")
    print("input set")
    c = db.cursor()
    a = c.execute("SELECT * FROM data")
    for row in a:
            c.execute("UPDATE data SET MAC2 = ? WHERE MAC = ?", (mac, row[0]))
            print(row)
            break
            
    db.commit()               
    db.close()
    
    
    
    
    return None


def get_MAC(): 
    db = sql.connect("app.db")
    print("input set")
    c = db.cursor()
    a = c.execute("SELECT * FROM data")
    mac = 0
    for row in a:
            mac = row[4]
            break
                        
    db.close()
    
    
    
    
    return mac

def do_not_have_MAC():
    db = sql.connect("app.db")
    print("input set")
    c = db.cursor()
    a = c.execute("SELECT * FROM data")
    mac = True
    for row in a:
            if row[4] != "None":
                mac = False
            break
                        
    db.close()
    
    
    
    
    return mac


def set_door(command): 
    db = sql.connect("app.db")
    c = db.cursor()
    a = c.execute("SELECT * FROM data")
    for row in a:
            c.execute("UPDATE data SET DoorNum = ? WHERE MAC = ?", (command, row[0]))
            break
            
    db.commit()               
    db.close()
   
    return None


def check_for_input():
    
    db = sql.connect("app.db")
    c = db.cursor()
    a = c.execute("SELECT * FROM data")
    comand = 4
    for row in a:
        if row[5] != "None":
            comand = row[5]
            c.execute("UPDATE data SET Command = ? WHERE MAC = ?", ("None", row[0]))
            break
            
    db.commit()               
    db.close()
    
    return comand

def check_for_door():
    
    door = 1
    db = sql.connect("app.db")
    c = db.cursor()
    a = c.execute("SELECT * FROM data")
    comand = 4
    for row in a:
        if row[5] != "None":
            door = row[6]
            break
            
    db.commit()               
    db.close()
    
    return 1

def insert_database_log(log):

    db = sql.connect("app.db")
    c = db.cursor()
    c.execute("INSERT INTO dataRepository VALUES (?, ?)", ("None", log))
    db.commit()

    db.close()

    return None

def get_database_log():

    db = sql.connect("app.db")
    print("access granted")
    c = db.cursor()
    a = c.execute("SELECT * FROM dataRepository")
    print("granting more")
    log = None
    for row in a:
            if row[1] == "None":
                log = row[1]
                c.execute("UPDATE dataRepository  SET LOG = ? WHERE LOG = ?", ("None", row[1]))

                break

    db.commit()
    db.close()
    return log

def insert_doorNum_ADMIN(doorNum):

    db = sql.connect("app.db")
    c = db.cursor()
    for row in doorNum:
        c.execute("INSERT INTO doorNumAdmin VALUES (?)",row)
    db.commit()

    db.close()

    return True

def get_doorNum_ADMIN():
    
    dbDoor = sql.connect("app.db")
    c = dbDoor.cursor()
    c.execute("SELECT * FROM doorNumAdmn")

    doorA = c.fetchall()

    dbDoor.close()
    return doorA


# def insert_doorNum_REG(doorNum):

#     db = sql.connect("app.db")
#     c = db.cursor()
#     for row in doorNum:
#         c.execute("INSERT INTO doorNumApp VALUES (?)", row)
#     db.commit()

#     db.close()

#     return True



#Start flask server
def run_Flask():
    #while not exit_event.is_set():
    app.run(host=IP_AD,port=3000,debug=False)




# def signal_handler(sig, frame):
#     print("Ctrl+C pressed. Exiting...")
#     exit_event.set()
    




def run_app():
# Create a socket object
    
    SERVER_HOST = IP_AD  # IP address of the server
    SERVER_PORT = 12346              # Port the server is listening on
    
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    
# Connect the socket to the server's address and port
    client_sock.connect((SERVER_HOST, SERVER_PORT))

    db4 = sql.connect("app.db")
    c2 = db4.cursor()
    new = 0
    try:
            a2 = c2.execute("SELECT * FROM data")
            print(9)
            for row in a2:
                print(row)
            
            database_insertrc(db4)
            new = 1
            db4.close()
    except(sql.Error):
            database_createsome(db4)
            database_insertrc(db4)
            print(0)
            db4.close()
            new = 0

    db4 = sql.connect("app.db")
    c3 = db4.cursor()
    try:
            a2 = c3.execute("SELECT * FROM dataRepository")
            print(9)
            for row in a2:
                print(row)
            delete_dataRepository(db4)
            database_dataRepo(db4)
            db4.close()
    except(sql.Error):
            database_dataRepo(db4)
            print(0)
            db4.close()
   

   

# Connect to the server
# Receive data from the server
    
    message = "Im client"
    client_sock.send(message.encode())
    
    response = client_sock.recv(1024)
    name = "rmlameiras@ua.pt"
    message = "rmlameiras@ua.pt"
    client_sock.send(message.encode())
    response = client_sock.recv(1024) 
    if do_not_have_MAC():
        message = "-1"
        client_sock.send(message.encode())
        mac = client_sock.recv(1024)
        set_MAC(mac.decode())
        message = "Done"
        client_sock.send(message.encode())
    
    else:
        mac = get_MAC()
        client_sock.send(mac.encode())
        
    response = client_sock.recv(1024)    
    print(f"Server says: {response.decode()}") 

    message = "Give num doors"
    client_sock.send(message.encode())
    door_sql = client_sock.recv(1024)
    #insert_doorNum_ADMIN(door_sql)
    user = "1"
    client_priv = RSA.generate(2048)
    client_pub = client_priv.publickey()
    #client_priv, client_pub = set_asymetric()	
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
       
        comand = check_for_input()
       
        if(int(comand) == 1): #Generate NFC
            ud = SHA256.new(bytearray(name.encode()))
            signaturaRSA = PKCS1_v1_5.new(client_priv)
            st = {"command": "NFC", "door": comand, "I'm": name, "Sig": str(base64.b64encode(signaturaRSA.sign(ud)), "utf8")}
            send_dict(client_sock, st)
            
            NFC_code = recv_dict(client_sock)
            print(NFC_code)
            NFC_code = decryptor.update(base64.b64decode(NFC_code["NFC code"])) + decryptor.finalize()
            insert_database_NFC(NFC_code)
            print("NFC is in database now")
            record = ndef.TextRecord(NFC_code)
            print(record)
            set_input(4)
        
        elif(int(comand) == 2):#Logs
            ud = SHA256.new(bytearray(name.encode()))
            signaturaRSA = PKCS1_v1_5.new(client_priv)
            st = {"command": "LOG", "door": comand, "I'm": name, "Sig": str(base64.b64encode(signaturaRSA.sign(ud)), "utf8")}
            send_dict(client_sock, st)
            log = client_sock.recv(1024)
            log = log.decode()
            print(log)
            insert_database_log(log)
            set_input(4)
        
        elif(int(comand) == 3): #addmistrator open door
            ud = SHA256.new(bytearray(name.encode()))
            signaturaRSA = PKCS1_v1_5.new(client_priv)
           # print("which door?\n")
            do = check_for_door()
            st = {"command": "Ademistrator_open", "door": comand, "I'm": name, "Sig": str(base64.b64encode(signaturaRSA.sign(ud)), "utf8"), "door": do}
            send_dict(client_sock, st)
            set_input(4)
             
        #set_input(4)
    
#Flaks Routes

@app.route('/')
def index():
    return "Server Online"   

@app.route('/door', methods = ['GET'])
def door_called():
    set_input(2)
    print("Command sent")
    return jsonify("Connection Established")
    # data = {
    #     'variable':  get_database_NFC(NFC_code)
    # }
    # return jsonify(data)   

@app.route('/doorNum', methods = ['GET'])
def door_num_called():
    dataDoor = get_doorNum_ADMIN
    if dataDoor:
        return jsonify(dataDoor)
    else:
        return jsonify({"error":'Error while fetching doors'}), 500

@app.route('/checkNFC', methods = ['GET'])
def getcommand():
    set_input(1)
    return jsonify("NFC generated")

@app.route('/opendoor', methods = ['GET'])
def door_opened():
    set_input(3)
    print("Command sent")
    return jsonify("Connection Established") 

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    confirmPassword = data.get('confirmPassword')

    # Check if email is in the database
    if is_email_in_database(email):
        response = {'message': 'Email already in use'}
        return jsonify(response)
    

    # # Password Checks
    # password_strength = zxcvbn(password)
    # pwned_count = is_password_pwned(password)


    # if pwned_count > 0:
    #     response = {'message': 'Password has been compromised before. Use a different one'}
    #     return jsonify(response)

    # if password_strength['score'] < 2:
    #     response = {'message': 'Use a stronger password'}
    #     return jsonify(response)
    
    # Generate a random 6-digit code
    code = ''.join(random.choices(string.digits, k=6))

    # Store the code in the session temporarily
    store_code(code)

    subject = 'Door App Login Verification Code'
    body = f'Your verification code is: {code}'
    if send_email(email, subject, body):
        response = {'message': 'Redirecting to Email Verification'}
        return jsonify(response)
    else:
        response = {'message': 'Failure in Sending Email Verification Code'}
        return jsonify(response)    


@app.route('/verifyEmail', methods=['POST'])
def verifyEmail():
    # Get the code entered by the user
    data = request.get_json()
    user_code = data.get('code')
    user_email = data.get('email')
    user_pass = data.get('password')
    print(user_code)
    #a = int(user_code)
    #a = get_code()
   
    #print(get_code())
 
    print("Codes printed")
    # Check if the entered code matches the code sent to the user
    if int(user_code) == get_code():
        delete_code()
        add_user(user_email, user_pass)
        response = {'message': 'Successful Email Verification'}
        return jsonify(response)
    else:
        delete_code()
        response = {'message': 'Incorrect Code'}
        return jsonify(response)


@app.route('/signin', methods=['POST'])
def login():

    # Check if session is open
    token = get_token()
    if token:
        response = {'message': 'Session is open'}
        return jsonify(response)

    data = request.get_json()
    email = data.get('username')
    password = data.get('password')

    print(email)

    # Check if the email is in the database
    if not is_email_in_database(email):
        response = {'message': 'Email and/or Password incorrect'}
        return jsonify(response)
    
    # Check if the passwords match
    user_password = get_password_by_email(email)

    print(user_password)
    print(type(user_password))
    print(password)
    print(type(password))


    if not check_password_hash(user_password[0], password):
        response = {'message': 'Email and/or Password incorrect'}
        return jsonify(response)

    # Generate a random 6-digit code
    code = ''.join(random.choices(string.digits, k=6))

     # Store the code in the db temporarily
    store_code(code)

    # Send the code to the user's email
    subject = 'Door App Login Verification Code'
    body = f'Your verification code is: {code}'
    if not send_email(email, subject, body):
        response = {'message': 'Failure in Sending Verification Code'}
        return jsonify(response)
    
    # Create session token
    expires = timedelta(hours=24)
    access_token = create_access_token(identity=email, expires_delta=expires)
    store_token(access_token)

    response = {'message': 'Success in Sending Verification Code'}
    return jsonify(response)


@app.route('/verifyCode', methods=['POST'])
def verifyCode():
    # Get the code entered by the user
    data = request.get_json()
    user_code = data.get('code')
    email = data.get('username')

    # Check if the entered code matches the code sent to the user
    if int(user_code) == get_code():
        delete_code()

        expires = timedelta(hours=24)
        access_token = create_access_token(identity=email, expires_delta=expires)
        store_token(access_token)


        response = {'message': 'Successful Log In'}
        return jsonify(response)
    else:
        delete_code()
        response = {'message': 'Incorrect Code'}
        return jsonify(response)

    
def main():

    app_handler = threading.Thread(target=run_app)
    app_handler.start()

    
if __name__ == "__main__":

    #signal.signal(signal.SIGINT, signal_handler)

    app_handler = threading.Thread(target=run_app)
    flask_handler = threading.Thread(target=run_Flask)
    app_handler.start()
    flask_handler.start() 

    app_handler.join()
    flask_handler.join()
    #main()
    #run_app()    
