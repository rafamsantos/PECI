from machine import UART, Pin
from nfc import NFC
import time
import binascii

baudrate = 9600
page_no = '31'
nfc = NFC(baudrate)

while True:
    dataRec = nfc.data_read(page_no)
    if dataRec:
        # Directly print the received data for simplicity
        print("Received data =", dataRec)
    else:
        print("No valid data received or card not detected")
    time.sleep(1)