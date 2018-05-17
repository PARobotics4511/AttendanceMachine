import RPi.GPIO as GPIO
import SimpleMFRC522
from RPLCD.gpio import CharLCD

from check_closing_time import check
import subprocess
from threading import Thread
import time
import datetime
import os
import csv

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
global reader
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

def interrupt1():
    print("interrupt1")

def main():
    clear()

    display_now = Thread(target=display("Please sign in"))
    display_now.start()

    ids = []
    with open("/home/pi/Documents/AttendanceMachine/ids.csv", "r") as ins:
        for line in ins:
            #(key, val) = line.split(',')
            #ids[key] = int(val)
            ids.append(line)

    global name
    name = read()

    if name in ids:
        display_now.join

        clear()
        short_name = compress_name(name)
        print(short_name)
        display_now = Thread(target=display("Select command, " + short_name))
        display_now.start()

        choice = pressButton()
        clear()

        #open csv log
        print("Logging file...")
        log_file = open("/home/pi/Documents/AttendanceMachine/logs/log-" + datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d').strftime('%m-%d-%y') + ".csv","ab")
        writer = csv.writer(log_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        if choice == 1:
            display_now.join()
            clear()

            writer.writerow([name,str(datetime.datetime.now()),'SIGNED IN'])

            display_second  = Thread(target=display("    Greetings, \r\n   " + short_name))
            display_second.start()
            time.sleep(1.25)
            print("Greetings, " + short_name + ". You are now signed in!")

            log_file.close()
            print("clearing...")
            clear()

            print("done clearing")
            #time.sleep(2.5)
            display_second.join()
            main()
        elif choice == 2:
            display_now.join()
            clear()
            #time.sleep(0.5)
            writer.writerow([name,str(datetime.datetime.now()),'SIGNED OUT'])
            display_third = Thread(target=display("    Goodbye, \r\n    " + short_name))
            display_third.start()
            print("You are now signed out! Thanks for coming!")

            log_file.close()
            time.sleep(2.25)

            display_third.join()
            main()
        elif choice == 3:
            display_now.join()
            buzz()
            time.sleep(0.2)
            display_now.join()
            buzz()
            time.sleep(0.2)display_now.join()
            buzz()
            time.sleep(0.2)
        elif choice == 4:
            display_now.join()
            clear()
            main()

        else:
            display_now.join()
            time.sleep(0.1)
            main()

    else:
        #interrupt1()
        time.sleep(1.5)
        display("Sorry. Please scan a valid ID")
        print("Sorry. Please scan a valid ID")

        main()

try:
    if __name__ == "__main__":
        start_checking = Thread(target=check())
        main()

except KeyboardInterrupt:
    GPIO.cleanup()
    start_checking.join()
    sys.exit()
