import RPi.GPIO as GPIO
import SimpleMFRC522
from RPLCD.gpio import CharLCD

import subprocess

import time
import datetime
import os

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
def send_log():
    #if datetime.datetime.today().weekday() == 5 and
    print("about to send log")
    with open("sent_log.txt","r") as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
        print last_line
        if str(datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d').strftime('%m-%d-%y')) in last_line:
            print("it's there duder")
        else:
            print("We're gonna send this one, my man")
            ammended_file = open("sent_log.txt","a")
            ammended_file.write("\n" + str(datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d').strftime('%m-%d-%y')) + " : Sent!")
            os.system("sudo python email_test.py")
             
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

        input1 = GPIO.input(button1)
        input2 = GPIO.input(button2)
        input3 = GPIO.input(button3)
        input4 = GPIO.input(button4)

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
    
def interrupt1():
    print("interrupt1")


def read():

    try:
        id, text = reader.read()
        print(id)
        print(text)
        return text.strip() + "\n"
    finally:
        GPIO.cleanup()
        

def main():
    
    #see if it's time to send the log to Mr. P
    send_log()
    
    buzz()

    interrupt1()
    time.sleep(1)
    #subprocess.call(["omxplayer", "-o", "local", "-l", "0006", "../../Downloads/intro.mp3"])
    display("Please sign in.")

    ids = []
    with open("ids.csv", "r") as ins:
        for line in ins:
            #(key, val) = line.split(',')
            #ids[key] = int(val)
            ids.append(line)
    print(ids)

    global name
    name = read()

    if name in ids:
        short_name = compress_name(name)
        print(short_name)
        display("Select command, " + name)
        interrupt1()
        buzz()
        time.sleep(1)
        choice = pressButton()
        #choice = input("Select your command:\n" + " ".join(menu_options) + "\n")
        #choice = int(choice)

        #open csv log
        print("Logging file...")
        log_file = open("logs/log-" + datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d').strftime('%m-%d-%y') + ".csv","a")
        time.sleep(0.1)

        #print(formatted_name)
        if choice == 1:
            log_file.write("\n" + name + ", " + str(datetime.datetime.now()) + ",SIGNED IN")
            display("    Greetings, \r\n" + name)
            print("Greetings, " + short_name + ". You are now signed in!")
            main()
        elif choice == 2:
            log_file.write("\n" + name + ", " + str(datetime.datetime.now()) + " SIGNED OUT")
            display("    Goodbye, \r\n" + short_name)
            interrupt1()
            time.sleep(1)
            display("   Thanks for \r\n    coming!")
            print("You are now signed out! Thanks for coming!")
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
            
        else:
            time.sleep(0.1)
            main()
    
    else:
        interrupt1()
        display("Sorry. Please scan a valid ID")
        print("Sorry. Please scan a valid ID")

        main()


if __name__ == "__main__":
    main()
