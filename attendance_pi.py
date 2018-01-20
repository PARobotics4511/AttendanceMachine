import RPi.GPIO as GPIO
import SimpleMFRC522
from RPLCD.gpio import CharLCD

import subprocess

import time
import datetime
import os
import csv
#from datetime import datetime, time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Screen Setup--------------------------------------
lcd = CharLCD(pin_rs=22, pin_rw=24, pin_e=23, pins_data=[21, 16, 12, 20],
              numbering_mode=GPIO.BCM,

cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True)


#-end-----------------------------------------------

button1= 6 #gray1
button2= 13 #blue
button3= 19 #red
button4= 26 # grey 2

menu_options = ["1) Sign in", "2) Sign out", "3) Quit"]

#testing-----------------------------------------------------------
reader = SimpleMFRC522.SimpleMFRC522()

GPIO.setwarnings(False)

#reading/writing
'''def write():
    try:
        text = raw_input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")

    finally:
        GPIO.cleanup()
'''
def read():
    
    try:
        #check_closingtime()
        id, text = reader.read()
        print(id)
        print(text)
        return text.strip() + "\n"
    finally:
        GPIO.cleanup()
        
def compress_name(name):
    name_list = name.split("_")
    formatted_name = str(name_list[0] + " " + name_list[1][0])
    return formatted_name
    
def buzz():
    buzz_pin = 27
    GPIO.setup(buzz_pin, GPIO.OUT)
    GPIO.output(buzz_pin, GPIO.HIGH)
    print("buzzing")
    time.sleep(0.5)
    GPIO.output(buzz_pin, GPIO.LOW)
    
def pressButton():
    button1= 6 #gray1
    button2= 13 #blue
    button3= 19 #red
    button4= 26 # grey 2

    GPIO.setup(button1, GPIO.IN)
    GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(button3, GPIO.IN)
    GPIO.setup(button4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    previous_input = 1

    while True:

        input1 = GPIO.input(button2)
        input2 = GPIO.input(button3)
        input3 = GPIO.input(button4)
        input4 = GPIO.input(button1)

        if((True) and ((not input1) or (not input2) or (not input3) or (not input4))):

            if(not input1):
               print("Button 1 Pressed!")
               return 1
            elif(not input2):
               print("Button 2 Pressed!")
               return 2
            elif(not input3):
               print("Button 3 Pressed!")
               return 3
            elif(not input4):
               print("Button 4 Pressed!")
               return 4

        time.sleep(0.1)

def display(message):
    lcd = CharLCD(pin_rs=22, pin_rw=24, pin_e=23, pins_data=[21, 16, 12, 20],
              numbering_mode=GPIO.BCM,

    cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True)

    lcd.write_string(message)

def clear():
    lcd = CharLCD(pin_rs=22, pin_rw=24, pin_e=23, pins_data=[21, 16, 12, 20],
              numbering_mode=GPIO.BCM,

    cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True)
    lcd.clear()
    time.sleep(0.5)
    
def interrupt1():
    print("interrupt1")

def main():
    clear()
    time.sleep(0.5)
    
    #check_closingtime()
    #see if it's time to send the log to Mr. P
    #send_log()
    
    #buzz()
    display("Please sign in.")
    time.sleep(1)

    
    
    ids = []
    with open("/home/pi/Documents/AttendanceMachine/ids.csv", "r") as ins:
        for line in ins:
            #(key, val) = line.split(',')
            #ids[key] = int(val)
            ids.append(line)
    print(ids)

    global name
    name = read()

    if name in ids:
        clear()
        buzz()
        time.sleep(1)
        clear()
        short_name = compress_name(name)
        print(short_name)
        display("Select command, " + short_name)
        time.sleep(0.5)
        choice = pressButton()
        clear()
        time.sleep(0.05)
        #choice = input("Select your command:\n" + " ".join(menu_options) + "\n")
        #choice = int(choice)

        #open csv log
        print("Logging file...")
        log_file = open("/home/pi/Documents/AttendanceMachine/logs/log-" + datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d').strftime('%m-%d-%y') + ".csv","ab")
        writer = csv.writer(log_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        #time.sleep(0.5)
        
        #print(formatted_name)
        if choice == 1:
            clear()
            time.sleep(0.5)
            writer.writerow([name,str(datetime.datetime.now()),'SIGNED IN'])
            display("    Greetings, \r\n   " + short_name)
            print("Greetings, " + short_name + ". You are now signed in!")
            time.sleep(1)
            log_file.close()
            print("clearing...")
            clear()
            time.sleep(0.8)
            print("done clearing")
            main()
        elif choice == 2:
            clear()
            time.sleep(0.5)
            writer.writerow([name,str(datetime.datetime.now()),'SIGNED OUT'])
            display("    Goodbye, \r\n    " + short_name)
            print("You are now signed out! Thanks for coming!")
            time.sleep(1)
            log_file.close()
            clear()
            time.sleep(0.8)
            main()
        elif choice == 3:
            buzz()
            time.sleep(0.2)
            buzz()
            time.sleep(0.2)
            buzz()
            interrupt1()
            time.sleep(1)
            clear()
            time.sleep(1)
            main()
        elif choice == 4:
            clear()
            
        else:
            time.sleep(0.1)
            main()
    
    else:
        interrupt1()
        time.sleep(1.5)
        display("Sorry. Please scan a valid ID")
        print("Sorry. Please scan a valid ID")

        main()


if __name__ == "__main__":
    main()
