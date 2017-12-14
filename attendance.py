import time
import datetime


global names
names = ["Jackathon", "Boomer Kingston", "Paul Deangelo-Willis"]

menu_options = ["1) Sign in", "2) Sign out", "3) Quit"]



def scan_id(option=0):
    global name
    name = input("What's your name?")
    if name in names:
        #stuff that was in the log() function
        print("Logging file...")
        log_file = open("log.csv","a")
        time.sleep(0.1)

        #this next thing is new
        if option == 1:
            log_file.write("\n" + name + ", " + str(datetime.datetime.now()) + ",SIGNED IN")
            print("You are now signed in!")
        elif option == 2:
            log_file.write("\n" + name + ", " + str(datetime.datetime.now()) + " SIGNED OUT")
            print("You are now signed out! Thanks for coming!")
        else:
            time.sleep(0.1)
    else:
        print("Sorry. Please enter a valid name")
        scan_id()

def main():
    #print("Main has been called!")
    choice = input("Select your command:\n" + " ".join(menu_options) + "\n")
    choice = int(choice)
    if choice == 1:
        scan_id(1)
    elif choice == 2:
        scan_id(2)
    else:
        time.sleep(0.5)
    #scan_id()


if __name__ == "__main__":
    main()
