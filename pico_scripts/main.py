from time import sleep
import time
import network
import urequests
import machine
import sys
import gc
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB332, PEN_P4
import pngdec
import mrequests as requests
from pimoroni import Button
from pimoroni import RGBLED

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

##############################################################

# Create a PicoGraphics instance
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_RGB332)
# X and Y max of display
x_max = 240
y_max = 135

#------------------------------------------------------------------------------------------------------------
# Set the backlight so we can see it!
display.set_backlight(.8)

# Set font
display.set_font("bitmap8")

# Define colors
RED = display.create_pen(255, 000, 000)
GREEN = display.create_pen(000, 255, 000)
BLUE = display.create_pen(000, 000, 255)
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(000, 000, 000)

def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()


#------------------------------------------------------------------------------------------------------------

clear()

#------------------------------------------------------------------------------------------------------------

# Define Buttons
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

# Define LED Pin number
led = RGBLED(6,7,8)

# Set default rgb light
led.set_rgb(10,10,0)

# Cats
cat_state = 'default'




# Create an instance of the PNG Decoder
png = pngdec.PNG(display)


latest_message = ' '


while True:

    # Set background color
    display.set_pen(BLACK)
    display.update()
    

    # We use this to reset whether to display the last message
    button_pressed = False
    look_back = False
    mood_state = None
    

    # Read the button states
    x_pressed = button_x.read()
    y_pressed = button_y.read()
    a_pressed = button_a.read()
    b_pressed = button_b.read()


    # Check state of the buttons
    if a_pressed:
        clear()
        display.set_pen(WHITE)
        display.text("Looking back one message", 10, 10, 115, 2)
        display.update()
        led.set_rgb(11,11,11)
        time.sleep(5)
        clear()
        button_pressed = True
        look_back = True

    if x_pressed and y_pressed:
        clear()
        display.set_pen(BLUE)
        display.text("Mood reset", 10, 10, 115, 2)
        display.update()
        led.set_rgb(1,1,1)
        time.sleep(5)
        clear()
        button_pressed = True

        cat_state = 'default'

    if y_pressed and not x_pressed:
        clear()
        display.set_pen(RED)
        display.text("Mood changed to negative", 10, 10, 115, 2)
        display.update()
        led.set_rgb(50,0,0)
        time.sleep(5)
        clear()
        button_pressed = True

        cat_state = 'negative'
    
    if x_pressed and not y_pressed:
        clear()
        display.set_pen(BLUE)
        display.text("Mood changed to positive", 10, 10, 115, 2)
        display.update()
        led.set_rgb(0,0,50)
        time.sleep(5)
        clear()
        button_pressed = True

        cat_state = 'positive'

    
    
        
    
    
    
    
    try:
        
        response = requests.get(url, auth=(auth_username, auth_password))
        latest_message = response.text
        print(f'Latest message: {latest_message}')
    

        # Update display only if the message changes
        if latest_message != last_message or button_pressed == True:
            last_message = latest_message
            display.set_pen(BLACK)
            display.clear()
            display.set_pen(WHITE)
            display.text(latest_message, 10, 10, 115, 2)
            display.update()
            print(f'Updated message: {latest_message}')

    except Exception as e:
        print(f'Error: {e}')

    # Debug memory usage
    gc.collect()  # Force garbage collection
    print(f"Free memory: {gc.mem_free()} bytes")
    
    if cat_state == 'default':
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



    elif cat_state == 'positive':
        try:
            # Open our PNG File from flash. In this example we're using an image of a cartoon pencil.
            # You can use Thonny to transfer PNG Images to your Pico.
            png.open_file("Gray_Content.png")

            # Get the image dimensions (you need to know the size of your image)
            width, height = 140, 127

            # Calculate the position to center the image
            x_position = (135 - width) // 2  # Centered X
            y_position = ((240 - height) // 2) + 50  # Centered Y

            

            # Decode our PNG file and set the X and Y
            png.decode(x_position, y_position, scale=1)

        # Handle the error if the image doesn't exist on the flash.
        except OSError:
            print("Error: PNG File missing. Copy the PNG file from the example folder to your Pico using Thonny and run the example again.")


    elif cat_state == 'negative':
        print("Negative")
    
    else:
        print("You did something wrong")


   
    time.sleep(1)  # Wait before the next request
    display.update()

    print(f'cats is equal to: {cat_state}')

    