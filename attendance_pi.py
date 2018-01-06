import RPi.GPIO as GPIO
import SimpleMFRC522
from RPLCD.gpio import CharLCD

import time
import datetime

GPIO.setmode(GPIO.BCM)

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
def display(message):
    lcd = CharLCD(pin_rs=22, pin_rw=24, pin_e=23, pins_data=[21, 16, 12, 20],
              numbering_mode=GPIO.BCM,

    cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True)

    lcd.write_string(message)
    
def read():
    
    try:
        id, text = reader.read()
        print(id)
        print(text)
        return text.strip() + "\n"
    finally:
        GPIO.cleanup()

def main():
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
        display(name)
        choice = input("Select your command:\n" + " ".join(menu_options) + "\n")
        choice = int(choice)

        #stuff that was in the log() function
        print("Logging file...")
        log_file = open("log.csv","a")
        time.sleep(0.1)
        
        #input1 = GPIO.input(button2)
        #this next thing is new
        if choice == 1:
            log_file.write("\n" + name + ", " + str(datetime.datetime.now()) + ",SIGNED IN")
            display("Greetings, " + name)
            print("Greetings, " + name + ". You are now signed in!")
        elif choice == 2:
            log_file.write("\n" + name + ", " + str(datetime.datetime.now()) + " SIGNED OUT")
            display("You are now signed out! Thanks for coming!")
            print("You are now signed out! Thanks for coming!")
        else:
            time.sleep(0.1)
    else:
        display("Sorry. Please scan a valid ID")
        print("Sorry. Please scan a valid ID")
        main()

    #print("Main has been called!")



if __name__ == "__main__":
    main()
