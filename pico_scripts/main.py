import time
import network
import urequests
from time import sleep
import machine
import sys

##################### dotenv parsing ##########################

def load_dotenv():
    
    credentials = {}
    try:
        # Open and read text file with info. Wish I could use .env :(
        f = open('env.txt', 'r')
        f = f.read()
        lines = f.splitlines()


        for line in lines:
            if "=" in line:
                key, value = line.split("=", 1)
                credentials[key.strip()] = value.strip()


    except OSError:
        print("Error: .env file not found.")
    return credentials

creds = load_dotenv()

##################### Global variables ########################

# Wi-Fi credentials

ssid = creds.get("SSID")
password = creds.get("PASSWORD")


# Flask app URL
url = 'http://pico.artoria.ooguy.com:5000/get_latest_message'

# Global variables
last_message = "No messages yet."


##############################################################

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print(wlan.ifconfig())

try:
    connect()
except KeyboardInterrupt:
    sys.exit("Error message")

print('Connected to Wi-Fi')

# Flask app URL
url = 'http://pico.artoria.ooguy.com:5000/get_latest_message'

while True:
    try:
        response = urequests.get(url)
        latest_message = response.text
        print(f'Latest message: {latest_message}')
    except Exception as e:
        print(f'Error: {e}')
    
    time.sleep(10)  # Check every 10 seconds