import RPi.GPIO as GPIO
import SimpleMFRC522

import time
import datetime

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
    
    if name in ids:
        choice = input("Select your command:\n" + " ".join(menu_options) + "\n")
        choice = int(choice)

        #stuff that was in the log() function
        print("Logging file...")
        log_file = open("log.csv","a")
        time.sleep(0.1)

        #this next thing is new
        if choice == 1:
            log_file.write("\n" + name + ", " + str(datetime.datetime.now()) + ",SIGNED IN")
            print("You are now signed in!")
        elif choice == 2:
            log_file.write("\n" + name + ", " + str(datetime.datetime.now()) + " SIGNED OUT")
            print("You are now signed out! Thanks for coming!")
        else:
            time.sleep(0.1)
    else:
        print("Sorry. Please enter a valid name")
        main()

    #print("Main has been called!")



if __name__ == "__main__":
    main()
