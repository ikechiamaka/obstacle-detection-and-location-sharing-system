import time
import serial
import RPi.GPIO as GPIO
from rpi_rf import RFDevice
from twilio.rest import Client

# Twilio setup
account_sid = "ACbb4c1eae87185b2b552ccfafca723ac4"
auth_token = "c18a825f2f73a659ea5ac9064cc7e9ab"
client = Client(account_sid, auth_token)

# SIM808 GPS setup
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

# Button setup
button_pin = 19
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up GPIO pins

BUZZER_PIN = 25

GPIO_TRIGGER1 = 12
GPIO_ECHO1 = 16
GPIO_TRIGGER2 = 21
GPIO_ECHO2 = 20

RF_PIN = 27  # The RF receiver pin
vibrator = 22
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(vibrator, GPIO.OUT)
GPIO.output(vibrator, GPIO.LOW)
# Set up RF receiver
rf_device = RFDevice(RF_PIN)
rf_device.enable_rx()

ON_SIGNAL = 8465154  # Replace with your remote's ON code
OFF_SIGNAL = 8465156 # Replace with your remote's OFF code
remote_status = False

def distance(trigger, echo):
    # Send a pulse to the sensor
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    # Measure the time it takes for the pulse to bounce back
    start_time = time.time()
    
    
    while GPIO.input(echo) == 0:
        start_time = time.time()

    stop_time = time.time()
    while GPIO.input(echo) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance_cm = (elapsed_time * 34300) / 2
    return distance_cm

def read_gps_data1():
    ser.write(b'AT+CGNSINF\r')
    time.sleep(1)
    response = ser.readlines()
    
    for line in response:
        if b'+CGNSINF:' in line:
            gps_data = line.split(b',')
            latitude = gps_data[3]
            longitude = gps_data[4]
            return f"Latitude: {latitude.decode('utf-8')}, Longitude: {longitude.decode('utf-8')}"
    return None

def read_gps_data():
    ser.write(b'AT+CGNSINF\r')
    time.sleep(1)
    response = ser.readlines()
    
    for line in response:
        if b'+CGNSINF:' in line:
            gps_data = line.split(b',')
            latitude = gps_data[3].decode('utf-8')
            longitude = gps_data[4].decode('utf-8')
            return latitude, longitude
    return None


def send_sms(latitude, longitude):
    google_maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    message_body = f"GPS Location: Latitude: {latitude}, Longitude: {longitude}\nGoogle Maps: {google_maps_url}"

    message = client.api.account.messages.create(
        to="+447856203083",
        from_="+15077282871",
        body=message_body
    )



try:
    ser.write(b'AT+CGNSPWR=1\r')  # Turn on GPS
    time.sleep(1)

    while True:
        # Distance measuring and RF receiver
        distance1 = distance(GPIO_TRIGGER1, GPIO_ECHO1)
        distance2 = distance(GPIO_TRIGGER2, GPIO_ECHO2)
        print("Distance1: {:.2f} cm".format(distance1))
        print("Distance2: {:.2f} cm".format(distance2))

        if rf_device.rx_code_timestamp != 0:
            if rf_device.rx_code == ON_SIGNAL:
                remote_status = True
            elif rf_device.rx_code == OFF_SIGNAL:
                remote_status = False

        if (distance1 < 100 or distance2 < 50) or remote_status:  # obstacle detected within 1 meter or remote status is ON
            GPIO.output(BUZZER_PIN, GPIO.HIGH)  # activate buzzer
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)  # turn off buzzer

        # Check if the button is pressed
        button_state = GPIO.input(button_pin)
        if button_state == False:
            print("Button pressed, sending GPS data...")
            gps_data = read_gps_data()
            if gps_data:
                latitude, longitude = gps_data
                send_sms(latitude, longitude)
                GPIO.output(vibrator, GPIO.HIGH)
                print("SMS sent.")
                time.sleep(1)
                GPIO.output(vibrator, GPIO.LOW)
                
            else:
                GPIO.output(vibrator, GPIO.LOW)
                print("Failed to read GPS data.")
            time.sleep(1)

        time.sleep(0.5)

except KeyboardInterrupt:
    ser.write(b'AT+CGNSPWR=0\r')  # Turn off GPS
    ser.close()
    rf_device.cleanup()
    GPIO.cleanup()

