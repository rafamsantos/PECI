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
import bingogame
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from parea import gameFlag

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the server's hostname and port
server_host = socket.gethostname()
server_port = 9999

# Connect to the server
client_socket.connect((server_host, server_port))

# Receive data from the server
response = client_socket.recv(1024)
print(f"Server says: {response.decode()}")

# Close the connection
client_socket.close()
