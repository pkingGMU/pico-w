import time
import network
import urequests
from time import sleep
import machine
import sys
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB332
import pngdec
import ubinascii  # Used for base64 encoding

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

auth_username = creds.get("auth_username")
auth_password = creds.get("auth_password")


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
url = 'http://pico.artoria.ooguy.com/get_latest_message' 

# Create a PicoGraphics instance
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_RGB332)

# Set the backlight so we can see it!
display.set_backlight(.8)

# Create some pens for use later.
BG = display.create_pen(200, 200, 200)
TEXT = display.create_pen(0, 0, 0)

# Clear the screen initially
display.set_pen(BG)
display.clear()
display.update()

# Create an instance of the PNG Decoder
png = pngdec.PNG(display)


latest_message = ' '


while True:

    

    

    
    try:
        
        response = requests.get(url, auth=(auth_username, auth_password))
        latest_message = response.text
        print(f'Latest message: {latest_message}')
    

        # Update display only if the message changes
        if latest_message != last_message:
            last_message = latest_message
            display.set_pen(BG)
            display.clear()
            display.set_pen(TEXT)
            display.text(latest_message, 10, 10, 115, 2)
            display.update()
            print(f'Updated message: {latest_message}')

    except Exception as e:
        print(f'Error: {e}')

    # Debug memory usage
    gc.collect()  # Force garbage collection
    print(f"Free memory: {gc.mem_free()} bytes")
    

    try:
        # Open our PNG File from flash. In this example we're using an image of a cartoon pencil.
        # You can use Thonny to transfer PNG Images to your Pico.
        png.open_file("carc.png")

        # Get the image dimensions (you need to know the size of your image)
        width, height = 140, 140

        # Calculate the position to center the image
        x_position = (135 - width) // 2  # Centered X
        y_position = ((240 - height) // 2) + 50  # Centered Y

        

        # Decode our PNG file and set the X and Y
        png.decode(x_position, y_position, scale=1)

    # Handle the error if the image doesn't exist on the flash.
    except OSError:
        print("Error: PNG File missing. Copy the PNG file from the example folder to your Pico using Thonny and run the example again.")

    display.update()

    # We're not doing anything else with the display now but we want to keep the program running!
    while True:
        pass