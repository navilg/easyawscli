#!/usr/bin/python3

from os import system, name

def mainmenu():
    print("AWS CLI Interface\n")
    print("0. Exit\n1. Start EC2 instance\n2. Stop EC2 instance\n3. Tag an instance\n4. Add IP in SG\n5. Remove an IP from SG\n6. Autoscaling Group suspend process")
    mainmenu_choice = input("Choose from above (0 to 5): ")
    return(mainmenu_choice)

def startEC2():
    print("StartEC2")
    clear()

def clear():
    print("Clear")
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

if __name__ == "__main__":
    choice = mainmenu()
    print(choice)

    if choice == 1:
        startEC2()
    elif choice == 2:
        stopEC2()
    elif choice == 3:
        tagInstance()
    elif choice == 4:
        addIPinEC2()
    elif choice == 5:
        removeIPinEC2()
    elif choice == 6:
        suspendProcess()
    else:
        print("Wrong choice")
        exit(1)

