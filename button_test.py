import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

button1= 13 #blue 
button2= 19 #red
button3= 6 # grey 1
button4= 26 # grey 2

GPIO.setup(button1, GPIO.IN)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3, GPIO.IN)
GPIO.setup(button4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

previous_input = 1

while True:
    
   
    input1 = GPIO.input(button4)
    
    
    #print(input1)
   
    if((not previous_input) and input1):
        print("Button pressed!")
    #update previous input
    previous_input = input1
    time.sleep(0.1)
