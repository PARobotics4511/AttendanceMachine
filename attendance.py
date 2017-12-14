import time
import datetime




#names = ["Jackathon", "Boomer Kingston", "Paul Deangelo-Willis"]


menu_options = ["1) Sign in", "2) Sign out", "3) Quit"]



def main():

    # THIS IS ALL NEW--------------------
    ids = {}
    with open("ids.txt", "r") as ins:
        for line in ins:
            (key, val) = line.split()
            ids[key] = int(val)
    print(ids)
    # -------------------------------------
    global name
    name = input("What's your name?")

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
