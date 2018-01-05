import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN)

previous_input = 0

while True:
    input1 = GPIO.input(17)
    if((not previous_input) and input1):
        print("Button pressed! Good job duder")
    #update previous input
    previous_input = input1
    time.sleep(0.05)
