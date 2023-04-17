# obstacle-detection-and-location-sharing-system With Raspberry Pi, sim 808, RF module, Ultrasonic Sensors, and Twilio
This Python script is designed for a Raspberry Pi and is used to build an obstacle detection and location sharing system. It uses distance sensors, an RF receiver, a buzzer, a button, a GPS module, and Twilio for sending SMS messages. Here is a brief overview of the different components and their functions:

Twilio Setup: Twilio is used to send SMS messages containing GPS location data when the button is pressed.
SIM808 GPS Setup: The SIM808 GPS module is used to obtain the GPS location data.
Button Setup: A button is used to trigger the sending of the SMS with GPS data.
GPIO Pins Setup: The script sets up the pins for the distance sensors, RF receiver, buzzer, and a vibration motor.
Distance Measuring: The script measures the distance to obstacles using two ultrasonic distance sensors.
RF Receiver: An RF receiver is used to control the buzzer remotely.
Main Loop: The script continuously measures the distance to obstacles, checks for button press and RF receiver commands, and sends the SMS with GPS data when the button is pressed.
When the script is running, it will do the following:

Measure the distance to obstacles using two distance sensors.
If an obstacle is detected within a specific range or the remote control is on, the buzzer will be activated.
If the button is pressed, the script will read GPS data from the GPS module.
If the GPS data is successfully read, an SMS will be sent to a specified phone number containing the GPS coordinates and a Google Maps link. The vibration motor will be activated briefly to indicate that the SMS has been sent.
If the GPS data could not be read, the vibration motor will stay off, and an error message will be printed.
In case of a keyboard interrupt, the script will turn off the GPS module, close the serial connection, clean up the RF device, and reset the GPIO pins.
![image](https://user-images.githubusercontent.com/66757712/232483658-f8e64e47-d94d-4ebe-93ba-996bb579faf4.png)
