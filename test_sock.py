import socket
import network  # Import the network module
import machine
from machine import Pin, SPI, PWM, I2C
from nfc import NFC
import utime, time
import st7789
import socket
import vga1_bold_16x32 as font
import os
buzzer = PWM(Pin(15))  # buzzer pin connected to GPIO15

def bequiet():
    buzzer.duty_u16(0)

data = '1B233A49'  # must be 4 byte, for write
baudrate = 9600  # communication buadrate between pico W and NFC module
page_no = '15'  # memory location divided into pages NTAG213/215/216 -> 4bytes per page
nfc = NFC(baudrate)  # create object

# define and configure SPI for Display
spi = SPI(1, baudrate=40000000, sck=Pin(10), mosi=Pin(11))
tft = st7789.ST7789(spi, 240, 240, reset=Pin(12, Pin.OUT), cs=Pin(9, Pin.OUT), dc=Pin(8, Pin.OUT),
                      backlight=Pin(13, Pin.OUT), rotation=1)  # SPI interface for tft screen

bequiet()

# WiFi module configuration
WIFI_SSID = 'Gal'
WIFI_PASSWORD = 'Jmml1234.'
bequiet()

# Server configuration
SERVER_HOST = '192.168.71.147'  # IP address of the server
SERVER_PORT = 12345                 # Port the server is listening on
bequiet()

# Connect to WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
bequiet()
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# Wait until connected to WiFi
while not wifi.isconnected():
    tft.init()  # initialize display
    tft.fill(0)  # clear display
    tft.text(font, "Not Connected!!!", 70, 100, st7789.CYAN)  # print on tft screen
    time.sleep(1)  # wait for 1 second
    bequiet()
    wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
client_socket.connect((SERVER_HOST, SERVER_PORT))
print("Connected to server")
while True:
    bequiet()
    tft.init()  # initialize display
    tft.fill(0)  # clear display
    tft.text(font, "Send!", 70, 100, st7789.CYAN)  # print on tft screen
    time.sleep(1)  # wait for 1 second

    # Send data to the server
    message = "Hello, server!"
    client_socket.sendall(message.encode())
    print("Sent:", message)




