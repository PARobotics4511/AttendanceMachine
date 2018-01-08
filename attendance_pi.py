import RPi.GPIO as GPIO
import SimpleMFRC522
from RPLCD.gpio import CharLCD

import time
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Screen Setup--------------------------------------
lcd = CharLCD(pin_rs=22, pin_rw=24, pin_e=23, pins_data=[21, 16, 12, 20],
              numbering_mode=GPIO.BCM,

cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True)

#lcd.write_string('Mahoney & Luke\r\n  are great2!')
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
def buzz():
    buzz_pin = 27
    GPIO.setup(buzz_pin, GPIO.OUT)
    #GPIO.output(buzz_pin, GPIO.HIGH)
    
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

        '''print("input 1 = " + str(input1))
        print("input 2 = " + str(input2))
        print("input 3 = " + str(input3))
        print("input 4 = " + str(input4))'''

        if((True) and ((not input1) or (not input2) or (not input3) or (not input4))):
            '''print("input 1 = " + str(input1))
            print("input 2 = " + str(input2))
            print("input 3 = " + str(input3))
            print("input 4 = " + str(input4))'''

            if(not input1):
               print("Button 1 Pressed!")
               #previous_input = input1
               return 1
            elif(not input2):
               print("Button 2 Pressed!")
               #previous_input = input2
               return 2
            elif(not input3):
               print("Button 3 Pressed!")
               #previous_input = input3
               return 3
            elif(not input4):
               print("Button 4 Pressed!")
               #previous_input = input4
               return 4
        #update previous input

        time.sleep(0.1)

def display(message):
    lcd = CharLCD(pin_rs=22, pin_rw=24, pin_e=23, pins_data=[21, 16, 12, 20],
              numbering_mode=GPIO.BCM,

    cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True)

    lcd.write_string(message)


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
    buzz()
    interrupt1()
    time.sleep(0.6)
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
    #read()
    #display(name)

    if name in ids:
        display("Select command, " + name)
        interrupt1()
        time.sleep(1)
        choice = pressButton()
        #choice = input("Select your command:\n" + " ".join(menu_options) + "\n")
        #choice = int(choice)

        #stuff that was in the log() function
        print("Logging file...")
        log_file = open("log.csv","a")
        time.sleep(0.1)

        #input1 = GPIO.input(button2)
        #this next thing is new
        #choice = pressButton()

        if choice == 1:
            log_file.write("\n" + name + ", " + str(datetime.datetime.now()) + ",SIGNED IN")
            display("    Greetings, \r\n" + name)
            print("Greetings, " + name + ". You are now signed in!")
        elif choice == 2:

            log_file.write("\n" + name + ", " + str(datetime.datetime.now()) + " SIGNED OUT")
            display("    Goodbye, \r\n" + name)
            interrupt1()
            time.sleep(1)
            display("   Thanks for \r\n    coming!")
            print("You are now signed out! Thanks for coming!")
        else:
            time.sleep(0.1)
    else:
        interrupt1()
        display("Sorry. Please scan a valid ID")
        print("Sorry. Please scan a valid ID")

        main()

    #print("Main has been called!")



if __name__ == "__main__":
    main()
